"""
POLARION LIVEDOC METADATA RETRIEVER
-----------------------------------
Purpose:
    Retrieves and displays high-level metadata for a specific Polarion LiveDoc 
    using the REST API. This is typically used to verify a document's existence 
    and extract its unique System ID or URI before performing more intensive 
    operations like item extraction or updates.
    
    CHECKS CONNECTION TO DOCUMENT AND ITS EXISTANCE

Functionality:
    - Performs an HTTP GET request to the specific Document resource endpoint.
    - Parses the JSON:API response to extract the 'attributes' and 'links' objects.
    - Outputs the Document Title (as seen in the UI), the Internal ID (UUID), 
      and the REST API Self-Link (URI).

Inputs:
    - _doc_url (str): The fully qualified REST URL for the document 
      (e.g., .../spaces/{spaceId}/documents/{docName}).
    - loc_headers (dict): Authorization headers containing the Bearer Token.

Returns:
    - The JSON data object if successful, or None if the request fails.
"""
    
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