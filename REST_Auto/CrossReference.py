import requests
import json

# --- SETTINGS ---
SERVER_URL = "https://almdev.mahle/polarion/rest/v1"
PROJECT_ID = "PDPXMT"
TOKEN = "eyJraWQiOiI1ZjA2NWZmZC0wYTkxNGEzMC0wNWE0YjE4Yy1hNTQxMWYyNCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiYjgxZjJjMjUtMGE5MTRhMzAtNzY5MjAyZDUtNmY4ODQyNTQiLCJleHAiOjE3Njg1MTQ0MDAsImlhdCI6MTc2ODMyMDYwOX0.cgcxtn_N8cL1MBImCdzhXv7UYjWr-N8pzyuSRPbYgx1v6HxtN5wGz3GKSu5ExnSitjeAAD8qtJdir74CxAwf3G4srP62b0JGCbgWDyvQagp35iYrHSuRz9Ih-tusaBq5ulf7Vy4ujTMbY_9dS60Sdp_rsOib21-Epit85Y7DjMp5m7fJkin8pwd0u-laGqm16XiHsX5LKnwGx_k44WHMkkpLs97RVUzWzV9hALVYKfxZyJiNl8Db5hhjIs1za0xnyPHuL8rgCQJrHWBEqBqg-amrwwTT85IG7BQZLVK1zVZY0YKg33OHo24NXcFInlueisz0EUM4PaQ6OaHNL_fgeQ"
# Format: "wiki/SW/HLD%20Specs"
DOC_PATH = "wiki/SW/HLD%20Specs" 
# Optional: ID of the heading you want this under (e.g., 'EL-123'). 
# If you don't have one yet, leave as None.
PARENT_ID = None 

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# --- REQUIREMENT DATA ---
req_data = {
    "data": {
        "type": "workitems",
        "attributes": {
            "type": "requirement",
            "title": "Interface1 Conditional Logic",
            "description": {
                "type": "text/html",
                "value": "SWC shall provide interface1 with false when param1 is true"
            },
            "document": DOC_PATH
        }
    }
}

# Add parent relationship only if PARENT_ID is provided
if PARENT_ID:
    req_data["data"]["relationships"] = {
        "parent": {
            "data": {
                "type": "workitems",
                "id": PARENT_ID
            }
        }
    }

# --- EXECUTION ---
def run_trial():
    url = f"{SERVER_URL}/projects/{PROJECT_ID}/workitems"
    response = requests.post(url, headers=headers, data=json.dumps(req_data))
    
    if response.status_code == 201:
        new_id = response.json()['data']['id']
        print(f"Success! Requirement created as: {new_id}")
        print(f"Check your document 'HLD Specs' at the bottom.")
    else:
        print(f"Failed with status {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    run_trial()
