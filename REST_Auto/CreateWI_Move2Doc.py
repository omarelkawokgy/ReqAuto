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
PARENT_ID = "PDPXMT-25253" 
SEVERITY = "should_have"

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/vnd.api+json', 
    'Accept': 'application/vnd.api+json'
}

# --- REQUIREMENT DATA ---


req_data = {
    "data": [
        {
            "type": "workitems",
            "attributes": {
                "type": "der_requirement",
                "title": "My New Requirement21",
                "description": {
                    "type": "text/html",
                    "value": "ascsdcsd"
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


inter_data_list = [
    {"title": "ACOM_Init", "function": "+ ACOM_Init(): void", "desc": "Initializes the ACOM software component.", "severity": "must_have"},
    {"title": "ACOM_MainFunction", "function": "+ ACOM_MainFunction(): void", "desc": "Periodic main function call for the component.", "severity": "must_have"},
    {"title": "ACOM_SpeedReqRpm_Get", "function": "+ ACOM_SpeedReqRpm_Get(): uint16_t", "desc": "Getter for the requested speed in RPM.", "severity": "should_have"},
    {"title": "ACOM_SpdReqOutOfRngFig_Get", "function": "+ ACOM_SpdReqOutOfRngFig_Get(): boolean", "desc": "Flag indicating if the speed request is out of range.", "severity": "should_have"},
    {"title": "ACOM_SpdFbPwmHz_Get", "function": "+ ACOM_SpdFbPwmHz_Get(): uint16_t", "desc": "Getter for the speed feedback PWM frequency in Hz.", "severity": "should_have"},
    {"title": "ACOM_SpdReqVolt_Set", "function": "+ ACOM_SpdReqVolt_Set(int16_t): void", "desc": "Setter for the requested voltage.", "severity": "should_have"},
    {"title": "ACOM_ActualSpdRpm_Set", "function": "+ ACOM_ActualSpdRpm_Set(int16_t): void", "desc": "Setter for the actual feedback speed in RPM.", "severity": "should_have"}
]

def fill_list(item, wi_type):
  wi_data = {
      "data": [
          {
              "type": "workitems",
              "attributes": {
                  "type": wi_type,
                  "title": item["title"],
                  "description": {
                      "type": "text/html",
                      "value": item["desc"]
                  },
                  "severity": SEVERITY
              }
          }  # End of the Work Item dictionary
      ]  # End of the "data" list
  }
  return wi_data
  
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
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',  # Pure header, no charset
    'Accept': 'application/json'
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

    url = f"{_SERVER_URL}/projects/{_PROJECT_ID}/workitems"
    
    local_headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json', 
    'Accept': 'application/json'
    }
        
    # OR keep data=json.dumps(req_data) with the explicit header above.
    response = requests.post(
        url, 
        headers=local_headers, 
        data=json.dumps(_req_data), # Ensure this is a string
        verify=False
    )
    
    if response.status_code != 201:
        print(f"Failed with status {response.status_code}")
        print(response.text)
        return
        
    # Note: Polarion v1 REST API often returns data in a 'data' wrapper
    response_json = response.json()
    new_id = response_json['data'][0]['id'] 
    print(f"Success! Requirement created as: {new_id}")
        
    #new_wi_id = new_wi_id.replace("", _PROJECT_ID)
    new_wi_id = new_id.replace(f"{_PROJECT_ID}/", "")
    print(f"new_wi_id: {new_wi_id}")
    # 2. Move to Document
    # Use just DOC_PATH if it already contains the space (e.g. 'SW/HLD Specs')
    move_url = f"{_SERVER_URL}/projects/{_PROJECT_ID}/workitems/{new_wi_id}/actions/moveToDocument"
    
    doc_ref = f"{_PROJECT_ID}/{_SPACE_ID}/{_DOC_NAME}"
    
    # The URL targets the 'linkedworkitems' sub-resource of your NEW work item
    link_url = f"{_SERVER_URL}/projects/{_PROJECT_ID}/workitems/{new_wi_id}/linkedworkitems"

    link_payload = {
        "data": [{
            "type": "linkedworkitems",
            "attributes": {
                "role": "parent"  # Change to 'has_parent' if that is your system's ID
            },
            "relationships": {
                "workItem": {
                    "data": {
                        "id": f"{_PROJECT_ID}/{PARENT_ID}",
                        "type": "workitems"
                    }
                }
            }
        }]
    }

    # Use POST to add the new link
    link_res = requests.post(link_url, headers=local_headers, json=link_payload, verify=False)

    
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
        
def wi_link(wi_id, style="long"):
    """Generates the Polarion HTML span for a Work Item link."""
    return f'<span class="polarion-rte-link" data-type="workItem" data-item-id="{wi_id}" data-option-id="{style}"></span>'
        
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
    interfaceList = get_workitemList(doc_url, "interface")
    
    interface1 = interfaceList[0]
    interface1_id = interface1['id'].split('/')[-1] # e.g., 'PDPXMT-25234'

    # Define the new description text using Polarion Wiki Markup for a link
    new_desc_text = (
        "SWC2 shall provide interface1 with false when "
        f"{wi_link(interface1_id)} " # This creates the visual link
        "param1 is true"
    )
    #print(f"req description: {new_desc_text}")
    req_data['data'][0]['attributes']['description']['value'] = new_desc_text
    for wi in inter_data_list:
      create_n_move(SERVER_URL, PROJECT_ID, safe_space, DOC_NAME, fill_list(wi, "interface"))
