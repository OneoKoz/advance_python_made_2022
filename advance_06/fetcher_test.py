import os.path
import unittest
from unittest import mock

from fetcher import get_args, start_client


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


class TestFetcherAsync(unittest.IsolatedAsyncioTestCase):

    @mock.patch('fetcher.fetch_url', new_callable=mock.AsyncMock)
    async def test_fetch(self, mock_fetch_url):
        mock_fetch_url.return_value = 5
        path2file = 'advance_06/urls.txt'
        with open(path2file, 'r', encoding='utf-8') as file:
            count_url = len(file.readlines())

        with mock.patch('builtins.print') as mock_print:
            await start_client(5, path2file)

            for cur_arg in mock_print.call_args_list:
                count_url -= 1
                assert cur_arg[0][-1] == 5
        assert count_url == 0
