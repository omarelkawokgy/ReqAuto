import requests
import json
import urllib.parse
#from get_pol_doc import get_polarion_document
#from get_wi_list import get_workitemList
from ReadFromSheet import get_work_records

# --- SETTINGS ---
SERVER_URL = "https://alm.mahle/polarion/rest/v1"
PROJECT_ID = "PDPXMT"
TOKEN_ALM = "eyJraWQiOiI0MzFiODM3Mi0wYTkxNjM1Mi03ODJjMDc2ZS04ZDg5NzJkNiIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiMjk5ZDM5MGItMGE5MTYzNTItNjE2YWVjNjQtNGIzMmU1ZmMiLCJleHAiOjE4NjA4MzMyNjIsImlhdCI6MTc3NDUxOTY2Mn0.hir2Qc3dylPKkSqYdkmuOGspPmZYOieZNIsTM9Z-zaVj7V-uzaM0Tsoi3pHdv3ZA8pR6S6xcNWdLjj1dAfKIYhx0p05cwWnUHpYa1RrfQQPTSIrEfCR77jbRG9udWOgZVrUxSpm0ARJhRql5eitcobVSRmg9Lqa8jn27zhpuWP3af4ZpfgVschjE2dDmYXK_zy_XkObfKsuQBGEiT6Au0WyoVi7qRr6UhzxTLQDA70AqqoiPVUq251vWn5b7hBdwouSZsh3RTaBa7gHSo3LgPedR4VxnNE11TADdYeTlY7tkdKtSroW6vpLaO362h_19E83ijNZzjOtSiiPsEcXGEA"
TOKEN = TOKEN_ALM

TASK_ID = "PDPXMT-23815"

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json', 
    'Accept': 'application/json'
}

def addWorkRecord(_user, _date, _timeSpent, _type, _comment, _WrUrl, loc_headers):
    payload = {
        "data": [
            {
                "type": "workrecords",
                "attributes": {
                    "timeSpent": _timeSpent,  # Ensure standard format
                    "date": _date,
                    "comment": _comment,
                    "type": ""
                },
                "relationships": {
                    "user": {
                        "data": {
                            "type": "users",
                            "id": _user  # Replace with your User ID
                        }
                    }
                }
            }
        ]
    }
    
    task_wr_url = _WrUrl
              
    print(f"Requesting Document: {task_wr_url}")
    
    response = requests.post(task_wr_url, headers=loc_headers, data=json.dumps(payload), verify=False)
    
    if response.status_code == 201:
        print(f"Successfully added work record to {response}")
    
    else:
        print(f"Failed to add record. Status: {response.status_code}")
        print(f"Response: {response.text}")

def checkWorkRecordDuplicate(_user, _date, _timeSpent, _type, _comment, _url, loc_headers):

    url_WR = _url
    
    # 2. Use the @all keyword to force the API to send all attributes
    params = {
        f"fields[{'workrecords'}]": "@all"
    }
    
    # 1. Fetch existing work records
    response = requests.get(url_WR, headers=loc_headers, params=params, verify=False)
    if response.status_code != 200:
        print(f"Error fetching records: {response.text}")
        return

    existing_records = response.json().get('data', [])
    print(f"existing_records length:{len(existing_records)}")

    # 2. Check for duplicates
    for record in existing_records:
        attrs = record.get('attributes', {})
        rels = record.get('relationships', {})
        # Normalize Type: Treat None or empty string as a match
        existing_type = (attrs.get('type') or "").strip()
        target_type = (_type or "").strip()

        # Normalize TimeSpent: Remove 'h', 'm', and spaces to compare raw numbers
        def clean_time(t):
            return "".join(filter(str.isdigit, str(t))) if t else ""
        
        # Comparison Logic
        date_match = attrs.get('date') == _date
        user_match = rels.get('user', {}).get('data', {}).get('id') == _user
        
        # Use 'in' for comment to handle potential encoding/hidden char issues
        comment_match = _comment.strip() in (attrs.get('comment') or "")
        
        # Time match: Flexible check
        time_match = clean_time(attrs.get('timeSpent')) == clean_time(_timeSpent)

        if date_match and user_match and comment_match and time_match:
            return True

    return False

def checkNaddWorkRecord(_SERVER_URL, _PROJECT_ID, _TASK_ID, _user, _date, _timeSpent, _type, _comment, loc_headers):
    url_WR = f"{_SERVER_URL}/projects/{_PROJECT_ID}/workitems/{_TASK_ID}/workrecords"
    
    if checkWorkRecordDuplicate(_user, _date, _timeSpent, _type, _comment, url_WR, loc_headers) == False:
        addWorkRecord(_user, _date, _timeSpent, _type, _comment, url_WR, loc_headers)
        print(f"Successfully added work record to {_TASK_ID}")
    else:
        print(f"✅ Duplicate Found: Skipping record")    
        
if __name__ == "__main__":
    records_df = get_work_records(week_number=12)
    print(f"Fetched {len(records_df)} records.")
    
    #ret = checkNaddWorkRecord(SERVER_URL, PROJECT_ID, TASK_ID, "e0149968", "2026-01-14", "1h 1/3h", "", "Adding work record via script", headers)
    #print(f"{ret}")

    # 2. Convert DataFrame rows to dictionaries and iterate
    for record in records_df:        
        #if record['project_name'] == 'PXM010' and record['date'] == '2026-01-13':
        # 3. Call the Polarion REST function
        # Note: Ensure variables like SERVER_URL and user_id are defined in your scope
        ret = checkNaddWorkRecord(
            _SERVER_URL=SERVER_URL, 
            _PROJECT_ID=record['project_name'], 
            _TASK_ID=record['task_id'], 
            _user="e0149968", 
            _date=record['date'], 
            _timeSpent=str(record['hours']), 
            _type="", 
            _comment=record['task_des'], 
            loc_headers=headers
        )
        #print(f"Status for {task_id}: {ret}")
            
    #TODO: update the sheet with status of the task set it from sheet to polrion if needed
    #TODO: request update a certain week only instead of the whole sheet        
