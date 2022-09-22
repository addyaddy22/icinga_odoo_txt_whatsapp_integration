from flask import Flask, request, abort, Response
import logging
import time
import requests, json
import xmlrpc.client
from constants import *
import flask
from send_message import *
from datetime import datetime
from whtsap_functions import *
from ticket_create import *

app = flask.Flask(__name__)


info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(SERVER_URL))
print(common.version())

uid = common.authenticate(DB_NAME, USERNAME, PASSWORD, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(SERVER_URL))

@app.route('/', methods=['GET'])
def running():
    return ' Server is Running'

@app.route('/webhook', methods=['POST'])
def respond():
    res=request.json
    print(res)
    print(res['alert_source'],  res['notification_type'],  res['hostname'], res['data']['host_state'], res['data']['Service_ID'],  res['data']['host_output'][:-20], res['data']['host_address'])
    print(type(res))
    print(res)
    print("*******************")
    check=res['data']['Service_ID']
    print(check)
    # s_id="CS5426-VEL-FIR-MRR-01"
    # partner=get_partner_id(s_id)
    pe_group = res['data']['host_groups']
    if res['notification_type']=="PROBLEM":
        print('This is a Problem')
        print(pe_group)
        print(type(pe_group))
        group_list = pe_group.split(";")
        print(type(group_list))
        print(group_list)
        for i in range(len(group_list)):
            if 'POP' in group_list[i]:
                user_pop=group_list[i]
                print(user_pop)
                print(user_pop)        
                send_notify = get_service_idz(user_pop)
                print(send_notify)
                if send_notify == 'OK':   
                    url1 = 'https://icinga0.telco.co.zw:5665/v1/actions/acknowledge-problem?type=Host&host=' 
                    print("done................")
                    payload = json.dumps({
                        "author": "icingaadmin",
                        "comment": "Global outage. Working on it."
                    })
                    hostname=res['hostname']
                    url1 += hostname
                    print (url1)
                    print(hostname)
                    r = requests.post(url1, headers=headers2, auth=AUTH, data=payload, verify=False)
                    print(r.status_code)
            
            elif 'Core' in group_list[i]:
                user_group = group_list[i]
                print('Internal notification', user_group , res['hostname'])
                print(internal_notify(user_group, res['hostname']))
                ticket = create_ticket(res['hostname'])
                if user_group:
                    url1 = 'https://icinga0.telco.co.zw:5665/v1/actions/acknowledge-problem?type=Host&host=' 
                    print("done................")
                    payload = json.dumps({
                        "author": "icingaadmin",
                        "comment": "Global outage. Working on it."
                    })
                    hostname=res['hostname']
                    url1 += hostname
                    print (url1)
                    print(hostname)
                    r = requests.post(url1, headers=headers2, auth=AUTH, data=payload, verify=False)
                    print(r.status_code)

            

    
    elif res['notification_type']=="RECOVERY":
        print("This is a recovery stage_id: 0,")
        
        
    return Response(status=200)


def internal_notify(group, host):
    num_list = ['0773709735','0783629597']
    print(group, host)
    for number in num_list:
        print(number)
        txt_notify = send_message(str(number),"Core Device "+ host + " is down")
        print(txt_notify)
        # whatsapp_notify = send_whatsapp_msg(number,"Core Device  " + host + " is down")
        # print(whatsapp_notify)


def get_service_idz(user_pop):

    datetimestring = datetime.now()
    # YY-mm-dd H:M:S
    dt_string = datetimestring.strftime("%Y-%m-%d %H:%M:%S")
    print("date and time =", dt_string)
    # pop1 = "VainonaPOP"
    pop="Dependency_Notify_Test"
    url = f"https://icinga0.telco.co.zw:5665/v1/objects/hosts?filter=\"{pop}\" in host.groups"

    payload={}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic cm9vdDpmYTk4ODE4ODlmNjhlOTFh'
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False)
    k=json.dumps(response.json(),indent=2, sort_keys=True)
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
                    print(type(partner_det))
                    print()
                    print('**************')
                    # notify = send_message(str(partner_det),"DevOps POP is down,we sincerely apologise for the inconvinience caused due to the area fault, out team are working flat-out to resolve the issue. Thank you")
                    # print(notify)
                    message = "An Area fault Notification has been send to this contact"
                    odoo_lognote = create_res_partner_chatter_message(subscription,message,dt_string)
                    print(odoo_lognote)
                    print('********&&&&#######')
                    send_whatsapp_msg(partner_det,'DevOps POP is down/Area Outage affecting Devz area.We sincerely apologise for the inconvenience caused by the area fault. Our team are working flat-out to resolve the issue. Please contact us on 08683012345 for more information regarding this')
                    print(send_whatsapp_msg)
                    
        return 'OK'


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

def create_res_partner_chatter_message(res_id,message,datetimestring):

    row_id = models.execute_kw(DB_NAME, uid, PASSWORD,
        'mail.message', 'create',
        [{ 'model': 'res.partner', 
        'res_id': res_id, 
        'body': message, 
        'author_id': 2, 
        'create_date': datetimestring, 
        'date': datetimestring, 
        'write_date': datetimestring }])

    return row_id



@app.get("/api")
def test():
    # return 'done'
    return request.args['hub.challenge']


@app.route('/webhook1', methods=['POST'])
def whatsapp_notify():
    number = '263773709735'
    return number



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




if __name__ == "__main__":
    app.run(port=5000)

