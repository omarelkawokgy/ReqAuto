import requests
import urllib.parse

# --- SETTINGS ---
SERVER_URL = "https://almdev.mahle/polarion/rest/v1"
PROJECT_ID = "PDPXMT"
TOKEN = "eyJraWQiOiI1ZjA2NWZmZC0wYTkxNGEzMC0wNWE0YjE4Yy1hNTQxMWYyNCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiYjgxZjJjMjUtMGE5MTRhMzAtNzY5MjAyZDUtNmY4ODQyNTQiLCJleHAiOjE3Njg1MTQ0MDAsImlhdCI6MTc2ODMyMDYwOX0.cgcxtn_N8cL1MBImCdzhXv7UYjWr-N8pzyuSRPbYgx1v6HxtN5wGz3GKSu5ExnSitjeAAD8qtJdir74CxAwf3G4srP62b0JGCbgWDyvQagp35iYrHSuRz9Ih-tusaBq5ulf7Vy4ujTMbY_9dS60Sdp_rsOib21-Epit85Y7DjMp5m7fJkin8pwd0u-laGqm16XiHsX5LKnwGx_k44WHMkkpLs97RVUzWzV9hALVYKfxZyJiNl8Db5hhjIs1za0xnyPHuL8rgCQJrHWBEqBqg-amrwwTT85IG7BQZLVK1zVZY0YKg33OHo24NXcFInlueisz0EUM4PaQ6OaHNL_fgeQ" # (Your token)
# Format: "wiki/SW/HLD%20Specs"
DOC_PATH = "SW/HLD Specs" 
# Optional: ID of the heading you want this under (e.g., 'EL-123'). 
# If you don't have one yet, leave as None.
PARENT_ID = "PDPXMT-25208" 

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}
 
def get_polarion_document(server_url, project_id, space_id, doc_name, token):
    """
    Accesses a specific Polarion LiveDoc and prints its metadata.
    """
    # URL encode IDs to handle spaces or special characters
    safe_space = urllib.parse.quote(space_id)
    safe_doc = urllib.parse.quote(doc_name)
    
    # Endpoint: /projects/{projectId}/spaces/{spaceId}/documents/{documentName}
    url = f"https://{server_url}/polarion/rest/v1/projects/{project_id}/spaces/{safe_space}/documents/{safe_doc}"#https://{server_url}/polarion/#/project/{project_id}/wiki/{safe_space}/{safe_doc}"
 
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    print(f"Requesting Document: {url}")
    
    try:
        response = requests.get(url, headers=headers, verify=False)
        
        if response.status_code == 200:
            doc_data = response.json().get('data', {})
            print("--- ? DOCUMENT ACCESSED ---")
            print(f"Title: {doc_data.get('attributes', {}).get('title')}")
            print(f"Internal ID: {doc_data.get('id')}")
            print(f"Module URI: {doc_data.get('links', {}).get('self')}")
            return doc_data
        else:
            print(f"--- ? FAILED (Status {response.status_code}) ---")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- USAGE ---
# If your path was "SW/HLD Specs", space_id is "SW" and doc_name is "HLD Specs"
get_polarion_document(
    server_url="almdev.mahle",
    project_id="PDPXMT",
    space_id="SW",
    doc_name="HLD Specs",
    token=TOKEN
)
