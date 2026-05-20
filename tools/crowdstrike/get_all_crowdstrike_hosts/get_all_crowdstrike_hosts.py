import os
from falconpy import Hosts
import json

def query_all_hosts_falconpy():
    """
    Connects to CrowdStrike Falcon via falconpy to query all hosts and returns a list of their hostnames and device IDs.
    
    Returns:
        dict: The response from the query_devices_by_filter_combined() method
    """
    try:
        # Access credentials from environment variables
        creds = json.loads(os.getenv("CREDENTIAL_CROWDSTRIKE_KEYS"))
        client_id = creds.get("primary_key", "")
        client_secret = creds.get("secondary_key", "")
        
        if not client_id or not client_secret:
            return {"error": "Falcon credentials (CLIENT_ID and CLIENT_SECRET) are not set in the environment variables."}

        # Initialize the Hosts client
        falcon = Hosts(client_id=client_id, client_secret=client_secret)

        #Retrieve the CrowdStrike hosts
        response = falcon.query_devices_by_filter_combined()

        return response
        
    except Exception as e:
        return {"error": f"An unexpected error occurred during the Falcon API call: {str(e)}"}
