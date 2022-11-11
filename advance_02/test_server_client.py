import subprocess
import threading
import unittest
from unittest import mock

from client import start_client
from server import start_server, calc_word


class TestClientServer(unittest.TestCase):

    def test_input_param_client(self):
        all_test_ans = [
            ('python3 client.py', 'not enough argument'),
            ('python3 client.py 10', 'not enough argument'),
            ('python3 client.py 10 notexistfile', 'file is not exists'),
            ('python3 client.py qq notexistfile', 'count must be int'),
        ]

        def run_shell(command):
            with subprocess.Popen([command], stdout=subprocess.PIPE, shell=True) as com_line:
                out = com_line.communicate()[0].decode('utf-8')
                return out.split('\n', maxsplit=1)[0]

        for test in all_test_ans:
            assert run_shell(test[0]) == test[1]

    def test_input_param_server(self):
        all_test_ans = [
            ('python3 server.py -w l -k 10', 'count must be number'),
            ('python3 server.py -w 10 -k wd', 'count must be number'),
            ('python3 server.py -w e -k w', 'count must be number'),
        ]

        def run_shell(command):
            with subprocess.Popen([command], stdout=subprocess.PIPE, shell=True) as com_line:
                out = com_line.communicate()[0].decode('utf-8')
                return out.split('\n', maxsplit=1)[0]

        for test in all_test_ans:
            assert run_shell(test[0]) == test[1]

    def test_server_calc(self):
        url_test = r'http://www.testingmcafeesites.com/testcat_ac.html'
        answ_test = b'{"br": 7, "html": 3, "it": 3, "head": 2, "title": 2, "URL": 2, "for": 2}'

        assert calc_word(url_test) == answ_test

    def test_client_server(self):

        test_value = '{"br": 7, "html": 3, "it": 3, "head": 2, "title": 2, "URL": 2, "for": 2}'

        def func4server():
            with mock.patch('server.calc_word') as mock_calc:
                mock_calc.return_value = test_value.encode('utf-8')
                start_server()

        with mock.patch('builtins.print') as mock_print:
            threading.Thread(target=func4server, daemon=True).start()
            start_client()

            for cur_arg in mock_print.call_args_list:
                if 'data=' in cur_arg:
                    assert cur_arg.split('data=')[-1] == test_value
