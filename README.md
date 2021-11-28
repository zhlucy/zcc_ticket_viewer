# Zendesk Ticket Viewer

The CLI program pulls tickets from Zendesk and displays them locally.

## Installing
Follow the commands below to install the program.
```
> git clone https://github.com/zhlucy/zcc_ticket_viewer
> cd zcc_ticket_viewer
> pip install -r requirements.txt
```

## Configurating
To generate and enable API token access, see https://support.zendesk.com/hc/en-us/articles/4408889192858-Generating-a-new-API-token

Before running the program, update src/config.ini to include your sudomain, email, and api token.
See example below.
```
> vim src/config.ini
---------config file---------
[USER]
subdomain=<change to your_subdomain>
email=<change to your_email>
api_token=<change to your_token>
```

## Executing program
After completed the steps above, run the program with the following command.
```
python3 src/ticket_viewer.py
```

## Usage Instruction
When the program starts, it displays the main menu.
```
----------------------------------------------------------------------------------------------------
Ticket Viewer Menu
----------------------------------------------------------------------------------------------------
     1: List all tickets
     2: List one ticket
     q: Quit
```
`1`: Lists all tickets with their id, subject, status, priority, and time of update.\
`2`: Displays one ticket with additional details, requester id, assignee id, description, and time of creating the ticket.\
`q`: Ends and exits the program.

### List All Tickets
If `1` is inputted, then the following is displayed.
```
----------------------------------------------------------------------------------------------------
List All Tickets
----------------------------------------------------------------------------------------------------
	 1: Previous page
	 2: Next page
	 z: Return to main menu
	 q: Quit
```
Each page shows a maximum of 25 tickets. Remember to expand/resize your terminal so the 25 tickets fit in the terminal; or scroll up to see the first few tickets.\
`1`: Goes to the previous page\
`2`: Goes to the next page\
`z`: Returns to the main menu\
`q`: Ends and exits the program

To start viewing the first page, input `2`.
When there are no previous or next page, the screen will display `Reached the end`.\
To see the command options again, input `x`.

### List One Ticket

If `2` is inputted, then the following is displayed.
```
----------------------------------------------------------------------------------------------------
List One Ticket
----------------------------------------------------------------------------------------------------
	 z: Return to main menu
	 q: Quit
```
`z`: Returns to the main menu\
`q`: Ends and exits the program

To view a ticket, input its ticket id.
If the ticket does not exist, the screen will display `Ticket not found`.\
To see the command options again, input `x`.

## Authors

Lucy Lu

## Testing
To run the unit tests for this program, use the command below.
```
python3 -m unittest
```
