import requests
import json
from constants import *

# USER='odoo-dev'
# KEY='d3649c6f-d450-4899-872f-16004be9451f'

def get_service_idz():

    pop1 = "VainonaPOP"
    pop="Dependency_Notify_Test"
    url = f"https://icinga0.telco.co.zw:5665/v1/objects/hosts?filter=\"{pop}\" in host.groups"

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic cm9vdDpmYTk4ODE4ODlmNjhlOTFh'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    k=json.dumps(response.json(),indent=2, sort_keys=True)
    # print(type(k))
    li=json.loads(k)
    count=0
    try:
        for i in range(len(li['results'])):
            z=li['results'][i]['attrs']['vars']
            if z:
                if "Service_ID" in z:
                    client_service_id = z['Service_ID']
                    print(client_service_id)
                    print(li['results'][i]['attrs']['address'],li['results'][i]['attrs']['name'],z['Service_ID'])
                    count= count +1
                    print(count)
                    anaytic_id = get_subscription_id(client_service_id)
                    print(anaytic_id)
                    subscription = get_subscription_params(anaytic_id)
                    print(subscription)
                    partner_det = get_partner_details(subscription)
                    print(partner_det)
                    print()
                    print('**************')
                    

    except Exception as e:
        print(e)
        pass


def get_subscription_id(service_id):
    try:
        url = f"{SERVER_URL}/{BASE_PATH}/sale.subscription.line/call/search"
        data = {
                "args": [[["service_id", "=", service_id]]]
            }

        response = requests.patch(url=url, json=data, headers=headers, auth=(USER, KEY))
        response_data = json.dumps(response.json(),indent=2, sort_keys=True)
        payload_data=json.loads(response_data)
        analytic_account_id = payload_data[0]

        return analytic_account_id 

    except Exception as e:
        print(e)
        pass


def get_subscription_params(analytic_account_id):
    try:
        url = f"{SERVER_URL}/{BASE_PATH}/sale.subscription/"

        payload = ""
        
        url_enco = url + str(analytic_account_id)
        response = requests.request("GET", url_enco, data=payload, headers=headers1)

        response_data = json.dumps(response.json(),indent=2, sort_keys=True)
        payload_data=json.loads(response_data)
        partner_id = payload_data['partner_id']

        return partner_id

    except Exception as e:
        print(e)
        pass


def get_partner_details(partner_id):

    try:
        url = f"{SERVER_URL}/{BASE_PATH}/res.partner/"

        params=[]
        payload = ""
        
        url_enco = url + str(partner_id)
        response = requests.request("GET", url_enco, data=payload, headers=headers1)

        response_data = json.dumps(response.json(),indent=2, sort_keys=True)
        payload_data=json.loads(response_data)
        partner_phone = payload_data['phone']
        partner_mobile = payload_data['mobile']
        if partner_mobile:
            params.append(partner_mobile)

        elif partner_phone and partner_mobile == None:
            params.append(partner_phone)
        
        else:
            print('contact has no details')

        return params[0]
    
    except Exception as e:
        print(e)
        pass



def postData(url, data):
    try:
        return requests.post(url=url, json=data, headers=header1, auth=(USER, KEY))

    except Exception as e:

        raise Exception(f" -> (postData) -> {e}")


def getData(url):

    try:
        return requests.get(url=url, auth=(USER, KEY))

    except Exception as e:

        raise Exception(f" -> (getData) -> {e}")


def patchRequest(url, data):
    try:
        return requests.patch(url=url, json=data, headers=header, auth=(USER, KEY))

    except Exception as e:

        raise Exception(f" -> (patchData) -> {e}")

    
# print(get_service_idz())
# print(get_subscription_id("SUB005-GENERIC-00"))
# print(get_subscription_params(4))
# print(get_partner_details(43))