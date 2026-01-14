import requests
import json
import urllib.parse

# --- SETTINGS ---
SERVER_URL = "https://almdev.mahle/polarion/rest/v1"
PROJECT_ID = "PDPXMT"
TOKEN = "eyJraWQiOiI1ZjA2NWZmZC0wYTkxNGEzMC0wNWE0YjE4Yy1hNTQxMWYyNCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiYjgxZjJjMjUtMGE5MTRhMzAtNzY5MjAyZDUtNmY4ODQyNTQiLCJleHAiOjE3Njg1MTQ0MDAsImlhdCI6MTc2ODMyMDYwOX0.cgcxtn_N8cL1MBImCdzhXv7UYjWr-N8pzyuSRPbYgx1v6HxtN5wGz3GKSu5ExnSitjeAAD8qtJdir74CxAwf3G4srP62b0JGCbgWDyvQagp35iYrHSuRz9Ih-tusaBq5ulf7Vy4ujTMbY_9dS60Sdp_rsOib21-Epit85Y7DjMp5m7fJkin8pwd0u-laGqm16XiHsX5LKnwGx_k44WHMkkpLs97RVUzWzV9hALVYKfxZyJiNl8Db5hhjIs1za0xnyPHuL8rgCQJrHWBEqBqg-amrwwTT85IG7BQZLVK1zVZY0YKg33OHo24NXcFInlueisz0EUM4PaQ6OaHNL_fgeQ" # (Your token)
# Format: "wiki/SW/HLD%20Specs"
DOC_PATH = "SW/HLD Specs" 
SPACE_ID = "SW"
DOC_NAME = "HLD Specs"
# Optional: ID of the heading you want this under (e.g., 'EL-123'). 
# If you don't have one yet, leave as None.
PARENT_ID = "PDPXMT-25208" 
SEVERITY = "should_have"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

# --- REQUIREMENT DATA ---


req_data = {
    "data": [
        {
            "type": "workitems",
            "attributes": {
                "type": "der_requirement",
                "title": "My New Requirement2",
                "description": {
                    "type": "text/html",
                    "value": "SWC2 shall provide interface1 with false when param1 is true"
                },
                "severity": SEVERITY
            }
        }  # End of the Work Item dictionary
    ]  # End of the "data" list
}

inter_data = {
    "data": [
        {
            "type": "workitems",
            "attributes": {
                "type": "interface",
                "title": "My interface",
                "description": {
                    "type": "text/html",
                    "value": "SWC_init"
                },
                "severity": SEVERITY
            }
        }  # End of the Work Item dictionary
    ]  # End of the "data" list
}

param_data = {
    "data": [
        {
            "type": "workitems",
            "attributes": {
                "type": "parameter",
                "title": "My Parameter",
                "description": {
                    "type": "text/html",
                    "value": "SWC_Param1"
                },
                "severity": SEVERITY
            }
        }  # End of the Work Item dictionary
    ]  # End of the "data" list
}

# Updated headers dictionary
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",  # CRITICAL: Polarion requires this
    "Accept": "application/json"         # Recommended: Tells Polarion what you expect back
}

def get_polarion_document(_doc_url):
    """
    Accesses a specific Polarion LiveDoc and prints its metadata.
    """
    try:
        response = requests.get(_doc_url, headers=headers, verify=False)
        
        if response.status_code == 200:
            doc_data = response.json().get('data', {})
            print("--- ? DOCUMENT ACCESSED ---")
            print(f"Title: {doc_data.get('attributes', {}).get('title')}")
            print(f"Internal ID: {doc_data.get('id')}")
            print(f"Module URI: {doc_data.get('links', {}).get('self')}")
        else:
            print(f"--- ? FAILED (Status {response.status_code}) ---")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_workitemList(_doc_url, _wi_type):
  # The space and doc name should be raw (e.g. "SW" and "HLD Specs")
  get_items_url = (_doc_url+f"/parts"
  f"?include=workItem"
  f"&fields[workitems]=type,title,id")
  
  print(f"get_items_url: {get_items_url}")
  
  response = requests.get(get_items_url, headers=headers, verify=False)
  print(f"DEBUG: Status Code Received: {response.status_code}") # Add this
  if response.status_code == 200:
      response_json = response.json()
  
      # Polarion REST (JSON:API) stores related objects in 'included'
      included_objects = response_json.get('included', [])
      print(f"DEBUG: Found {len(included_objects)} included_objects(s).")
      
      # Filter 'included' objects where the type is 'interface'
      # In 2026, 'type' is typically an ID within the attributes
      wi_list = [
      obj for obj in included_objects 
      if obj.get('type') == 'workitems' and obj.get('attributes', {}).get('type') == _wi_type
      ]
      print(f"\nTotal wi_list {_wi_type} collected: {len(wi_list)}")
    
      for obj in included_objects:
        #Get the data inside attributes
        attrs = obj.get('attributes', {})
        obj_id = obj.get('id')
        
        #Get the specific Polarion Type (e.g., 'interface', 'requirement', 'heading')
        polarion_type = attrs.get('type')
        title = attrs.get('title', 'NO TITLE')
        
        print(f"--- Object ID: {obj_id} ---")
        print(f"  Resource Type (API): {obj.get('type')}")
        print(f"  Polarion Type (WorkItem): {polarion_type}")
        print(f"  Title: {title}")
  else:
      print(f"Failed to fetch document items: {response.status_code}")
  return wi_list

def test_connection(_SERVER_URL, _PROJECT_ID):
    # This is the simplest possible call to verify access
    url_connectionTest = f"{_SERVER_URL}/projects/{_PROJECT_ID}"
    
    print(f"Connecting to: {url_connectionTest}...")
    
    try:
        response = requests.get(url_connectionTest, headers=headers, verify=False)
        
        if response.status_code == 200:
            print("--- SUCCESS! ---")
            print("Authentication works.")
            print(f"Project Name: {response.json()['data']['attributes']['name']}")
        else:
            print(f"--- FAILED ---")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

        
        

def create_n_move(_SERVER_URL, _PROJECT_ID, _SPACE_ID, _DOC_NAME, _req_data):
    #url = f"{_SERVER_URL}/projects/{PROJECT_ID}/workitems"
    url = f"{_SERVER_URL}/projects/{_PROJECT_ID}/workitems"
    safe_doc = urllib.parse.quote(_DOC_NAME)
    # Use json= instead of data= to let requests handle serialization & headers,
    # OR keep data=json.dumps(req_data) with the explicit header above.
    response = requests.post(
        url, 
        headers=headers, 
        data=json.dumps(_req_data), # Ensure this is a string
        verify=False
    )
    
    if response.status_code == 201:
        # Note: Polarion v1 REST API often returns data in a 'data' wrapper
        response_json = response.json()
        new_id = response_json['data'][0]['id'] 
        print(f"Success! Requirement created as: {new_id}")
    else:
        print(f"Failed with status {response.status_code}")
        print(response.text)
    #new_wi_id = new_wi_id.replace("", _PROJECT_ID)
    new_wi_id = new_id.replace(f"{_PROJECT_ID}/", "")
    print(f"new_wi_id: {new_wi_id}")
    # 2. Move to Document
    # Use just DOC_PATH if it already contains the space (e.g. 'SW/HLD Specs')
    move_url = f"{_SERVER_URL}/projects/{_PROJECT_ID}/workitems/{new_wi_id}/actions/moveToDocument"
    
    doc_ref = f"{_PROJECT_ID}/{_SPACE_ID}/{_DOC_NAME}"
    #/projects/{_PROJECT_ID}/spaces/{_SPACE_ID}/documents/{safe_doc}"
    move_data = {
                "targetDocument": doc_ref
    }
    
    print(f"\n[Step 2] Moving to Document: {move_url}")
    print(f"Payload: {json.dumps(move_data)}")
    
    move_res = requests.post(move_url, headers=headers, json=move_data, verify=False)
    
    if move_res.status_code in [200, 204]:
        print(f"+++ Successfully moved {new_wi_id} into Document.")
    else:
        print(f"!!! Move Failed (Status {move_res.status_code})")
        print(f"Response Body: {move_res.text}")
        
        
        
if __name__ == "__main__":

        # URL encode IDs to handle spaces or special characters
    safe_space = urllib.parse.quote(SPACE_ID)
    safe_doc = urllib.parse.quote(DOC_NAME)
    
    # Endpoint: /projects/{projectId}/spaces/{spaceId}/documents/{documentName}
    doc_url = f"{SERVER_URL}/projects/{PROJECT_ID}/spaces/{safe_space}/documents/{safe_doc}"
 
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/json"
    }

    print(f"Requesting Document: {doc_url}")
    
    test_connection(SERVER_URL, PROJECT_ID)
    get_polarion_document(doc_url)
    get_workitemList(doc_url, "interface")
    #create_n_move(SERVER_URL, PROJECT_ID, SPACE_ID, DOC_NAME, param_data)
