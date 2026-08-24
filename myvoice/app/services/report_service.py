from datetime import datetime, timedelta, date
from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
import calendar

from app.models import Report, ReportSkillSummary, Session, SkillLevel
from app.services.aggregation_service import AggregationService

class ReportService:
    @staticmethod
    async def generate_monthly_report(db: AsyncSession, child_id: UUID, year: int, month: int) -> Report:
        """
        Generate a monthly report for a child.
        """
        # 1. Determine Date Range
        _, last_day = calendar.monthrange(year, month)
        start_date = datetime(year, month, 1)
        end_date = datetime(year, month, last_day, 23, 59, 59)
        
        # 2. Check if Report already exists
        stmt = select(Report).where(
            Report.child_id == child_id,
            Report.period_start_date == start_date,
            Report.report_type == "monthly"
        )
        result = await db.execute(stmt)
        existing_report = result.scalar_one_or_none()
        
        if existing_report:
            return existing_report

        # 3. Gather Data (Sessions, Skills)
        # Sessions
        session_stmt = select(Session).where(
            Session.child_id == child_id,
            Session.start_time >= start_date,
            Session.start_time <= end_date
        )
        result = await db.execute(session_stmt)
        sessions = result.scalars().all()
        
        total_sessions = len(sessions)
        avg_engagement = sum(s.engagement_score or 0 for s in sessions) / total_sessions if total_sessions > 0 else 0
        
        from app.services.openai_service import chat_with_ai
        import json

        # 4. Generate AI Summary (Real LLM - gpt-4o-mini for cost optimization)
        # Prepare Context
        context = f"""
        Child ID: {child_id}
        Month: {year}-{month}
        Total Sessions: {total_sessions}
        Average Engagement: {avg_engagement:.1f}
        """
        
        system_prompt = """
        You are an expert child education consultant. Generate a monthly report for a parent based on their child's learning data.
        Return a JSON object with the following keys:
        - summary_text: A warm, encouraging paragraph summarizing the month's progress (Korean).
        - strengths_summary: 2-3 bullet points of what the child did well (Korean).
        - areas_to_improve: 1-2 bullet points of constructive feedback (Korean).
        - skill_summaries: A list of objects { "skill_id": "Vocabulary", "comment": "..." } for Vocabulary, Pronunciation, Fluency.
        
        Tone: Encouraging, professional, yet friendly.
        """
        
        try:
            llm_response = await chat_with_ai(
                system_prompt=system_prompt,
                conversation_history=[],
                child_utterance=context,
                json_mode=True,
                model="gpt-4o-mini" # User requested Cost Optimization
            )
            data = json.loads(llm_response)
        except Exception as e:
            print(f"Report Generation Failed: {e}")
            # Fallback
            data = {
                "summary_text": f"{month}월 학습을 완료했습니다!",
                "strengths_summary": ["- 꾸준히 학습에 참여했습니다."],
                "areas_to_improve": ["- 더 많은 대화를 시도해보세요."],
                "skill_summaries": []
            }

        # Helper to convert list to string
        def list_to_str(val):
            if isinstance(val, list):
                return "\n".join(val)
            return str(val) if val else ""

        # 5. Create Report
        report = Report(
            child_id=child_id,
            period_start_date=start_date,
            period_end_date=end_date,
            report_type="monthly",
            summary_text=data.get("summary_text"),
            strengths_summary=list_to_str(data.get("strengths_summary")),
            areas_to_improve=list_to_str(data.get("areas_to_improve")),
            created_at=datetime.now()
        )
        
        # Fetch family_id
        from app.models import Child
        child_stmt = select(Child).where(Child.child_id == child_id)
        child_result = await db.execute(child_stmt)
        child_obj = child_result.scalar_one()
        report.family_id = child_obj.family_id
        
        db.add(report)
        await db.flush() # Get report_id
        
        # 6. Create Skill Summaries
        skill_comments = {s["skill_id"]: s["comment"] for s in data.get("skill_summaries", [])}
        skills = ["Vocabulary", "Pronunciation", "Fluency"]
        
        for skill in skills:
            skill_summary = ReportSkillSummary(
                report_id=report.report_id,
                skill_id=skill,
                level=child_obj.level, 
                summary_for_parent=skill_comments.get(skill, f"{skill} 능력이 향상되고 있습니다.")
            )
            db.add(skill_summary)
            
        await db.commit()
        await db.refresh(report)
        return report

    @staticmethod
    async def get_latest_report(db: AsyncSession, child_id: UUID) -> Report | None:
        stmt = select(Report).where(Report.child_id == child_id).order_by(Report.created_at.desc()).limit(1)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
