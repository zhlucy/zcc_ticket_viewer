import unittest
from unittest import mock
import io
from os import sys
import configparser
sys.path.append('src')
from ticket_viewer import *
from viewer import *

class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

def get_mock_response(url, **kwargs):
        if url == 'http://example.com/api/v2/tickets.json':
            return MockResponse({'tickets' : [{'id' : 1}, {'id' : 2}], 
                                'meta' : {'has_more' : True}, 
                                'links' : {'next' : 'http://next.com/api/v2/tickets.json'}}, 200)
        elif url == 'http://next.com/api/v2/tickets.json':
            return MockResponse({'tickets': [{'id' : 3}, {'id' : 4}], 
                                 'meta' : {'has_more' : False}, 
                                 'links' : {'next' : None}}, 200)
        else:
            return MockResponse({'tickets': [{'id' : 3}, {'id' : 4}], 
                                 'meta' : {'has_more' : False}, 
                                 'links' : {'next' : None}}, 200)
        

def get_mock_response_fail(ur, **kwardgs):
    return MockResponse(None, 404)

class MockConfig:
    def __init__(self):
        self.vars = {'USER' : {'subdomain' : 'test_sub', 'email' : 'test_email', 'api_token' : 'test_token'}}

    def read(self, file):
        pass

    def get(self, section, name):
        return self.vars.get(section).get(name)

class TestViewer(unittest.TestCase):
    menu = "----------------------------------------------------------------------------------------------------\n"\
        "Ticket Viewer Menu\n"\
        "----------------------------------------------------------------------------------------------------\n"\
        "     1: List all tickets\n"\
        "     2: List one ticket\n"\
        "     q: Quit\n"
    list_all_menu = "----------------------------------------------------------------------------------------------------\n"\
        "List All Tickets\n"\
        "----------------------------------------------------------------------------------------------------\n"\
        "     1: Previous page\n"\
        "     2: Next page\n"\
        "     x: Show options\n"\
        "     z: Return to main menu\n"\
        "     q: Quit\n"
    list_one_menu = "----------------------------------------------------------------------------------------------------\n"\
        "List One Ticket\n"\
        "----------------------------------------------------------------------------------------------------\n"\
        "     x: Show options\n"\
        "     z: Return to main menu\n"\
        "     q: Quit\n"

    def check_stdout(self, string, function, *args):
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        function(*args)
        sys.stdout = sys.__stdout__ 
        self.assertEqual(string, capturedOutput.getvalue())

    @mock.patch('requests.get', side_effect=get_mock_response)
    def test_get_tickets(self, mock_get):
        response = get_mock_response('http://example.com/api/v2/tickets.json')
        tickets = get_tickets(response, 'some/token:some')
        self.assertListEqual([{'id' : 1}, {'id' : 2}, {'id' : 3}, {'id' : 4}], tickets)

    def test_get_config(self):
        config = configparser.ConfigParser()
        config.read('tests/test_config.ini')
        self.assertEqual('some_domain', get_config(config, 'USER', 'subdomain', 'unknown'))
        self.assertEqual('some_email', get_config(config, 'USER', 'email', 'unknown'))
        self.assertEqual('some_token', get_config(config, 'USER', 'api_token', 'unknown'))

    def test_get_config_default(self):
        config = configparser.ConfigParser()
        config.read('tests/test_default_config.ini')
        self.assertEqual('unknown', get_config(config, 'USER', 'subdomain', 'unknown'))
        self.assertEqual('unknown', get_config(config, 'USER', 'email', 'unknown'))
        self.assertEqual('unknown', get_config(config, 'USER', 'api_token', 'unknown'))

    def test_print_error_401(self):
        response = MockResponse(None, 401)
        self.check_stdout('HTTP Status Code 401.\nAuthentication failed.\n', print_error, response)

    def test_print_error_403(self):
        response = MockResponse(None, 403)
        self.check_stdout("HTTP Status Code 403.\nThe account doesn’t have the required permissions to use the API.\n",
                          print_error, response)
      
    def test_print_error_404(self):
        response = MockResponse(None, 404)
        self.check_stdout('HTTP Status Code 404.\nResource not found.\n', print_error, response)

    def test_print_error_409(self):
        response = MockResponse(None, 409)
        self.check_stdout("HTTP Status Code 409.\nMerge conflict or a uniqueness constraint error in the database due "\
            "to the attempted simultaneous creation of a resource. Try your API call again.\n", print_error, response)

    def test_print_error_422(self):
        response = MockResponse(None, 422)
        self.check_stdout("HTTP Status Code 422.\nThe content type and the syntax of the request entity are correct, "\
            "but the content itself is not processable by the server.\n", print_error, response)

    def test_print_error_429(self):
        response = MockResponse(None, 429)
        self.check_stdout('HTTP Status Code 429.\nA usage limit has been exceeded.\n', print_error, response)

    def test_print_error_503(self):
        response = MockResponse({}, 503)
        self.check_stdout("HTTP Status Code 503.\nZendesk Support may be experiencing internal issues or undergoing "\
            "scheduled maintenance.\n", print_error, response)

    def test_print_error_503_with_retry(self):
        response = MockResponse({'Retry-After' : 2}, 503)
        self.check_stdout("HTTP Status Code 503.\nA database timeout or deadlock. Retry request after 2 seconds.\n", 
                          print_error, response)

    def test_print_error_500(self):
        response = MockResponse(None, 500)
        self.check_stdout('HTTP Status Code 500.\nServer failed. Try again later.\n', print_error, response)

    def test_print_error_other(self):
        response = MockResponse(None, 402)
        self.check_stdout('HTTP Status Code 402.\n', print_error, response)

    @mock.patch('builtins.input', side_effect=['1', 'q'])
    def test_menu_1(self, mock_input):
        viewer = Viewer([{'id' : 1}, {'id' : 2}])
        correct_out = self.menu + self.list_all_menu
        self.check_stdout(correct_out, viewer.menu)

    @mock.patch('builtins.input', side_effect=['2', 'q'])
    def test_menu_2(self, mock_input):
        viewer = Viewer([{'id' : 1}, {'id' : 2}])
        correct_out = self.menu + self.list_one_menu
        self.check_stdout(correct_out, viewer.menu)

    @mock.patch('builtins.input', side_effect=['1', 'q'])
    def test_listone_ticket(self, mocked_input):
        viewer = Viewer([{'id' : 1, 'requester_id' : 12, 'assignee_id' : 1243, 'subject' : 'subject 1', 'description' : 'some details',
                          'status' : 'open', 'priority' : 'low', 'updated_at' : 'some_time', 'created_at' : 'created_time', 'tags' : ['t1', 't2']}, 
                         {'id' : 2, 'requester_id' : 2432, 'assignee_id' : 34, 'subject' : 'subject 2', 'description' : 'some details',
                          'status' : 'open', 'priority' : 'high', 'updated_at' : 'some_time', 'created_at' : 'created_time', 'tags' : ['t1', 't2']}])
        ticket_detail = "----------------------------------------------------------------------------------------------------\n"\
        "Subject: subject 1\n"\
        "----------------------------------------------------------------------------------------------------\n"\
        "Requester: 12           Status: open         Created At: created_time\n"\
        "Assignee: 1243          Priority: low        Updated At: some_time\n\n"\
        "some details\n\n"\
        "Tags: ['t1', 't2']\n"
        correct_out = self.list_one_menu + ticket_detail
        self.check_stdout(correct_out, viewer.listone)

    @mock.patch('builtins.input', side_effect=['2', 'z', 'q'])
    def test_listone_z(self, mocked_input):
        viewer = Viewer([{'id' : 1}, {'id' : 2}])
        correct_out = self.menu + self.list_one_menu + self.menu
        self.check_stdout(correct_out, viewer.menu)

    @mock.patch('builtins.input', side_effect=['x', 'q'])
    def test_listone_x(self, mocked_input):
        viewer = Viewer([{'id' : 1}, {'id' : 2}])
        correct_out = self.list_one_menu * 2
        self.check_stdout(correct_out, viewer.listone)

    def test_get_ticket(self):
        viewer = Viewer([{'id' : 1}, {'id' : 2}])
        self.assertDictEqual({'id' : 2}, viewer.get_ticket(2))
        self.assertEqual(None, viewer.get_ticket(3))
        self.check_stdout("Please enter an integer.\n", viewer.get_ticket, 'some')

    def test_listall_paging(self):
        self.maxDiff = None
        tickets = [{'id' : 1, 'subject' : 'subject 1', 'status' : 'open', 'priority' : 'low', 'updated_at' : 'some_time'}, 
                             {'id' : 2, 'subject' : 'subject 2', 'status' : 'open', 'priority' : 'high', 'updated_at' : 'some_time'},
                             {'id' : 3, 'subject' : 'subject 3', 'status' : 'open', 'priority' : 'high', 'updated_at' : 'some_time'}]
        page_1 = "ID         Subject                            Status     Priority   Updated At\n"\
            "----------------------------------------------------------------------------------------------------\n"\
            "1          subject 1                          open       low        some_time\n"\
            "2          subject 2                          open       high       some_time\n"\

        page_2 = "ID         Subject                            Status     Priority   Updated At\n"\
            "----------------------------------------------------------------------------------------------------\n"\
            "3          subject 3                          open       high       some_time\n"
        end = "Reached the end\n"

        @mock.patch('builtins.input', side_effect=['2', 'q'])
        def check_show_tickets(mocked):
            viewer = Viewer(tickets)
            Viewer.MAX_PER_PAGE = 2
            correct_out = self.list_all_menu + page_1
            self.check_stdout(correct_out, viewer.listall)
            
        @mock.patch('builtins.input', side_effect=['1', 'q'])
        def check_end_prev(mocked):
            viewer = Viewer(tickets)
            Viewer.MAX_PER_PAGE = 2
            correct_out = self.list_all_menu + end
            self.check_stdout(correct_out, viewer.listall)

        @mock.patch('builtins.input', side_effect=['2', '2', 'q'])
        def check_next(mocked):
            viewer = Viewer(tickets)
            Viewer.MAX_PER_PAGE = 2
            correct_out = self.list_all_menu + page_1 + page_2
            self.check_stdout(correct_out, viewer.listall)

        @mock.patch('builtins.input', side_effect=['2', '2', '2', 'q'])
        def check_end_next(mocked):
            viewer = Viewer(tickets)
            Viewer.MAX_PER_PAGE = 2
            correct_out = self.list_all_menu + page_1 + page_2 + end
            self.check_stdout(correct_out, viewer.listall)

        @mock.patch('builtins.input', side_effect=['2', '2', '1', 'q'])
        def check_prev(mocked):
            viewer = Viewer(tickets)
            Viewer.MAX_PER_PAGE = 2
            correct_out = self.list_all_menu + page_1 + page_2 + page_1
            self.check_stdout(correct_out, viewer.listall)

        check_show_tickets()
        check_end_prev()
        check_next()
        check_end_next()
        check_prev()

    def test_print_ticket_page(self):
        viewer = Viewer([{'id' : 1, 'subject' : 'subject 1', 'status' : 'open', 'priority' : 'low', 'updated_at' : 'some_time'}, 
                         {'id' : 2, 'subject' : 'subject 2', 'status' : 'open', 'priority' : 'high', 'updated_at' : 'some_time'}])
        self.assertTrue(viewer.print_ticket_page(0))
        self.assertFalse(viewer.print_ticket_page(-1))
        self.assertFalse(viewer.print_ticket_page(1))

    @mock.patch('builtins.input', side_effect=['1', 'z', 'q'])
    def test_listall_z(self, mocked_input):
        viewer = Viewer([{'id' : 1}, {'id' : 2}])
        correct_out = self.menu + self.list_all_menu + self.menu
        self.check_stdout(correct_out, viewer.menu)

    @mock.patch('builtins.input', side_effect=['x', 'q'])
    def test_listall_x(self, mocked_input):
        self.maxDiff = None
        viewer = Viewer([{'id' : 1}, {'id' : 2}])
        correct_out = self.list_all_menu * 2
        self.check_stdout(correct_out, viewer.listall)

    def test_div_round(self):
        self.assertEqual(2, div_round(4, 2))
        self.assertEqual(1, div_round(1, 2))
        self.assertEqual(2, div_round(3, 2))

    def test_format_field(self):
        self.assertEqual("some_string    ", format_field('some_string', 15))
        self.assertEqual("some_", format_field('some_string', 5))
        self.assertEqual("123  ", format_field(123, 5))
        self.assertEqual("1", format_field(1, 1))

    @mock.patch('requests.get', side_effect=get_mock_response)
    @mock.patch('configparser.ConfigParser', side_effect=MockConfig)
    @mock.patch('builtins.input', side_effect=['q'])
    def test_main_success(self, mock_request, mock_config, mock_in):
        self.check_stdout(self.menu + '\nExited Program\n', main)

    @mock.patch('requests.get', side_effect=get_mock_response_fail)
    @mock.patch('configparser.ConfigParser', side_effect=MockConfig)
    def test_main_fail(self, mock_request, mock_config):
        correct_out = 'HTTP Status Code 404.\nResource not found.\n\nExited Program\n'
        self.check_stdout(correct_out, main)