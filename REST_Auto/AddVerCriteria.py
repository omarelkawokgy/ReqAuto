################# Add Verification criteria to requirements ####################
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
    'Accept': 'application/json',
    "If-Match": "*"
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

def get_existing_verification(wi_url, headers):
    r = requests.get(wi_url, headers=headers, verify=False)
    r.raise_for_status()
    attrs = r.json()["data"]["attributes"]

    vc = attrs.get("ver_criteria")
    if not vc:
        return []

    # split by line breaks (your chosen separator)
    return [x.strip() for x in vc["value"].split("<br/>") if x.strip()]

def merge_verification(existing, new_items):
    merged = existing.copy()
    for item in new_items:
        if item not in merged:
            merged.append(item)
    return merged

def update_verification(wi_id, verText, headers):

    payload = {
        "data": {
            "type": "workitems",
            "id": f"{PROJECT_ID}/{wi_id}",
            "attributes": {
                "ver_criteria": {                 # ✅ correct field
                    "type": "text/plain",          # ✅ OBJECT required
                    "value": verText
                }
            }
        }
    }

    url = f"{SERVER_URL}/projects/{PROJECT_ID}/workitems/{wi_id}"
    
    print("URL WAS:", url)
    print("PAYLOAD ID:", payload["data"]["id"])
    
    r = requests.patch(
        url,
        data=json.dumps(payload),
        headers=headers,
        verify=False
    )
    r.raise_for_status()
    
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

   
if __name__ == "__main__":
    # URL encode IDs to handle spaces or special characters
    safe_space = urllib.parse.quote(SPACE_ID)
    safe_doc = urllib.parse.quote(DOC_NAME)
    
    test_connection(SERVER_URL, PROJECT_ID, headers)
    
    wi_id = "61DE-62527-74509"
    wi_url = f"{SERVER_URL}/projects/{PROJECT_ID}/workitems/{wi_id}"
    
    verification_data = [
        {
            "wi_id": "61DE-62527-74369",
            "ver_criteria": (
                "During UpdateFaultsMessage execution, verify COMH calls XCSP-39928, "
                "XCSP-40459, and XCSP-38489 and correctly stores the returned error information."
            )
        },
        {
            "wi_id": "61DE-62527-74500",
            "ver_criteria": (
                "Verify COMH updates CAN status by calling each specified J1939_SET_SPN interface "
                "with correct scaling and published values observable on the CAN network."
            )
        },
        {
            "wi_id": "61DE-62527-74386",
            "ver_criteria": (
                "Verify COMH updates all listed Pump Fault SPNs using the defined J1939_SET_SPN "
                "interfaces and clears all sticky fault bits after the update cycle."
            )
        },
        {
            "wi_id": "61DE-62527-74131",
            "ver_criteria": (
                "Verify ECUM ROM and RAM usage does not exceed the limits defined by "
                "61DE-62527-74132 and 61DE-62527-74133 using memory analysis reports."
            )
        },
        {
            "wi_id": "61DE-62527-72999",
            "ver_criteria": (
                "Verify MAIN ROM and RAM usage remains within the limits defined by "
                "61DE-62527-73000 and 61DE-62527-73001 based on compiled memory reports."
            )
        },
        {
            "wi_id": "61DE-62527-69032",
            "ver_criteria": (
                "Verify CANM reports CAN active when 61DE-62527-67440 returns TRUE and provides "
                "the operational state via 61DE-62527-67474."
            )
        },
        {
            "wi_id": "61DE-62527-72548",
            "ver_criteria": (
                "Verify CANM evaluates the mode via 61DE-62527-72560 and calls 61DE-62527-72558 "
                "with EOL_MODE configuration when the evaluated mode is EOL_MODE."
            )
        },
        {
            "wi_id": "61DE-62527-68978",
            "ver_criteria": (
                "Verify CANM executes cyclic CAN processing after initialization via "
                "61DE-62527-67714 using 61DE-62527-67438 as the execution context."
            )
        },
        {
            "wi_id": "61DE-62527-68982",
            "ver_criteria": (
                "Verify CANM extracts the CAN speed request and provides the RPM value through "
                "61DE-62527-67472 during cyclic CAN processing."
            )
        },
        {
            "wi_id": "61DE-62527-72556",
            "ver_criteria": (
                "Verify CANM initializes the J1939 Application layer by calling "
                "61DE-62527-72542 during system initialization."
            )
        },
        {
            "wi_id": "61DE-62527-72546",
            "ver_criteria": (
                "Verify CANM initializes the J1939 Data Link layer by calling "
                "61DE-62527-72541 as part of CAN stack initialization."
            )
        },
        {
            "wi_id": "61DE-62527-72555",
            "ver_criteria": (
                "Verify CANM initializes the J1939 Data Transfer layer by calling "
                "61DE-62527-72538 during startup sequencing."
            )
        },
        {
            "wi_id": "61DE-62527-72553",
            "ver_criteria": (
                "Verify CANM initializes the J1939 Diagnostics layer by calling "
                "61DE-62527-72544 once preceding layers are initialized."
            )
        },
        {
            "wi_id": "61DE-62527-72552",
            "ver_criteria": (
                "Verify CANM initializes the J1939 ECU address by calling 61DE-62527-72559 "
                "using the parameter provided by 61DE-62527-72561."
            )
        },
        {
            "wi_id": "61DE-62527-72550",
            "ver_criteria": (
                "Verify CANM initializes the J1939 Memory Access layer by calling "
                "61DE-62527-72539 during CAN stack setup."
            )
        },
        {
            "wi_id": "61DE-62527-72557",
            "ver_criteria": (
                "Verify CANM initializes the J1939 Transport layer by calling "
                "61DE-62527-72543 as part of initialization."
            )
        },
        {
            "wi_id": "61DE-62527-72547",
            "ver_criteria": (
                "Verify CANM initializes the message handler by calling "
                "61DE-62527-72545 after transport layer initialization."
            )
        },
        {
            "wi_id": "61DE-62527-68987",
            "ver_criteria": (
                "Verify CANM periodically updates 61DE-62527-67472 and 61DE-62527-67473 "
                "during execution of 61DE-62527-67714."
            )
        },
        {
            "wi_id": "61DE-62527-68976",
            "ver_criteria": (
                "Verify CANM blocks CAN influence when 61DE-62527-67440 returns FALSE and "
                "reports CAN inactive status via 61DE-62527-67474."
            )
        },
        {
            "wi_id": "61DE-62527-68984",
            "ver_criteria": (
                "Verify CANM provides a valid speed via 61DE-62527-67472 only when "
                "61DE-62527-67440 returns TRUE, otherwise providing an invalid value (-1)."
            )
        },
        {
            "wi_id": "61DE-62527-72549",
            "ver_criteria": (
                "Verify CANM reconfigures the hardware filter via 61DE-62527-72558 using "
                "the node address from 61DE-62527-72559 when not in EOL mode."
            )
        },
        {
            "wi_id": "61DE-62527-69007",
            "ver_criteria": (
                "Verify CANM retrieves ENABLE via 61DE-62527-69012, interprets 0/1 as FALSE/TRUE, "
                "and stores the result in 61DE-62527-67473."
            )
        },
        {
            "wi_id": "61DE-62527-69006",
            "ver_criteria": (
                "Verify CANM retrieves SPEED_COMMAND via 61DE-62527-69013, scales it using "
                "61DE-62527-72649, and stores the RPM in Speed_Request."
            )
        },
        {
            "wi_id": "61DE-62527-68993",
            "ver_criteria": (
                "Verify CANM sets 61DE-62527-67426 to FALSE upon reception of any valid CAN "
                "message via the CAN_Message_IN buffer."
            )
        },
        {
            "wi_id": "61DE-62527-68992",
            "ver_criteria": (
                "Verify CANM sets 61DE-62527-67426 to TRUE when no valid CAN message is received "
                "within the timeout defined by 61DE-62527-72648."
            )
        },
        {
            "wi_id": "61DE-62527-72551",
            "ver_criteria": (
                "Verify CANM updates the stack status to STACK_DETECTED by calling "
                "61DE-62527-72540."
            )
        },
        {
            "wi_id": "61DE-62527-68988",
            "ver_criteria": (
                "Verify CANM sets 61DE-62527-67426 to TRUE whenever the Communication_Timeout_Detect "
                "flag is active."
            )
        },
        {
            "wi_id": "61DE-62527-69009",
            "ver_criteria": (
                "Verify CANM writes the actual battery voltage from 61DE-62527-69030 to the CAN "
                "transmit buffer using 61DE-62527-67432."
            )
        },
        {
            "wi_id": "61DE-62527-69002",
            "ver_criteria": (
                "Verify CANM writes the actual battery supply current from 61DE-62527-67434 "
                "to the CAN transmit buffer using 61DE-62527-69027."
            )
        },
        {
            "wi_id": "61DE-62527-69008",
            "ver_criteria": (
                "Verify CANM writes the actual system speed from 61DE-62527-67445 to the CAN "
                "transmit buffer using 61DE-62527-69025."
            )
        },
        {
            "wi_id": "61DE-62527-69003",
            "ver_criteria": (
                "Verify CANM writes the system temperature from 61DE-62527-67430 to the CAN "
                "transmit buffer using 61DE-62527-69018."
            )
        },
        {
            "wi_id": "61DE-62527-69004",
            "ver_criteria": (
                "Verify CANM maps each listed error status flag from application interfaces "
                "to the corresponding CAN transmit signals as specified."
            )
        }
    ]
    for item in verification_data:
        # 3️⃣ Update work item
        update_verification(item["wi_id"], item["ver_criteria"], headers)
        print("✅ Verification criteria updated successfully")
    
    
    
#################### AI Prompt ######################
#     using this excel sheet give python code list with each item containing element for the id and element for the verification criteria text
#     verification criteria specification:
#     write the verification criteria suitable for swe5 make it specific for each requirement avoid generic criteria try to use interfaces parameters and word mentioned in the requirement itself. Also do not exceed 2 lines of text otherwise it ll be overkill
# 
#     and this is how i ll use it in code
#         for item in verification_data:
#             # 3️⃣ Update work item
#             update_verification(item["wi_id"], item["ver_criteria"], headers)
#             print("✅ Verification criteria updated successfully")
