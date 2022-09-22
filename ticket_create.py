import requests
from constants import *

def create_ticket(hostname):

    url = f"{SERVER_URL}/api/v1/ticket-notify/helpdesk.ticket"

    payload = {
        "name": hostname + " Ticket Test1",
        "team_id": 1,
        "description": "Core Device " + hostname + " is down",
        "active": True,
        "ticket_type_id": 2,
        "color": 1,
        "user_id": 2,
        "partner_id": 47,
        "tag_ids": [
            3
        ],
        "is_self_assigned": True,
        "partner_name": "Telecontract",
        "partner_email": "pr@telco.co.zw",
        "closed_by_partner": True,
        "email": "pr@telco.co.zw",
        "priority": "2",
        "stage_id": 1,
        "email_cc": "",
        "rating_ids": [0]
        
    }


    response = requests.request("POST", url, json=payload, headers=ticket_headers, verify=False)

    print(response.text)


# print(create_ticket('UCRM3'))