import asyncio
import sys
import os
from uuid import uuid4

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.database import async_session_maker
from app.models import Child, FamilyAccount
from app.services.gamification_service import GamificationService
from sqlalchemy import select

async def verify_phase4():
    print("🚀 Starting Phase 4 Verification...")
    
    async with async_session_maker() as db:
        # 1. Setup Test Data
        # Create a temp family and child if needed, or pick existing
        # For safety/speed, let's create a new temporary child
        family_id = uuid4()
        child_id = uuid4()
        
        print(f"📝 Creating test child {child_id}...")
        family = FamilyAccount(
            family_id=family_id,
            parent_name="Test Parent",
            contact_email=f"test_p4_{uuid4()}@example.com",
            hashed_password="hashed_secret"
        )
        db.add(family)
        
        child = Child(
            child_id=child_id,
            family_id=family_id,
            name="Gamification Tester",
            birth_date=datetime.now(),
            level=1,
            xp=0,
            avatar_emoji="🐰" # Default legacy
        )
        db.add(child)
        await db.commit()
        
        # 2. Test Gamification Service (XP Award)
        print("\n🧪 Testing GamificationService.award_xp...")
        # Award 50 XP (No Level Up)
        res1 = await GamificationService.award_xp(db, str(child_id), 50, "test")
        print(f"   Award 50 XP: {res1}")
        assert res1["earned_xp"] == 50
        assert res1["total_xp"] == 50
        assert res1["level"] == 1
        assert res1["level_up"] == False
        
        # Award 60 XP (Should Level Up: 50 + 60 = 110 => Level 2)
        # Formula: Level = 1 + (110 // 100) = 2
        res2 = await GamificationService.award_xp(db, str(child_id), 60, "test")
        print(f"   Award 60 XP: {res2}")
        assert res2["total_xp"] == 110
        assert res2["level"] == 2
        assert res2["level_up"] == True
        
        # 3. Test Avatar Logic (Mocking Endpoint Logic)
        print("\n🧪 Testing Avatar Update Logic...")
        # Reload child
        stmt = select(Child).where(Child.child_id == child_id)
        result = await db.execute(stmt)
        child = result.scalar_one()
        
        # Update Avatar ID
        new_avatar_id = "avatar_field_3d"
        child.avatar_id = new_avatar_id
        await db.commit()
        
        # Verify Persistence
        await db.refresh(child)
        print(f"   Child Avatar ID: {child.avatar_id}")
        assert child.avatar_id == new_avatar_id
        
        # 4. Clean up (Optional, but good for repeatable tests)
        print("\n🧹 Cleaning up test data...")
        await db.delete(child)
        await db.delete(family)
        await db.commit()
        
    print("\n✅ Phase 4 Verification Completed Successfully!")

if __name__ == "__main__":
    from datetime import datetime
    asyncio.run(verify_phase4())
