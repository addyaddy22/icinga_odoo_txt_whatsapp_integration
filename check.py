import json
import requests
from xmlrpc import client
import xmlrpc.client
from datetime import datetime




# txt = "Dependency_Notify_Test;kvm-g7-2;Servers;VainonaPOP;Virtual_Machine"

# x = txt.split(";")

# print(type(x))
# print(x)
# for i in range(len(x)):
#     if 'POP' in x[i]:
# 	    print(x[i])
SERVER_URL = 'http://154.119.80.8:7500'
DB_NAME = 'odoo_ash'
USERNAME = 'developer@telco.co.zw'
PASSWORD = 'xxxx'


url = "https://sandbox.ipos.co.zw/api/v1/helpdesk_ticketing/helpdesk.ticket"
headers = {
    "cookie": "session_id=bad780cd5a14a881866a0eec1bbdcb313fad4dce",
    "Content-Type": "application/json",
    "Authorization": "xxx"
}

info = xmlrpc.client.ServerProxy('https://demo.odoo.com/start').start()
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(SERVER_URL))
print(common.version())

uid = common.authenticate(DB_NAME, USERNAME, PASSWORD, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(SERVER_URL))

message = "Its working"
date = "2021-12-18 21:00:03"


# datetime object containing current date and time
datetimestring = datetime.now()
 
print("now =", datetimestring)


# dd/mm/YY H:M:S
dt_string = datetimestring.strftime("%Y-%m-%d %H:%M:%S")
print("date and time =", dt_string)


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


# print(create_res_partner_chatter_message(43,message,str(dt_string)))