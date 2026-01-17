import requests
import json
import urllib.parse
from get_pol_doc import get_polarion_document
from get_wi_list import get_workitemList

# --- SETTINGS ---
SERVER_URL = "https://almdev.mahle/polarion/rest/v1"
PROJECT_ID = "PDPXMT"
TOKEN = "eyJraWQiOiI1ZjA2NWZmZC0wYTkxNGEzMC0wNWE0YjE4Yy1hNTQxMWYyNCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiYzhjMmU1NGUtMGE5MTRhMzAtNzY5MjAyZDUtODM4NWNjOGIiLCJleHAiOjE4NTQ5MTMzNzQsImlhdCI6MTc2ODU5OTc3NH0.TpQf5YcwVx3GZ14KD6YMWU9AaXVF5mno4UvBQ61MNBmr1Y_5ltvCP8pnjbl9skFh2nsvzmR2sqYdb1HlLvjLJgdGTDpWdmN_X7pcRZkvg9QqQA6zgXXjKhTgA1Tp0A_ztQ_Umhr1D_HvI3AODf7vc84rBgzZhbAHVEk3vluXigKweyExEQZX7TiIl7BWZ2fbr1nLzCmdAv1dJfI3OFFf30rwbv4WXL6zt0sVWptbymVdTlA5TjcY-BKyg-bFTvV62hktMH3LhPQ0FqsNCkoYSPjKEPx7nLkwBD7MNC9ZvFkUIHDG3tzQOw2nL7IWVYAN2wxCyh2_bgFzkDZsRBFJuw" # (Your token)
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
    'Content-Type': 'application/json', 
    'Accept': 'application/json'
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

def test_connection(_SERVER_URL, _PROJECT_ID, loc_headers):
    # This is the simplest possible call to verify access
    url_connectionTest = f"{_SERVER_URL}/projects/{_PROJECT_ID}"
    
    print(f"Connecting to: {url_connectionTest}...")
    
    try:
        response = requests.get(url_connectionTest, headers=loc_headers, verify=False)
        
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

        
        

def create_n_move(_SERVER_URL, _PROJECT_ID, _SPACE_ID, _DOC_NAME, _PARENT_ID,_req_data, _doc_url, loc_headers):

    # Assuming _req_data structure is: {"data": {"attributes": {"title": "...", "type": "..."}}}
    new_title = _req_data['data'][0]['attributes']['title']
    new_type = _req_data['data'][0]['attributes']['type']
    
    # Use your existing function
    existing_items = get_workitemList(_doc_url, new_type, loc_headers)
    
    print(f"title of new item: {new_title}")
    print(f"type of new item: {new_type}")
    # Check if title exists in the returned list
    for item in existing_items:
        print(f"title of in list: {item.get('attributes', {}).get('title')}")
        # Note: Adjust 'title' key depending on how your get_workitemList parses data
        if item.get('attributes', {}).get('title') == new_title:
            print(f"Skipping: Work Item '{new_title}' already exists in document.")
            return item.get('id')
            
    url = f"{_SERVER_URL}/projects/{_PROJECT_ID}/workitems"
     
    # OR keep data=json.dumps(req_data) with the explicit header above.
    response = requests.post(
        url, 
        headers=loc_headers, 
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
                        "id": f"{_PROJECT_ID}/{_PARENT_ID}",
                        "type": "workitems"
                    }
                }
            }
        }]
    }

    # Use POST to add the new link
    link_res = requests.post(link_url, headers=loc_headers, json=link_payload, verify=False)

    
    move_data = {
                "targetDocument": doc_ref
    }
    
    print(f"\n[Step 2] Moving to Document: {move_url}")
    print(f"Payload: {json.dumps(move_data)}")
    
    move_res = requests.post(move_url, headers=loc_headers, json=move_data, verify=False)
    
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
              

    print(f"Requesting Document: {doc_url}")
    
    test_connection(SERVER_URL, PROJECT_ID, headers)
    get_polarion_document(doc_url, headers)
    interfaceList = get_workitemList(doc_url, "interface", headers)
    
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
        create_n_move(SERVER_URL, PROJECT_ID, safe_space, DOC_NAME, PARENT_ID, fill_list(wi, "interface"), doc_url, headers)
