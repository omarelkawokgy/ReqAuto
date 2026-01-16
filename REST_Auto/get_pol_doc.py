import requests
import json
import urllib.parse

def get_polarion_document(_doc_url, loc_headers):
    """
    Accesses a specific Polarion LiveDoc and prints its metadata.
    """
    try:
        response = requests.get(_doc_url, headers=loc_headers, verify=False)
        
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