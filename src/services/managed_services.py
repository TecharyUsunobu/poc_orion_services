from flask import jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class ManagedServices:
    def __init__(self):
        self.base_url = os.getenv('HALO_API_URL')
        self.auth_url = os.getenv('HALO_AUTH_URL')
        self.client_id = os.getenv('HALO_CLIENT_ID')
        self.client_secret = os.getenv('HALO_CLIENT_SECRET')
        
    def get_halo_token(self):
        """Fetches an access token from the HaloPSA API"""
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
            "scope": "all"
        }
        try:
            response = requests.post(self.auth_url, data=payload)
            if response.status_code == 200:
                token_data = response.json()
                return token_data.get('access_token')
            else:
                print(f"Failed to fetch token: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None
        
        
    def get_client_details(self, client_name):
        """Fetch client ID in HaloPSA for a given client name."""
        access_token = self.get_halo_token()
        if not access_token:
            return {"error": "Failed to fetch access token"}

        client_url = f"{self.base_url}/Client/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        params = {"search": client_name}

        try:
            response = requests.get(client_url, headers=headers, params=params)
            if response.status_code == 200:
                client_data = response.json()
                clients = client_data.get("clients", [])
                if clients:
                    return clients[0].get("id")
                else:
                    return {"error": "No clients found matching the provided name."}
            else:
                return {"error": f"Failed to fetch client details: {response.text}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
        
        
        
    def get_halo_agent_details(self, agent_id):
        """Fetch details of an agent assigned to a ticket."""
        access_token = self.get_halo_token()
        if not access_token:
            return {"error": "Failed to fetch access token"}
        
        agent_url = f"{self.base_url}Agent/{agent_id}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        try: 
            response = requests.get(agent_url, headers=headers)
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
                return {"error": f"Failed to fetch agent details: {response.text}"}
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}
        
    
    def get_tickets_for_techary(self, client_name, ticket_category):
        """Fetch tickets from HaloPSA using the access token."""
        client_id = self.get_client_details(client_name)
        if isinstance(client_id, dict) and client_id.get("error"):
            return {"error": "Failed to fetch client details", "details": client_id}

        access_token = self.get_halo_token()
        if not access_token:
            return {"error": "Failed to fetch access token"}

        tickets_url = f"{self.base_url}/Tickets"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        query_params = {
            "client_id": client_id,
            "page_size": 50,
            "page_no": 2,
            "order": "ticket_id",
            "open_only": True,
            "search": ticket_category,
        }

        try:
            response = requests.get(tickets_url, headers=headers, params=query_params)
            if response.status_code == 200:
                ticket_response = response.json()
                ticket_list = ticket_response.get("tickets", [])
                for ticket in ticket_list:
                    ticket["assigned_agent"] = self.get_halo_agent_details(ticket.get('agent_id'))
                
                return {"tickets": ticket_list, "total_open_tickets": len(ticket_list)}
            else:
                return {"error": "Failed to fetch tickets", "details": response.text}
        except Exception as e:
            return {"error": "An error occurred while fetching tickets", "details": str(e)}
        

