import asyncio
import sys
import os
from uuid import uuid4
from datetime import datetime, timedelta

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.database import async_session_maker
from app.models import FamilyAccount, Child, Session, Report, ReportSkillSummary
from app.services.report_service import ReportService
from sqlalchemy import delete

async def test_report_generation():
    print("🚀 Starting Report Service Verification (LLM Integration)...")
    
    async with async_session_maker() as db:
        # 1. Setup Data
        family_id = uuid4()
        child_id = uuid4()
        
        # Create Family & Child
        family = FamilyAccount(family_id=family_id, parent_name="Test Parent", contact_email=f"test_{uuid4()}@example.com", hashed_password="pw")
        child = Child(
            child_id=child_id, 
            family_id=family_id, 
            name="AI Report Kid", 
            level=3,
            birth_date=datetime.now()
        )
        db.add(family)
        db.add(child)
        
        # Create Sessions (Good engagement)
        today = datetime.now()
        for i in range(3):
            s = Session(
                session_id=uuid4(),
                child_id=child_id,
                start_time=today - timedelta(days=i),
                end_time=today - timedelta(days=i) + timedelta(minutes=15),
                duration_seconds=900,
                status="completed",
                session_type="adventure",
                engagement_score=90 + i # High scores
            )
            db.add(s)
        await db.commit()
        
        # 2. Cleanup old reports if any
        await db.execute(delete(Report).where(Report.child_id == child_id))
        await db.commit()

        # 3. Generate Report
        print("\n📝 Generating Monthly Report (calling gpt-4o-mini)...")
        report = await ReportService.generate_monthly_report(db, child_id, today.year, today.month)
        
        # 4. Verify Content
        print(f"\n✅ Report Generated: {report.report_id}")
        print(f"Summary: {report.summary_text}")
        print(f"Strengths: {report.strengths_summary}")
        print(f"Improvements: {report.areas_to_improve}")
        
        # Verify Skills
        print("\n📊 Skill Summaries:")
        stmt = f"SELECT * FROM report_skill_summaries WHERE report_id = '{report.report_id}'"
        # We can just lazily load if attached, but let's query manually to be safe in script
        from sqlalchemy import select
        result = await db.execute(select(ReportSkillSummary).where(ReportSkillSummary.report_id == report.report_id))
        summaries = result.scalars().all()
        for s in summaries:
            print(f" - {s.skill_id}: {s.summary_for_parent}")

        # 5. Cleanup
        print("\n🧹 Cleaning up...")
        # from sqlalchemy import delete # Removed redundant import
        await db.execute(delete(ReportSkillSummary).where(ReportSkillSummary.report_id == report.report_id))
        await db.execute(delete(Report).where(Report.child_id == child_id))
        await db.execute(delete(Session).where(Session.child_id == child_id))
        await db.delete(child)
        await db.delete(family)
        await db.commit()

if __name__ == "__main__":
    asyncio.run(test_report_generation())
