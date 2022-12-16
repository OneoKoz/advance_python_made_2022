import threading
import unittest
from unittest import mock

from advance_02.client import start_client
from advance_02.server import start_server, get_args


class TestServer(unittest.TestCase):

    @mock.patch('getopt.getopt')
    @mock.patch('builtins.print')
    def test_valid_data(self, mock_print, mock_get_arg):
        all_test_ans = [
            (([('-w', 'l'), ('-k', '10')],), 'count must be number'),
            (([('-w', '10'), ('-k', 'wd')],), 'count must be number'),
            (([('-w', 'e'), ('-k', 'w')],), 'count must be number'),
        ]

        for test in all_test_ans:
            mock_get_arg.return_value = test[0]

            num_thread, num_word = get_args()

            assert num_thread == (int(test[0][0][0][1]) if test[0][0][0][1].isdigit() else None)
            assert num_word == (int(test[0][0][1][1]) if test[0][0][1][1].isdigit() else None)

            for cur_arg in mock_print.call_args_list:
                assert cur_arg[0][0] == test[1]

    @mock.patch('advance_02.server.calc_word', return_value=True)
    def test_server_calc(self, mock_calc):
        test_value = '{}'
        path2file = '../conf/urls.txt'
        with open(path2file, 'r') as file:
            count_url = len(file.readlines())

        mock_calc.return_value = test_value.encode('utf-8')

        server = threading.Thread(target=start_server, args=(1, 7), daemon=True)
        server.start()
        with mock.patch('builtins.print') as mock_print:
            start_client(path2file, 1)
            server.join()
            for cur_arg in mock_print.call_args_list:
                for call_line in cur_arg[0]:
                    if 'data=' in call_line:
                        test = call_line.split('data=')[-1].replace('\'', '')
                        count_url -= 1
                        assert test == test_value

        assert count_url == 0
