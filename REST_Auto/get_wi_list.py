import requests
import json
import urllib.parse

# --- SETTINGS --- POE54
SERVER_URL = "https://alm.mahle/polarion/rest/v1"
PROJECT_ID = "61DE-62527"
TOKEN = "eyJraWQiOiI1ZjA2NWZmZC0wYTkxNGEzMC0wNWE0YjE4Yy1hNTQxMWYyNCIsInR5cCI6IkpXVCIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlMDE0OTk2OCIsImlkIjoiYzhjMmU1NGUtMGE5MTRhMzAtNzY5MjAyZDUtODM4NWNjOGIiLCJleHAiOjE4NTQ5MTMzNzQsImlhdCI6MTc2ODU5OTc3NH0.TpQf5YcwVx3GZ14KD6YMWU9AaXVF5mno4UvBQ61MNBmr1Y_5ltvCP8pnjbl9skFh2nsvzmR2sqYdb1HlLvjLJgdGTDpWdmN_X7pcRZkvg9QqQA6zgXXjKhTgA1Tp0A_ztQ_Umhr1D_HvI3AODf7vc84rBgzZhbAHVEk3vluXigKweyExEQZX7TiIl7BWZ2fbr1nLzCmdAv1dJfI3OFFf30rwbv4WXL6zt0sVWptbymVdTlA5TjcY-BKyg-bFTvV62hktMH3LhPQ0FqsNCkoYSPjKEPx7nLkwBD7MNC9ZvFkUIHDG3tzQOw2nL7IWVYAN2wxCyh2_bgFzkDZsRBFJuw" # (Your token)
# Format: "wiki/SW/HLD%20Specs"
DOC_PATH = "SW/HLD Specs" 
SPACE_ID = "1_Software_Requirements_Analysis"
DOC_NAME = "XCSP Target Parameters"
# Optional: ID of the heading you want this under (e.g., 'EL-123'). 
# If you don't have one yet, leave as None.
PARENT_ID = "PDPXMT-25253" 
SEVERITY = "should_have"

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json', 
    'Accept': 'application/json'
}

# def get_workitemList(_doc_url, _wi_type, loc_headers):
#   # The space and doc name should be raw (e.g. "SW" and "HLD Specs")
#   get_items_url = (_doc_url+f"/parts"
#   f"?include=workItem"
#   f"&fields[workitems]=type,title,id")
#   
#   print(f"get_items_url: {get_items_url}")
#   
#   response = requests.get(get_items_url, headers=loc_headers, verify=False)
#   print(f"DEBUG: Status Code Received: {response.status_code}") # Add this
#   if response.status_code == 200:
#       response_json = response.json()
#   
#       # Polarion REST (JSON:API) stores related objects in 'included'
#       included_objects = response_json.get('included', [])
#       print(f"DEBUG: Found {len(included_objects)} included_objects(s).")
#       
#       # Filter 'included' objects where the type is 'interface'
#       # In 2026, 'type' is typically an ID within the attributes
#       wi_list = [
#       obj for obj in included_objects 
#       if obj.get('type') == 'workitems' and obj.get('attributes', {}).get('type') == _wi_type
#       ]
#       print(f"\nTotal wi_list {_wi_type} collected: {len(wi_list)}")
#     
#       for obj in included_objects:
#         #Get the data inside attributes
#         attrs = obj.get('attributes', {})
#         obj_id = obj.get('id')
#         
#         #Get the specific Polarion Type (e.g., 'interface', 'requirement', 'heading')
#         polarion_type = attrs.get('type')
#         title = attrs.get('title', 'NO TITLE')
#         
#         print(f"--- Object ID: {obj_id} ---")
#         print(f"  Resource Type (API): {obj.get('type')}")
#         print(f"  Polarion Type (WorkItem): {polarion_type}")
#         print(f"  Title: {title}")
#   else:
#       print(f"Failed to fetch document items: {response.status_code}")
#   return wi_list

def get_workitemList(_doc_url, _wi_type, loc_headers):

    all_workitems = []
    # The space and doc name should be raw (e.g. "SW" and "HLD Specs")
    fetch_url = (f"{_doc_url}/parts"
                f"?include=workItem"
                f"&fields[workitems]=type,title,id")

    print(f"get_items_url: {fetch_url}")

    # Polarion uses 'page[offset]' and 'page[limit]' for pagination
    params = {'page[offset]': 0, 'page[limit]': 100} # Start at 0, fetch 100 items at a time

    while fetch_url:
        response = requests.get(fetch_url, headers=loc_headers, verify=False)
        if response.status_code != 200:
            print(f"Error fetching work items: {response.text}")
            break
            
        json_data = response.json()
        included_objects = json_data.get('included', [])
        
        wi_list = [
        obj for obj in included_objects 
        if obj.get('type') == 'workitems' and obj.get('attributes', {}).get('type') == _wi_type
        ]
        print(f"wi list size: {len(included_objects)}")
        all_workitems.extend(wi_list)
        
        # Check for the next link provided by the API (standard JSON:API practice)
        # This tells you if there is another page to fetch
        next_link = json_data.get('links', {}).get('next')
        
        if next_link:
            # If there's a next page, update the URL for the next iteration
            fetch_url = next_link
            params = {} # The 'next' link usually contains all necessary params already
        else:
            # No more pages, exit the loop
            fetch_url = None
            
        print(f"To Next page")
    return all_workitems

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
    
    test_connection(SERVER_URL, PROJECT_ID, headers)
    # URL encode IDs to handle spaces or special characters
    safe_space = urllib.parse.quote(SPACE_ID)
    safe_doc = urllib.parse.quote(DOC_NAME)
    
    # Endpoint: /projects/{projectId}/spaces/{spaceId}/documents/{documentName}
    doc_url = f"{SERVER_URL}/projects/{PROJECT_ID}/spaces/{safe_space}/documents/{safe_doc}"
    
    param_list = get_workitemList(doc_url, "parameter", headers)
    print(f" Fetching finished items: {len(param_list)}")
    
    for param in param_list:
        # Safely access the title from the nested attributes
        title = param.get('attributes', {}).get('title', "")
        
        if "LOGIC" in title:
            titleTxt = title.split()[0]
            print(f"{titleTxt} OR ")
    
