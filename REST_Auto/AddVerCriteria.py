################# Add Verification criteria to requirements ####################
################# Add mandatory interface attributes also ######################
import re
import requests
import json
import urllib.parse
import pandas as pd
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
    
def update_interface_attributes(wi_id, if_unit, def_val, if_min, if_max, headers):
    payload = {
        "data": {
            "type": "workitems",
            "id": f"{PROJECT_ID}/{wi_id}",
            "attributes": {
                "unit": if_unit,
                "value": def_val,         # ✅ STRING or number
                "lowerLimit": if_min,     # ✅ STRING or number
                "upperLimit": if_max      # ✅ STRING or number
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
    
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)   # ✅ THIS IS CRITICA

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


def guess_attributes(name: str):
    n = name.upper()

    if any(k in n for k in [
        "FLAG", "ENABLE", "ERROR", "FAULT", "STATUS",
        "STALL", "OVER", "UNDER", "DERATING", "WARNING"
    ]):
        return "Boolean", "0", "0", "1"

    if "VOLT" in n or "VBAT" in n or "VDC" in n or "VLOGIC" in n:
        return "V", "0", "0", "17"

    if "CURRENT" in n or "IBAT" in n:
        return "A", "0", "0", "50"

    if "TEMP" in n:
        return "°C", "0", "-40", "125"

    if "SPEED" in n or "RPM" in n:
        return "RPM", "0", "0", "2000"

    if "TIME" in n:
        return "ms", "0", "0", "32700"

    return "UInt16", "0", "0", "65535"

   
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
        }
    ]
    
    
    
#     for item in interfaceAttribute:
#         update_interface_attributes(
#             wi_id=item["wi_id"],
#             if_unit=item["if_unit"],
#             def_val=item["def_val"],
#             if_min=item["if_min"],
#             if_max=item["if_max"],
#             headers=headers
#         )
#         print("✅ Interface attributes updated successfully")

# Keep only Interface items

# Load Excel
    xf = pd.ExcelFile("C:\Mahle\AUX_Archi\ReqAuto\REST_Auto\workitems (33).xlsx", engine="openpyxl")
    df = xf.parse(xf.sheet_names[0])

    # Normalize column names
    cols = {c.lower(): c for c in df.columns.astype(str)}
    id_col = cols["id"]
    title_col = cols["title"]
    type_col = cols["type"]
    
    
    print(f"ID column name: {id_col}")
    print(f"Title column name: {title_col}")
    print(f"Type column name: {type_col}")

    iface = df[df[type_col].str.lower() == "interface"].copy()
    iface["wi_id"] = iface[id_col].astype(str).str.split("/").str[-1]
    interfaceAttribute = []
    for _, row in iface.iterrows():
        print(str(row[title_col]))
        unit, dv, mn, mx = guess_attributes(str(row[title_col]))
        interfaceAttribute.append({
            "wi_id": row["wi_id"],
            "if_unit": unit,
            "def_val": dv,
            "if_min": mn,
            "if_max": mx
        })
    
    print(f"Total interface items: {len(interfaceAttribute)}")
    
    for item in interfaceAttribute:
        update_interface_attributes(
            wi_id=item["wi_id"],
            if_unit=item["if_unit"],
            def_val=item["def_val"],
            if_min=item["if_min"],
            if_max=item["if_max"],
            headers=headers
        )
        print("✅ Interface attributes updated successfully")


#     for item in verification_data:
#         # 3️⃣ Update work item
#         update_verification(item["wi_id"], item["ver_criteria"], headers)
#         print("✅ Verification criteria updated successfully")
    
    
    
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
