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
    
    url = "https://{}.zendesk.com/api/v2/tickets.json".format(subdomain)
    response = requests.get(url, headers={'Authorization': 'Basic {}'.format(encrypted)})

    if response.status_code == 200:
        viewer = Viewer(response.json()["tickets"]);
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

if __name__ == '__main__':
    main()