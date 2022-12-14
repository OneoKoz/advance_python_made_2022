import os.path
import unittest
from unittest import mock

from advance_06.fetcher import get_args


class TestFetcher(unittest.TestCase):

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
