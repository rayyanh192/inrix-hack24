import requests
import json


def get_token():
    url = "https://na-api.beta.inrix.com/Traffic/Inrix.ashx?Action=GetSecurityToken&vendorId=1680049421&consumerId=3466e4ef-329b-474f-b52b-a3818e9df6b6&format=json"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    token = json.loads(response.text)["result"]["token"]
    print("Token: " + token)
    return token
