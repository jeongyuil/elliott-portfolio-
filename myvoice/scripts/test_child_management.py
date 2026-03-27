import asyncio
import sys
import os
from httpx import AsyncClient, ASGITransport
from uuid import uuid4
from datetime import datetime, date

# Add project root to sys.path
sys.path.append(os.getcwd())

from app.database import async_session_maker
from app.models import FamilyAccount, Child
from app.core.security import create_access_token
from app.main import app

async def test_child_management():
    print("🚀 Starting Child Management Verification...")
    
    async with async_session_maker() as db:
        # 1. Setup Family
        family_id = uuid4()
        family = FamilyAccount(
            family_id=family_id,
            parent_name="Manager Parent",
            contact_email=f"manage_{uuid4()}@example.com",
            hashed_password="pw"
        )
        db.add(family)
        await db.commit()
        
        # Create Token
        token = create_access_token({"sub": str(family.family_id), "family_id": str(family.family_id), "role": "parent"})
        headers = {"Authorization": f"Bearer {token}"}
        
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            
            # 2. Create Child via API
            print("\n🧪 Testing POST /v1/parent/children...")
            create_payload = {
                "name": "Original Name",
                "birth_date": "2018-01-01",
                "gender": "m",
                "primary_language": "ko"
            }
            resp = await client.post("/v1/parent/children", json=create_payload, headers=headers)
            print(f"   Status: {resp.status_code}")
            if resp.status_code != 201:
                print(f"   Error: {resp.text}")
            assert resp.status_code == 201
            child_data = resp.json()
            child_id = child_data["child_id"]
            print(f"   Created Child: {child_data['name']} ({child_data['birth_date']})")
            
            # 3. Update Child via API
            print("\n🧪 Testing PATCH /v1/parent/children/{child_id}...")
            update_payload = {
                "name": "Updated Name",
                "birth_date": "2019-05-05",  # Changed date
                "gender": "f",               # Changed gender
                "avatar_id": "avatar_fox"
            }
            resp = await client.patch(f"/v1/parent/children/{child_id}", json=update_payload, headers=headers)
            print(f"   Status: {resp.status_code}")
            if resp.status_code != 200:
                print(f"   Error: {resp.text}")
            assert resp.status_code == 200
            updated_data = resp.json()
            
            print(f"   Updated Child: {updated_data['name']} ({updated_data['birth_date']})")
            assert updated_data["name"] == "Updated Name"
            assert updated_data["birth_date"] == "2019-05-05"
            assert updated_data["gender"] == "f"
            assert updated_data["avatar_id"] == "avatar_fox"
            
            # 4. Verify Persistence
            print("\n🧪 Verifying Persistence...")
            resp = await client.get(f"/v1/parent/children/{child_id}", headers=headers)
            persisted_data = resp.json()
            assert persisted_data["name"] == "Updated Name"
            
        # 5. Cleanup
        print("\n🧹 Cleaning up...")
        db.expunge_all() # Clear session to avoid side effects
        
        # Cleanup via SQL execution
        from sqlalchemy import delete
        await db.execute(delete(Child).where(Child.child_id == child_id))
        await db.execute(delete(FamilyAccount).where(FamilyAccount.family_id == family_id))
        await db.commit()

    print("\n✅ Child Management Verification Completed Successfully!")

if __name__ == "__main__":
    asyncio.run(test_child_management())
