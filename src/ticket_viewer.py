import requests
import base64
import os
import configparser
os.sys.path.append('src')
from viewer import Viewer

def main():
    """
    Parses values in config.ini and runs the ticket viewer program.
    """
    config = configparser.ConfigParser()
    config.read(get_abs_path('config.ini'))
    subdomain = get_config(config, 'USER', 'subdomain', 'unknown')
    email = get_config(config, 'USER', 'email', 'unknown')
    token = get_config(config, 'USER', 'api_token', 'unknown')
    encrypted = base64.b64encode(bytes('{email_addr}/token:{api_token}'.format(email_addr=email, api_token=token), 'utf-8')).decode('utf-8')
    url = "https://{}.zendesk.com/api/v2/tickets.json?page[size]=100".format(subdomain)
    response = requests.get(url, headers={'Authorization': 'Basic {}'.format(encrypted)})

    if response.status_code == 200:
        tickets = get_tickets(response, encrypted)
        viewer = Viewer(tickets);
        viewer.menu()
    else:
        print_error(response)
    print("\nExited Program")

def get_tickets(response, encrypted):
    """
    Returns a list of all tickets.
    """
    json = response.json()
    tickets = json["tickets"]
    while json["meta"]["has_more"]:
        response = requests.get(json["links"]["next"], headers={'Authorization': 'Basic {}'.format(encrypted)})
        json = response.json()
        tickets.extend(json["tickets"])
    return tickets

def get_config(config, section, name, default):
    """
    Returns values in config.ini.
    """
    if len(config.get(section, name)):
        return config.get(section, name)
    return default

def print_error(response):
    """
    Prints the error message.
    """
    status_code = response.status_code
    print("HTTP Status Code {}.".format(status_code))
    if status_code == 401:
        print("Authentication failed.")
    elif status_code == 403:
        print("The account doesn’t have the required permissions to use the API.")
    elif status_code == 404:
        print("Resource not found.")
    elif status_code == 409:
        print("Merge conflict or a uniqueness constraint error in the database due "\
            "to the attempted simultaneous creation of a resource. Try your API call again.")
    elif status_code == 422:
        print("The content type and the syntax of the request entity are correct, "\
            "but the content itself is not processable by the server.")
    elif status_code == 429:
        print("A usage limit has been exceeded.")
    elif status_code == 503: 
        if response.json().get('Retry-After'):
            print("A database timeout or deadlock. Retry request after {} seconds.".format(response.json().get('Retry-After')))
        else:
            print("Zendesk Support may be experiencing internal issues or undergoing scheduled maintenance.")
    elif status_code >= 500:
        print("Server failed. Try again later.")

def get_abs_path(file):
    """
    Gets absolute path of file.
    """
    p = os.path.abspath(os.path.dirname(os.sys.argv[0]))
    return os.path.join(p, file)


if __name__ == '__main__':
    main()