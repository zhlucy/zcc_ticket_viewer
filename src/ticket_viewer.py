import requests
import base64
import os
import configparser
from viewer import Viewer

def main():

    config = configparser.ConfigParser()
    config.read('config.ini')
    subdomain = config['USER']['subdomain']
    email = config['USER']['Email']
    token = config['USER']['api_token']
    encrypted = base64.b64encode(bytes('{email_addr}/token:{api_token}'.format(email_addr=email, api_token=token), 'utf-8')).decode('utf-8')
    
    url = "https://{}.zendesk.com/api/v2/tickets.json?page[size]=100".format(subdomain)
    response = requests.get(url, headers={'Authorization': 'Basic {}'.format(encrypted)})

    if response.status_code == 200:
        tickets = getTickets(response, encrypted)
        viewer = Viewer(tickets);
        viewer.menu()
    elif response.status_code == 401:
        print("Authentication failed.")
    elif response.status_code >= 500:
        print("Server failed. Try again later.")
    else: 
        print("HTTP Status Code {}.".format(response.status_code))
    print("Exit")

def env_set():
    variables = ["SUBDOMAIN", "EMAIL", "TOKEN"]
    return all([var in os.environ.keys() for var in variables])

def getTickets(response, encrypted):
    json = response.json()
    tickets = json["tickets"]
    while json["meta"]["has_more"]:
        response = requests.get(json["links"]["next"], headers={'Authorization': 'Basic {}'.format(encrypted)})
        json = response.json()
        tickets.extend(json["tickets"])
    return tickets

if __name__ == '__main__':
    main()