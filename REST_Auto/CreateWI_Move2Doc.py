"""
POLARION WORK ITEM CREATOR & DOCUMENT MOVER
-------------------------------------------
Brief:
    Automates the batch creation of Polarion Work Items (Requirements, Interfaces, 
    Parameters) and attaches them to a specific LiveDoc and Parent Heading.

Key Actions:
    1. Connection Validation: Verifies API access to the project.
    2. Duplicate Prevention: Scans the target LiveDoc to ensure the item doesn't 
       already exist before creating.
    3. Work Item Creation: POSTs new data to the project-level work item endpoint.
    4. Relationship Linking: Automatically links the new item to a 'Parent' work item.
    5. LiveDoc Integration: Executes 'moveToDocument' to place the new item 
       within the specific document structure.
"""

import re
import requests
import json
import urllib.parse
from get_pol_doc import get_polarion_document
from get_wi_list import get_workitemList
SERVER_URL_ALM_DEV = "https://almdev.mahle/polarion/rest/v1"
SERVER_URL_ALM = "https://alm.mahle/polarion/rest/v1"

POE54_ID = "61DE-62527"
XCSP_ID = "XCSP"
TRAINING_ID = "PDPXMT"
MCT_ID = ""

TOKEN_ALMDEV = "eyJraWQiOiI1ZjA2NWZmZC0wYTkxNGEzMC0wNWE0YjE4Yy1hNTQxMWYyNCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiYzhjMmU1NGUtMGE5MTRhMzAtNzY5MjAyZDUtODM4NWNjOGIiLCJleHAiOjE4NTQ5MTMzNzQsImlhdCI6MTc2ODU5OTc3NH0.TpQf5YcwVx3GZ14KD6YMWU9AaXVF5mno4UvBQ61MNBmr1Y_5ltvCP8pnjbl9skFh2nsvzmR2sqYdb1HlLvjLJgdGTDpWdmN_X7pcRZkvg9QqQA6zgXXjKhTgA1Tp0A_ztQ_Umhr1D_HvI3AODf7vc84rBgzZhbAHVEk3vluXigKweyExEQZX7TiIl7BWZ2fbr1nLzCmdAv1dJfI3OFFf30rwbv4WXL6zt0sVWptbymVdTlA5TjcY-BKyg-bFTvV62hktMH3LhPQ0FqsNCkoYSPjKEPx7nLkwBD7MNC9ZvFkUIHDG3tzQOw2nL7IWVYAN2wxCyh2_bgFzkDZsRBFJuw" # (Your token)
TOKEN_ALM = "eyJraWQiOiI0MzFiODM3Mi0wYTkxNjM1Mi03ODJjMDc2ZS04ZDg5NzJkNiIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiMjk5ZDM5MGItMGE5MTYzNTItNjE2YWVjNjQtNGIzMmU1ZmMiLCJleHAiOjE4NjA4MzMyNjIsImlhdCI6MTc3NDUxOTY2Mn0.hir2Qc3dylPKkSqYdkmuOGspPmZYOieZNIsTM9Z-zaVj7V-uzaM0Tsoi3pHdv3ZA8pR6S6xcNWdLjj1dAfKIYhx0p05cwWnUHpYa1RrfQQPTSIrEfCR77jbRG9udWOgZVrUxSpm0ARJhRql5eitcobVSRmg9Lqa8jn27zhpuWP3af4ZpfgVschjE2dDmYXK_zy_XkObfKsuQBGEiT6Au0WyoVi7qRr6UhzxTLQDA70AqqoiPVUq251vWn5b7hBdwouSZsh3RTaBa7gHSo3LgPedR4VxnNE11TADdYeTlY7tkdKtSroW6vpLaO362h_19E83ijNZzjOtSiiPsEcXGEA"

POE54_HLD = "2_Software_Architectural_Design/POE54_SW_HLD_Name"
TRAINING = "SW/HLD Specs" 

# Format: "wiki/SW/HLD%20Specs"
POE54_HLD_PATH = "2_Software_Architectural_Design/POE54_SW_HLD_Name"
TRAINING_PATH = "SW/HLD Specs"

POE54_SPACE = "2_Software_Architectural_Design"
TRAINING_SPACE = "SW"

POE54_DOC_NAME = "POE54_SW_HLD_Name"
TRAINIG_DOC_NAME = "HLD Specs"

PROJ = "POE54"

if PROJ == "POE54" :
   SERVER_URL = SERVER_URL_ALM
   PROJECT_ID = POE54_ID
   TOKEN = TOKEN_ALM
   DOC_PATH = POE54_HLD
   SPACE_ID = POE54_SPACE
   DOC_PATH = POE54_HLD_PATH
   DOC_NAME = POE54_DOC_NAME
   
elif  PROJ == "TRAINING":
   SERVER_URL = SERVER_URL_ALM_DEV
   PROJECT_ID = TRAINING_ID
   TOKEN = TOKEN_ALMDEV
   DOC_PATH = TRAINING
   SPACE_ID = TRAINING_SPACE
   DOC_PATH = TRAINING
   DOC_NAME = TRAINIG_DOC_NAME

# Optional: ID of the heading you want this under (e.g., 'EL-123'). 
# If you don't have one yet, leave as None.
PARENT_ID = "PDPXMT-25252" 
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
    {
        "title": "J1939_SET_SPN_STALLFAULT",
        "function": "+ J1939_SET_SPN_STALLFAULT(value: bool): void",
        "desc": "Sets the stall fault status in the J1939 Pump Faults status message.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_LOWLOADOPERATION",
        "function": "+ J1939_SET_SPN_LOWLOADOPERATION(value: bool): void",
        "desc": "Updates the low load operation fault indication in the J1939 Pump Faults message.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_OVERCURRENT",
        "function": "+ J1939_SET_SPN_OVERCURRENT(value: bool): void",
        "desc": "Sets the overcurrent fault flag in the J1939 Pump Faults message.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_UNDERVOLTAGE",
        "function": "+ J1939_SET_SPN_UNDERVOLTAGE(value: bool): void",
        "desc": "Sets the undervoltage fault status for transmission via J1939.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_OVERVOLTAGE",
        "function": "+ J1939_SET_SPN_OVERVOLTAGE(value: bool): void",
        "desc": "Updates the overvoltage fault indication in the J1939 Pump Faults message.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_OVERTEMP",
        "function": "+ J1939_SET_SPN_OVERTEMP(value: bool): void",
        "desc": "Sets the overtemperature fault flag based on detected PCB overtemperature conditions.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_OVERTEMPDERATING",
        "function": "+ J1939_SET_SPN_OVERTEMPDERATING(value: bool): void",
        "desc": "Sets the overtemperature derating fault indication in the J1939 message.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_VOLATGEDRAFTING",
        "function": "+ J1939_SET_SPN_VOLATGEDRAFTING(value: bool): void",
        "desc": "Updates the voltage derating fault status for J1939 Pump Faults reporting.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_ERRORSHORTCIRCUIT",
        "function": "+ J1939_SET_SPN_ERRORSHORTCIRCUIT(value: bool): void",
        "desc": "Sets the short-circuit fault indication in the J1939 Pump Faults message.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_INTERNALFAULT",
        "function": "+ J1939_SET_SPN_INTERNALFAULT(value: bool): void",
        "desc": "Sets the internal fault status bit for J1939 Pump Faults transmission.",
        "severity": "must_have"
    },
    {
        "title": "J1939_SET_SPN_CANERROR",
        "function": "+ J1939_SET_SPN_CANERROR(value: bool): void",
        "desc": "Updates the CAN communication error flag in the J1939 Pump Faults message.",
        "severity": "must_have"
    }
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
                "role": "has_parent"  # Change to 'has_parent' if that is your system's ID
            },
            "relationships": {
                "workItem": {
                    "data": {
                        "id": _PARENT_ID,
                        "type": "heading"
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
    
    # Send the POST request with the new structured payload
    move_res = requests.post(move_url, headers=loc_headers, json=move_data, verify=False)

    
    if move_res.status_code in [200, 204]:
        print(f"+++ Successfully moved {new_wi_id} into Document.")
    else:
        print(f"!!! Move Failed (Status {move_res.status_code})")
        print(f"Response Body: {move_res.text}")
        
def wi_link(wi_id, style="long"):
    """Generates the Polarion HTML span for a Work Item link."""
    return f'<span class="polarion-rte-link" data-type="workItem" data-item-id="{wi_id}" data-option-id="{style}"></span>'

def process_requirement_text(raw_text, source_lists):
    if isinstance(source_lists, dict):
        source_lists = [source_lists]

    lookup = {}
    for item in source_lists:
        if isinstance(item, dict):
            title = item.get('attributes', {}).get('title')
            wi_id = item.get('id')
            if title and wi_id:
                lookup[title] = wi_id

    def replacement(match):
        title = match.group(1)
        if title in lookup:
            raw_id = lookup[title].split('/')[-1]
            return f'<span class="polarion-rte-link" data-type="workItem" data-item-id="{raw_id}" data-option-id="long">{title}</span>'
        return match.group(0)

    # Use 'raw_text' as defined in the function header above
    return re.sub(r'\{([^}]+)\}', replacement, raw_text)
        
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
    parameterList = get_workitemList(doc_url, "parameter", headers)
    
    interface1 = interfaceList[0]
    interface1_id = interface1['id'].split('/')[-1] # e.g., 'PDPXMT-25234'
    print(f"parameterList len: {len(parameterList)}")
    #raw_text = "SWC2 shall provide interface3 with false when {SWC_init} this is parameter {SWC_Param1} is true another interface {ACOM_SpdFbPwmHz_Get} also another param {SWC_Param1}"
    raw_text = [
        "COMH shall collect motor error information by calling {MCMD_MCTL_ERRORS_GET} during execution of {COMH_UpdateFaultsMessage}. COMH shall collect application error information by calling {APMD_APPL_ERRORS_GET} during execution of {COMH_UpdateFaultsMessage}. COMH shall collect hardware driver error information by calling {HWMD_HWDD_ERRORS_GET} during execution of {COMH_UpdateFaultsMessage}.",
        "COMH shall set the Over‑Temperature sticky fault bit. If motor errors indicate a stall condition, COMH shall set the Stall Fault sticky fault bit. If motor errors indicate a low‑load condition, COMH shall set the Low‑Load Operation sticky fault bit. If application errors indicate a voltage derating condition, COMH shall set the Voltage Derating sticky fault bit. If application errors indicate PCB over‑temperature speed degradation, COMH shall set the Over‑Temperature Derating sticky fault bit. If application errors indicate an undervoltage condition, COMH shall set the Undervoltage sticky fault bit. If application errors indicate an overvoltage condition, COMH shall set the Overvoltage sticky fault bit. If motor errors indicate an over‑current condition, COMH shall set the Over‑Current sticky fault bit.",
        "COMH shall check whether the transmit push‑to‑queue operation is confirmed by calling {J1939_GetTxPushToQueueConfirmedFlag}. COMH shall update Pump Faults SPNs only if {J1939_GetTxPushToQueueConfirmedFlag} indicates a confirmed transmit operation.",
        "COMH shall update Pump Faults SPNs by calling the following interfaces using the corresponding sticky fault bits:{J1939_SET_SPN_STALLFAULT}{J1939_SET_SPN_LOWLOADOPERATION}{J1939_SET_SPN_OVERCURRENT}{J1939_SET_SPN_UNDERVOLTAGE}{J1939_SET_SPN_OVERVOLTAGE}{J1939_SET_SPN_OVERTEMP}{J1939_SET_SPN_OVERTEMPDERATING}{J1939_SET_SPN_VOLATGEDRAFTING}{J1939_SET_SPN_ERRORSHORTCIRCUIT}{J1939_SET_SPN_INTERNALFAULT}{J1939_SET_SPN_CANERROR}.",
        "COMH shall Transmit Confirmation Reset after Pump Faults SPN update and sticky fault clearing, COMH shall clear the transmit confirmation flag by calling {J1939_SetTxPushToQueueConfirmedFlag}."
    ]
    
    polTxtP = process_requirement_text(raw_text[3], interfaceList+parameterList)

#     # Define the new description text using Polarion Wiki Markup for a link
#     new_desc_text = (
#         "SWC2 shall provide interface1 with false when "
#         f"{wi_link(interface1_id)} " # This creates the visual link
#         "param1 is true"
#     )
#     print(f"req description: {new_desc_text}")
    req_data['data'][0]['attributes']['description']['value'] = polTxtP
    req_data['data'][0]['attributes']['title'] = polTxtP
#     
    # CREATING list of INTERFACES
    #for wi in inter_data_list:
    create_n_move(SERVER_URL, PROJECT_ID, safe_space, DOC_NAME, PARENT_ID, req_data, doc_url, headers)
        #create_n_move(SERVER_URL, PROJECT_ID, safe_space, DOC_NAME, PARENT_ID, fill_list(wi, "interface"), doc_url, headers)
    
    #TODO: if parent does not exist in document then dont create workitem
