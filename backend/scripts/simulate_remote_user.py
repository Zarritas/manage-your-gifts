import httpx
import sqlite3
import time
import argparse
import sys
import os

# Configuration
BASE_URL = "http://localhost:8000/api"
# Check if DB path exists
DB_PATH = r"d:\Programing\gitrepos\manage-your-gifts\backend\gifts.db"

if not os.path.exists(DB_PATH):
    # Try alternate path if relative path was used in config
    print(f"Warning: DB not found at {DB_PATH}, trying ./gifts.db")
    DB_PATH = r"d:\Programing\gitrepos\manage-your-gifts\backend\gifts.db"

def get_otp(email):
    print(f"Reading OTP for {email} from {DB_PATH}...")
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Find table name: usually emailotp or email_otp. Let's try select from sqlite_master if needed.
        # But previous investigation showed EmailOTP model. Table likely 'emailotp'.
        cursor.execute("SELECT code FROM emailotp WHERE email = ? ORDER BY created_at DESC LIMIT 1", (email,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return row[0]
        return None
    except Exception as e:
        print(f"Error getting OTP: {e}")
        return None

def login(email):
    client = httpx.Client(base_url=BASE_URL)
    # 1. Request OTP
    print(f"Requesting OTP for {email}...")
    try:
        resp = client.post("/auth/send-code", json={"email": email})
        if resp.status_code != 200:
            print(f"Login failed: {resp.text}")
            sys.exit(1)
    except Exception as e:
         print(f"Connection failed: {e}")
         sys.exit(1)
    
    # 2. Get OTP from DB
    time.sleep(1.0) # Wait for DB write
    code = get_otp(email)
    if not code:
        print("Could not find OTP in DB. Is the backend running? Is the DB path correct?")
        sys.exit(1)
    print(f"Found OTP: {code}")

    # 3. Verify
    print("Verifying OTP...")
    resp = client.post("/auth/verify-code", json={"email": email, "code": code})
    if resp.status_code != 200:
        print(f"Verify failed: {resp.text}")
        sys.exit(1)
    
    token = resp.json()["access_token"]
    print(f"Logged in as {email}.")
    return token

def setup_admin(email="admin_script@example.com"):
    token = login(email)
    headers = {"Authorization": f"Bearer {token}"}
    client = httpx.Client(base_url=BASE_URL, headers=headers)
    
    # Update profile name (optional)
    client.put("/users/me", json={"name": "Admin User", "language": "en"})

    # Create Group
    print("Creating Group...")
    resp = client.post("/groups", json={"name": "Realtime Test Group", "description": "For WS Test"})
    if resp.status_code != 200:
        print(f"Create Group failed: {resp.text}")
        sys.exit(1)
    
    group = resp.json()
    print(f"GROUP_ID={group['id']}") # specific format for easy parsing
    return group['id']

def join_group(group_id, user_email):
    token = login(user_email)
    headers = {"Authorization": f"Bearer {token}"}
    client = httpx.Client(base_url=BASE_URL, headers=headers)
    
    # Update profile name
    client.put("/users/me", json={"name": "Joiner User", "language": "en"})

    print(f"Joining group {group_id} as {user_email}...")
    resp = client.post(f"/api/groups/{group_id}/join") 
    # Wait, BASE_URL includes /api? 
    # If BASE_URL is http://localhost:8000/api, then client.post("/groups") is /api/groups
    # but client.post("/api/groups/...") would be /api/api/groups.
    # Checks above: setup_admin used "/groups", correct.
    # join_group above used "/api/groups/..." -> mistype in thought process?
    # Actually, join endpoint is router.post("/{group_id}/join") under prefix /api/groups.
    # So URL is /api/groups/{group_id}/join.
    # If BASE_URL has /api, then we need /groups/{id}/join.
    
    resp = client.post(f"/groups/{group_id}/join")
    print(f"Join response: {resp.status_code} {resp.text}")

def accept_user(group_id, user_email, admin_email="admin_script@example.com"):
    # 1. Login as admin
    token = login(admin_email)
    headers = {"Authorization": f"Bearer {token}"}
    client = httpx.Client(base_url=BASE_URL, headers=headers)
    
    # 2. Find User ID
    print(f"Fetching group details for {group_id}...")
    resp = client.get(f"/groups/{group_id}")
    if resp.status_code != 200:
        print(f"Get Group failed: {resp.text}")
        return

    group_data = resp.json()
    members = group_data.get("members", [])
    
    target_user_id = None
    for m in members:
        if m.get("email") == user_email:
            target_user_id = m.get("user_id")
            break
            
    if not target_user_id:
        print(f"User {user_email} not found in group members list.")
        return

    print(f"Accepting user {target_user_id}...")
    resp = client.post(f"/groups/{group_id}/members/{target_user_id}/accept")
    print(f"Accept response: {resp.status_code} {resp.text}")

def create_gift(group_id, admin_email="admin_script@example.com"):
    token = login(admin_email)
    headers = {"Authorization": f"Bearer {token}"}
    client = httpx.Client(base_url=BASE_URL, headers=headers)
    
    print("Creating Gift...")
    resp = client.post(f"/groups/{group_id}/gifts", json={
        "title": "Scripted Gift",
        "description": "Appears by magic",
        "link": "http://magic.com"
    })
    print(f"Create Gift response: {resp.status_code} {resp.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    
    setup = subparsers.add_parser("setup_admin")
    
    join = subparsers.add_parser("join")
    join.add_argument("--group_id", required=True)
    join.add_argument("--user_email", required=True)

    accept = subparsers.add_parser("accept")
    accept.add_argument("--group_id", required=True)
    accept.add_argument("--user_email", required=True)
    
    gift = subparsers.add_parser("create_gift")
    gift.add_argument("--group_id", required=True)
    
    args = parser.parse_args()
    
    if args.command == "setup_admin":
        setup_admin()
    elif args.command == "join":
        join_group(args.group_id, args.user_email)
    elif args.command == "accept":
        accept_user(args.group_id, args.user_email)
    elif args.command == "create_gift":
        create_gift(args.group_id)
