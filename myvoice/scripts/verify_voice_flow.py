
import urllib.request
import urllib.error
import json
import uuid
import sys

BASE_URL = "http://localhost:8000/v1"

def request(method, endpoint, data=None, headers={}):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    
    if data:
        req.add_header('Content-Type', 'application/json')
        req.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
        except:
            body = e.read().decode()
        return e.code, body
    except Exception as e:
        print(f"Error: {e}")
        return 500, str(e)

def print_step(title):
    print(f"\n=== {title} ===")

def main():
    # 1. Signup/Login Parent
    print_step("1. Parent Auth")
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "password123"
    parent_name = "TestParent"
    
    status, data = request("POST", "/auth/signup", {
        "email": email,
        "password": password,
        "parent_name": parent_name
    })
    
    if status == 409:
        print("User exists, logging in...")
        status, data = request("POST", "/auth/login", {
            "email": email,
            "password": password
        })
    
    if status not in [200, 201]:
        print(f"Auth failed: {status} {data}")
        sys.exit(1)
        
    parent_token = data["access_token"]
    print(f"Parent Token: {parent_token[:20]}...")
    
    # 2. Create Child
    print_step("2. Create Child")
    headers = {"Authorization": f"Bearer {parent_token}"}
    
    child_name = "LunaUser"
    status, data = request("POST", "/parent/children", {
        "name": child_name,
        "birth_date": "2018-01-01", 
        "gender": "F",
        "primary_language": "ko",
        "development_stage_language": "pre-operational"
    }, headers)
    
    if status != 201:
        print(f"Create child failed: {status} {data}")
        sys.exit(1)
        
    child_id = data["child_id"]
    print(f"Child Created: {child_name} ({child_id})")

    # 3. Get Child Token
    print_step("3. Get Child Token")
    status, data = request("POST", "/auth/select-child", {
        "child_id": child_id
    }, headers)
    
    if status != 200:
        print(f"Select child failed: {status} {data}")
        sys.exit(1)
        
    child_token = data["child_token"]
    print(f"Child Token: {child_token}") # Full token needed for browser
    
    # 4. Start Session
    print_step("4. Start Session (Backend Check)")
    kid_headers = {"Authorization": f"Bearer {child_token}"}
    unit_id = "8ca51667-9725-4122-bb0d-ad50072508a0" # Meeting Zoo Friends
    
    status, data = request("POST", "/kid/sessions", {
        "child_id": child_id,
        "session_type": "curriculum",
        "curriculum_unit_id": unit_id
    }, kid_headers)
    
    if status != 201:
        print(f"Start session failed: {status} {data}")
        print("Note: Ensure seed data is populated for this unit ID.")
        sys.exit(1)
        
    print(f"Session Started: {data['sessionId']}")
    print(f"Activities: {len(data['activities'])}")
    for act in data['activities']:
        print(f"- {act['name']} ({act['activityType']})")
        if act.get('introNarratorScript'):
            print(f"  Script: {act['introNarratorScript'][:50]}...")

    print("\nSUCCESS! Backend verification complete.")

if __name__ == "__main__":
    main()
