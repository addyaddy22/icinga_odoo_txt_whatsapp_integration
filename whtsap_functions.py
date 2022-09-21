import json
import requests
from constants import *




# @app.post("/webhook")
# def post():
#     body = request.json

#     base = body['entry'][0]['changes'][0]['value']
#     if('messages' in base):
#         sender = base['messages'][0]['from']

#         msg = base['messages'][0]['text']['body']

#         enviroment.recv(sender, msg)

#     return "Done"

def send_whatsapp_msg(phone, message):
    try:
        phone_num = phone.replace('0','263',1)
        print(message)
        print(phone_num)
        url = f"https://graph.facebook.com/v14.0/{fb_phone}/messages"
        data = {
            "messaging_product": "whatsapp",
            "to": phone_num,
            "text": {"body": message}
        }
        
        json_ob = json.dumps(data['text'], indent =4)
        
        data = {
            "messaging_product": "whatsapp",
            "to": phone_num,
            "text":json_ob
        }
        print(data)
        headers = {
            "Authorization": 
            f"Bearer {fb_token}", 
            "Content-Type": "application/json"
        }

        # req = requests.post(url, json=data, headers=headers)
        response = requests.request("POST", url, headers=headers, data=data)
        print(response.text)
    except Exception as e:
        print(e)
        pass


# def send_whatsapp_msg():

    # url = "https://graph.facebook.com/v14.0/100472189494375/messages"

    # payload ={
    #     "messaging_product": "whatsapp",
    #     "to": "263773709735",
    #     "text": {
    #         "body": "Check your txt"
    #     }
    # }

    # headers = {
    # 'Authorization': 'Bearer EAALCHNivZAiQBAHp9662wAfX8jOnvZCZAswleLxtkMHRfZCqUIY86NbDZC6kaZCYIxZBxQAesLayi3wzAfmDY1FxZBwOybZAKfXcpjRL5FUifRI8iQX9zfvgJGbVgMpDazQcRxDQavx3LRZAJvlBfNsulGsnEuD6ysp5giTTwAYN041vXnR7Jn48ZAzSckVRlVrX4pVUeakZBkDYWQZDZD',
    # 'Content-Type': 'application/json'
    # }

#     response = requests.request("POST", url, headers=headers, data=payload)

#     print(response.text)
# print(send_whatsapp_msg('0773709735','hi wht can we do'))