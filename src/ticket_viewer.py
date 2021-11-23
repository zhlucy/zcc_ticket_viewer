import argparse
import requests
import base64

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("subdomain", help="subdomain of website")
    parser.add_argument("email", help="email address of account")
    parser.add_argument("key", help="key for authentication")

    parser.add_argument("-o", "--oauth", action="store_true", help="flag for oauth token authentication")
    parser.add_argument("-a", "--api", action="store_true", help="flag for api token authentication")
    args = parser.parse_args()

    url = "https://{}.zendesk.com/api/v2/tickets.json".format(args.subdomain)
    if (args.oauth):
        print("oauth")
        print(args.key)
        response = requests.get(url, headers={'Authorization': 'Bearer {}'.format(args.key)})
    elif (args.api):
        token = base64.b64encode(bytes('{email_addr}/token:{api_token}'.format(email_addr=args.email, api_token=args.key), 'utf-8')).decode('utf-8')
        response = requests.get(url, headers={'Authorization': 'Basic {}'.format(token)})
    else:
        response = requests.get(url, auth=(args.email, args.key))

    if response.status_code == 200:
        print("Success")
    elif response.status_code == 401:
        print("Authentication failed.")
    elif response.status_code >= 500:
        print("Server failed. Try again later.")
    else: 
        print("HTTP Status Code {}.".format(response.status_code))
    print("Exit")

if __name__ == '__main__':
    main()