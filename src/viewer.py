import os

class Viewer:
    """
    A class representing a ticket viewer.

    Attributes:
        amount (int): Total number of tickets.
        pages (int): Total number of pages of tickets.
        tickets (list): List of tickets.
    """
    MAX_PER_PAGE = 25

    def __init__(self, tickets):
        """
        Creates a Viewer object.

        Args:
            tickets (list): List of tickets.
        """
        self.amount = len(tickets)
        self.pages = div_round(self.amount, Viewer.MAX_PER_PAGE)
        self.tickets = tickets
        self.end = False

    def menu(self):
        """
        Displays main menu.
        q: Quit
        1: List all tickets
        2: List one ticket
        """
        options = {'1' : 'List all tickets', '2' : 'List one ticket', 'q' : 'Quit'}
        while not self.end:
            self.print_menu('Ticket Viewer Menu', options)
            data = input("\nOption: ")
            if data == 'q':
                self.end = True
                break
            elif data == '1':
                self.listall()
            elif data == '2':
                self.listone()

    def listone(self):
        """
        Displays menu for listing one ticket.
        Expects ticket id for user input.
        q: Quit
        z: Return to main menu
        """
        options = {'z' : 'Return to main menu', 'q' : 'Quit'}
        self.print_menu("List One Ticket", options)
        while not self.end:
            data = input("\nInput x to see command options\nTicket ID: ")
            if data == 'q':
                self.end = True
                break
            elif data == 'z':
                break
            elif data == 'x':
                self.print_menu("List One Ticket", options)
            else: 
                ticket = self.get_ticket(data)
                if ticket:
                    self.print_detail_ticket(ticket)

    def get_ticket(self, id):
        """
        Returns the ticket specified by the id.
        """
        try:
            id = int(id)
            for ticket in self.tickets:
                if id == ticket["id"]:
                    return ticket
            print('Ticket not found.')
            return None
        except ValueError:
            print('Please enter an integer.')


    def listall(self):
        """
        Displays menu for listing all tickets.
        q: Quit
        z: Return to main menu
        1: Previous page
        2. Next page
        """
        options = {'1' : 'Previous page', '2' : 'Next page', 'z' : 'Return to main menu', 'q' : 'Quit'}
        page, was_end = -1, True
        self.print_menu("List All Tickets", options)
        while not self.end:
            data = input("\nInput x to see command options\nOption: ")
            if data == 'q':
                self.end = True
                break
            elif data == 'z':
                break
            elif data == 'x':
                self.print_menu("List All Tickets", options)
            elif data == '1':
                if self.print_ticket_page(page - 1):
                    page -= 1
                    was_end = False
                elif not was_end:
                    page -= 1
                    was_end = True
            elif data == '2':
                if self.print_ticket_page(page + 1):
                    page += 1
                    was_end = False
                elif not was_end:
                    page += 1
                    was_end = True

    def print_ticket_page(self, page_num):
        """
        Prints a page of tickets specified by page_num. 
        Returns True if page_num is in range, else returns False.
        """
        clear()
        if not 0 <= page_num < self.pages:
            print("Reached the end")
            return False
        else:
            self.print_header()
            for i in range(page_num * Viewer.MAX_PER_PAGE, min(page_num * Viewer.MAX_PER_PAGE + Viewer.MAX_PER_PAGE, self.amount)):
                self.print_ticket(i)
            return True

    def print_header(self):    
        """
        Prints the header of the page view for listing all tickets.
        """
        id = format_field("ID", 10) 
        subject = format_field("Subject", 30)
        status = format_field("Status", 10)
        priority = format_field("Priority", 10)
        updated_at = "Updated At"
        print("{id} {subject}     {status} {priority} {updated_at}".format(id=id, subject=subject, status=status, priority=priority, updated_at=updated_at))
        print('-'*100)
        
    def print_ticket(self, index):
        """
        Prints the ticket specified by its index.
        """
        ticket = self.tickets[index]  
        id = format_field(ticket["id"], 10)
        subject = format_field(ticket["subject"], 30)
        status = format_field(ticket["status"], 10)
        priority = format_field(ticket["priority"], 10)
        updated_at = ticket["updated_at"]
        print("{id} {subject}     {status} {priority} {updated_at}".format(id=id, subject=subject, status=status, priority=priority, updated_at=updated_at))
    
    def print_detail_ticket(self, ticket):
        """
        Prints the ticket wih more details.
        """
        clear()
        print('-'*100)
        print("Subject: {}".format(ticket["subject"]))
        print('-'*100)
        requester = format_field(ticket["requester_id"], 10)
        assignee = format_field(ticket["assignee_id"], 10)
        status = format_field(ticket["status"], 10)
        priority = format_field(ticket["priority"], 10)
        created_at = ticket["created_at"]
        updated_at = ticket["updated_at"]
        print("Requester: {requester}   Status: {status}   Created At: {created_at}".format(requester=requester, status=status, created_at=created_at))
        print("Assignee: {assignee}    Priority: {priority} Updated At: {updated_at}".format(assignee=assignee, priority=priority, updated_at=updated_at))
        print("\n{}".format(ticket["description"]))
        print("\nTags: {}".format(ticket["tags"]))

    def print_menu(self, title, options):
        clear()
        print('-'*100)
        print(title)
        print('-'*100)

        for key in options.keys():
            print("     {key}: {description}".format(key=key, description=options[key]))

def div_round(num, den):
    """
    Divides num by den and rounds up.
    """
    return num // den + (num % den > 0)

def format_field(field, max_length):
    """
    Formats field into a string wih a maximum length of max_len.
    If the field is shorter than the max length, then it's padded with space.
    """
    field = str(field)
    length = min(len(field), max_length)
    if length < max_length:
        return field[:length] + (max_length - length) * " "
    else:
        return field[:length]

def clear():
    os.system('clear')