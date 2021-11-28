# Zendesk Ticket Viewer

The CLI program pulls tickets from Zendesk and displays them locally.

## Installing
Follow the commands below to install the program.
```
> git clone https://github.com/zhlucy/zcc_ticket_viewer
> pip install -r requirements.txt
```

## Configurating
Before running the program, update src/config.ini to include your sudomain, email, and api token.
See example below.
```
> vim src/config.ini
---------config file---------
[USER]
subdomain=<insert subdomain>
email=<insert email>
api_token=<insert api token>
```

## Executing program
After completed the steps above, run the program with the following command.
```
python3 src/ticket_viewer.py
```

## Usage Instruction
When the program starts, it displays the main menu.
```
----------------------------------------------------------------------------------------------------\n"\
Ticket Viewer Menu\n"\
----------------------------------------------------------------------------------------------------\n"\
     1: List all tickets\n"\
     2: List one ticket\n"\
     q: Quit\n"
```
1: Lists all tickets with their id, subject, status, priority, and time of update.
2: Displays one ticket with additional details, requester id, assignee id, description, and time of creating the ticket.
q: Ends and exits the program.

	If `1` is inputted, then the following is displayed.
	```
	----------------------------------------------------------------------------------------------------\n"\
	List All Tickets
	----------------------------------------------------------------------------------------------------\n"\
		 1: Previous page
		 2: Next page
		 x: Show options
		 z: Return to main menu
		 q: Quit
	```
	Each page shows a maximum of 25 tickets.
	1: Goes to the previous page
	2: Goes to the next page
	x: Shows the options (ie. this screen) again
	z: Returns to the main menu
	q: Ends and exits the program

	To start viewing the first page, input `2`.
	When there are no previous or next page, the screen will display `Reached the end`.
	
	---------------------------------------------------------------------------------------------------------
	
	If `2` is inputted, then the following is displayed.
	```
	----------------------------------------------------------------------------------------------------\n"\
	List One Ticket
	----------------------------------------------------------------------------------------------------\n"\
		 x: Show options
		 z: Return to main menu
		 q: Quit
	```
	x: Shows the options (ie. this screen) again
	z: Returns to the main menu
	q: Ends and exits the program

	To view a ticket, input its ticket id.
	If the ticket does not exist, the screen will display `Ticket not found`.

## Authors

Lucy Lu

## Testing
To run the unit tests for this program, use the command below.
```
python3 -m unittest
```