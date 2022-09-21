import requests
import json

url = "https://icinga0.telco.co.zw:5665/v1/actions/acknowledge-problem?type=Host&host=ucrm0.telco.co.zw"

payload = json.dumps({
  "author": "icingaadmin",
  "comment": "Global outage. Working on it."
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Basic cm9vdDpmYTk4ODE4ODlmNjhlOTFh'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)