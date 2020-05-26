import requests
requests.packages.urllib3.disable_warnings()
from config import servers
import time

def GetCimcToken(server):
    header = {"Content-Type": "application/json"}
    body = {"UserName": server["user"], "Password": server["password"]}
    url="https://{}/redfish/v1/SessionService/Sessions".format(server["ip"])
    try:
        response = requests.post(url=url, headers=header, json=body, verify=False)
        if response.status_code == 201:
            print("OAuth Token is %s" % response.headers["X-Auth-Token"])
            return response.headers["X-Auth-Token"]
        else:
            print("Something has gone wrong...")
            print("Headers: " + response.headers)
            print("Body: " + response.json())
    except ValueError as e:
        print (e)

def GetSerialNumber(server):
    header = {"Content-Type": "application/json", "Authentication": server["token"]}
    url="https://{}/redfish/v1/Chassis/1".format(server["ip"])
    try:
        response = requests.get(url=url, auth=(server["user"],server["password"]), verify=False)
        return response.json()["SerialNumber"]
    except ValueError as e:
        print(e)

def PowerOff(server):
    url = "https://{}/redfish/v1/Systems/{}/Actions/ComputerSystem.Reset".format(server["ip"],server["serial"])
    body = {"ResetType":"ForceOff"}
    try:
        response = requests.post(url=url, auth=(server["user"],server["password"]), json=body, verify=False)
        print("Server %s was powered down" % server["serial"])
    except ValueError as e:
        print(e)

def PowerOn(server):
    url = "https://{}/redfish/v1/Systems/{}/Actions/ComputerSystem.Reset".format(server["ip"],server["serial"])
    body = {"ResetType":"On"}
    try:
        response = requests.post(url=url, auth=(server["user"],server["password"]), json=body, verify=False)
        print("Server %s was powered up" % server["serial"])
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    for server in servers:
        server["token"] = "OAuth " + GetCimcToken(server)
        server["serial"] = GetSerialNumber(server)
        PowerOff(server)
        time.sleep(5)
        PowerOn(server)
    