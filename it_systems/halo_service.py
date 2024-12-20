import requests 
import os
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()
URL = os.getenv('HALO_API_URL')


# Get HaloPSA OAuth2 Access token
def get_halo_token():
    """ Fetches an access token from HaloPSA. """
    
    # Getting credentials 
    consumer_url=os.getenv('HALO_AUTH_URL')
    client_id=os.getenv('HALO_CLIENT_ID')
    client_secret=os.getenv('HALO_CLIENT_SECRET') 
    
   # Preparing request payload
    payload = {
       "client_id": client_id,
       "client_secret": client_secret,
       "grant_type": "client_credentials",
       "scope": "all"
   }
    
    try: 
        # Making the request to fetch the token
        response = requests.post(consumer_url, data=payload)
        if response.status_code == 200:
            token_data = response.json()
            
            #Extracting the access token from the api response
            # print(token_data.get("access_token"))
            return token_data.get("access_token")
        else:
            print(f"Failed to fetch token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"An error ocurred: {str(e)}")
        return None

# Getting HaloPSA Agent details
def get_halo_agent_details(agent_id):
    """Fetch details of an agent assigned to a ticket."""
    access_token = get_halo_token()
    if not access_token:
        return {"error": "Failed to fetch access token"}

    # Construct the endpoint URL for fetching agent details
    agent_url = f"https://jarvis.techary.com/api/Agent/{agent_id}" 
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(agent_url, headers=headers)

        # Handle successful response
        if response.status_code == 200:
            agent_data = response.json()

            # Extract and format specific agent details
            agent_info = {
                "id": agent_data.get("id"),
                "name": agent_data.get("name"),
                "job_title": agent_data.get("jobtitle"),
                "email": agent_data.get("email"),
                # "online_status": agent_data.get("lastonline"),
                # "teams": [team.get("team_name") for team in agent_data.get("teams", [])],
                # "photo_path": agent_data.get("agentphotopath"),
                # "initials": agent_data.get("initials")
            }

            return agent_info  # Return formatted agent information

        else:
            # Handle unsuccessful status codes
            return {"error": f"Failed to fetch agent details (Status Code: {response.status_code})"}

    except Exception as e:
        # Handle exceptions such as network errors
        return {"error": "An error occurred while fetching agent details", "details": str(e)}

    
    
def get_client_details(client_name):
    """Fetching client ID in HaloPSA for a given client name. """
    
    # Getting HaloPSA OAuth2 access token
    access_token = get_halo_token()
    if not access_token:
        return {"error": "Failed to fetch access token"}
    
    # Building the endpoint URL for fetching client details
    agent_url = f"https://jarvis.techary.com/api/Client/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    params = {"search": client_name}
    
    try:
        response = requests.get(agent_url, headers=headers, params=params)
        
        #Handle successful response
        if response.status_code == 200:
            client_data = response.json()
            clients = client_data.get("clients", [])
            
            if clients:
                # Assuming the first client match is the right one
                return clients[0].get("id")
            else:
                return {"error": "No clients found matching the provided name."}
        else:
            # Handle unsuccessful status codes
            return {"error": f"Failed to fetch agent details (Status Code: {response.status_code})"}
    except Exception as e:
        # Handle exceptions such as network errors
        return {"error": "An error occurred while fetching agent details", "details": str(e)}
    

get_halo_token()