import requests
import urllib3
import json
urllib3.disable_warnings()


url =  "https://hotspot.openaccess.co.zw/ibsng_odoo_customer_data/sms_notification.php"


def send_message(number,message):
    payload = {'numbers':number,'message': message}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers,verify=False)
    print(response.text)



# send_message('0773709735','Test API message dude')