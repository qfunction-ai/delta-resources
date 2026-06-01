import os
from falconpy import Alerts
import json

def get_crowdstrike_alerts():
    """
    Connects to CrowdStrike using falconpy and retrieves all current alerts 
    by handling pagination through the get_alerts_combined API.
    """
    try:
        # Access credentials from environment variables
        creds = json.loads(os.getenv("CREDENTIAL_CROWDSTRIKE_KEYS"))
        client_id = creds.get("primary_key", "")
        client_secret = creds.get("secondary_key", "")
        
        if not client_id or not client_secret:
            return "Error: CrowdStrike API credentials (CLIENT_ID and CLIENT_SECRET) are not set in the environment variables."

        # Initialize the Alerts client
        falcon = Alerts(client_id=client_id, client_secret=client_secret)
        
        all_alerts = []
        after_token = None
        page_count = 0

        response = falcon.get_alerts_combined(
                filter="",
                limit=1000,
                sort="created_timestamp|desc"
        )

        return response
        
    except Exception as e:
        return f"An error occurred while fetching alerts: {e}"
