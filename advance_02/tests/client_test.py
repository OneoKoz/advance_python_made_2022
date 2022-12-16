import os.path
import threading
import unittest
from unittest import mock

from advance_02.client import start_client, get_args
from advance_02.server import start_server


class TestClient(unittest.TestCase):

    @mock.patch('builtins.print')
    def test_valid_data(self, mock_print):
        all_test_ans = [
            (['cl.py', ''], 'not enough argument'),
            (['cl.py', '10'], 'not enough argument'),
            (['cl.py', '10', 'notexistfile'], 'file is not exists'),
            (['cl.py', 'qq', 'notexistfile'], 'count must be int'),
        ]

        for test in all_test_ans:
            with mock.patch('sys.argv', test[0]):
                num_thr, path_2_urls = get_args()
                self.assertEqual(num_thr, (int(test[0][1]) if len(test[0]) > 2 and test[0][1].isdigit() else None))
                self.assertEqual(path_2_urls,
                                 (int(test[0][2]) if len(test[0]) > 2 and os.path.exists(test[0][2]) else None))
                for cur_arg in mock_print.call_args_list:
                    if test[1] in cur_arg[0][0]:
                        self.assertEqual(cur_arg[0][0], test[1])

    @mock.patch('advance_02.server.calc_word', return_value=True)
    def test_client_server(self, mock_calc):
        test_value = r'{"br": 7, "html": 3, "it": 3, "head": 2, "title": 2, "URL": 2, "for": 2}'

        mock_calc.return_value = test_value.encode('utf-8')

        server = threading.Thread(target=start_server, args=(2, 7), daemon=True)
        server.start()
        with mock.patch('builtins.print') as mock_print:
            start_client('../conf/urls.txt', 3)
            server.join()
            for cur_arg in mock_print.call_args_list:
                for call_line in cur_arg[0]:
                    if 'data=' in call_line:
                        test = call_line.split('data=')[-1].replace('\'', '')
                        assert test == test_value
