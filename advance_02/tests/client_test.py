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
                assert num_thr == (int(test[0][1]) if len(test[0]) > 2 and test[0][1].isdigit() else None)
                assert path_2_urls == (int(test[0][2]) if len(test[0]) > 2 and os.path.exists(test[0][2]) else None)
                for cur_arg in mock_print.call_args_list:
                    if test[1] in cur_arg[0][0]:
                        assert cur_arg[0][0] == test[1]

    @mock.patch('advance_02.client.read_file_urls')
    def test_client_server(self, mock_read):
        test_value = '{"br": 7, "html": 3, "it": 3, "head": 2, "title": 2, "URL": 2, "for": 2}'

        def func4server():
            with mock.patch('advance_02.server.calc_word') as mock_calc:
                mock_calc.return_value = test_value.encode('utf-8')
                start_server(1, 7)

        with mock.patch('builtins.print') as mock_print:
            threading.Thread(target=func4server, daemon=True).start()

            with mock.patch('queue.Queue.get') as mock_que_get:
                mock_que_get.return_value = ['test_url', None]
                start_client('', 1)

                for cur_arg in mock_print.call_args_list:
                    if 'data=' in cur_arg:
                        assert cur_arg.split('data=')[-1] == test_value
