import asyncio
import sys
import os
from httpx import AsyncClient, ASGITransport
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import delete

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.database import async_session_maker
from app.models import FamilyAccount, Child, Session, Report, ChildInventory, ReportSkillSummary
from app.core.security import create_access_token
from app.main import app

from sqlalchemy import delete, select

async def verify_parent_api():
    print("🚀 Starting Parent API Verification...")
    
    async with async_session_maker() as db:
        # 1. Setup Data
        family_id = uuid4()
        child_id = uuid4()
        
        # Create Family
        family = FamilyAccount(
            family_id=family_id,
            parent_name="Parent Tester",
            contact_email=f"parent_test_{uuid4()}@example.com",
            hashed_password="hashed_secret"
        )
        db.add(family)
        
        # Create Child
        child = Child(
            child_id=child_id,
            family_id=family_id,
            name="Report Kid",
            birth_date=datetime.now(),
            level=2,
            xp=150
        )
        db.add(child)
        
        # Create Dummy Sessions for Stats
        for i in range(5):
             s = Session(
                 session_id=uuid4(),
                 child_id=child_id,
                 start_time=datetime.now() - timedelta(days=i),
                 end_time=datetime.now() - timedelta(days=i) + timedelta(minutes=10),
                 duration_seconds=600,
                 status="completed",
                 session_type="adventure",
                 engagement_score=85
             )
             db.add(s)
             
        await db.commit()
        
         # Create Token
        token = create_access_token({"sub": str(family.family_id), "family_id": str(family.family_id), "role": "parent"})
        headers = {"Authorization": f"Bearer {token}"}
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            # 2. Test Dashboard Stats
            print("\n🧪 Testing GET /v1/parent/dashboard/stats...")
            resp = await client.get(f"/v1/parent/dashboard/stats?child_id={child_id}", headers=headers)
            print(f"   Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"   Error: {resp.text}")
            assert resp.status_code == 200
            data = resp.json()
            assert data["total_sessions"] >= 5
            assert data["total_learning_time_minutes"] >= 50
            
            # 3. Test Generate Report
            print("\n🧪 Testing POST /v1/parent/reports/generate...")
            today = datetime.now()
            resp = await client.post(
                f"/v1/parent/reports/generate?child_id={child_id}&year={today.year}&month={today.month}",
                headers=headers
            )
            print(f"   Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"   Error: {resp.text}")
            assert resp.status_code == 200
            report_data = resp.json()
            report_id = report_data["report_id"]
            print(f"   Generated Report ID: {report_id}")
            
            # 4. Test List Reports
            print("\n🧪 Testing GET /v1/parent/reports...")
            resp = await client.get(f"/v1/parent/reports?child_id={child_id}", headers=headers)
            print(f"   Status: {resp.status_code}")
            assert resp.status_code == 200
            reports = resp.json()
            assert len(reports) >= 1
            assert reports[0]["report_id"] == report_id
            
            # 5. Test Get Report Detail
            print("\n🧪 Testing GET /v1/parent/reports/{report_id}...")
            resp = await client.get(f"/v1/parent/reports/{report_id}", headers=headers)
            print(f"   Status: {resp.status_code}")
            assert resp.status_code == 200
            detail = resp.json()
            assert detail["report_id"] == report_id
            if "skill_summaries" in detail:
                 print(f"   Skill Summaries: {len(detail['skill_summaries'])}")
            else:
                 print("   Skill Summaries: None (check schema or eager load)")

        # 6. Cleanup
        print("\n🧹 Cleaning up...")
        # Delete related entities first to avoid FK constraint/nullify issues
        
        # Delete Skill Summaries via Subquery
        skill_subq = select(Report.report_id).where(Report.child_id == child_id)
        await db.execute(delete(ReportSkillSummary).where(ReportSkillSummary.report_id.in_(skill_subq)))
        
        await db.execute(delete(Report).where(Report.child_id == child_id))
        await db.execute(delete(Session).where(Session.child_id == child_id))
        await db.execute(delete(ChildInventory).where(ChildInventory.child_id == child_id))
        
        await db.delete(child)
        await db.delete(family)
        await db.commit()

    print("\n✅ Parent API Verification Completed Successfully!")

if __name__ == "__main__":
    asyncio.run(verify_parent_api())
