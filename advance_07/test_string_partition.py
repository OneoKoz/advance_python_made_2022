import unittest


class TestStringPartition(unittest.TestCase):

    def test_no_sign(self):
        tests_val = [
            ('test test', '/'),
            ('test test', '.'),
            ('test test', ','),
            ('testtest', ' '),
            ('test test', 'q'),
        ]
        for line, sign in tests_val:
            left_res, sign_res, right_res = line.partition(sign)
            self.assertEqual(left_res, line)
            self.assertEqual(sign_res, '')
            self.assertEqual(right_res, '')

    def test_left_sign(self):
        tests_val = [
            ('/test test', '/'),
            ('.test test', '.'),
            (',test test', ','),
            (' testtest', ' '),
            ('qtest test', 'q'),
        ]
        for line, sign in tests_val:
            left_res, sign_res, right_res = line.partition(sign)
            self.assertEqual(left_res, '')
            self.assertEqual(sign_res, sign)
            self.assertEqual(right_res, line[1:])

    def test_right_sign(self):
        tests_val = [
            ('test test/', '/'),
            ('test test.', '.'),
            ('test test,', ','),
            ('testtest ', ' '),
            ('testtestq', 'q'),
        ]
        for line, sign in tests_val:
            left_res, sign_res, right_res = line.partition(sign)
            self.assertEqual(left_res, line[:len(line) - 1])
            self.assertEqual(sign_res, sign)
            self.assertEqual(right_res, '')

    def test_both_sign(self):
        tests_val = [
            ('test /test', '/', 'test ', 'test'),
            ('test .test.', '.', 'test ', 'test.'),
            ('test ,test,', ',', 'test ', 'test,'),
            ('testt est ', ' ', 'testt', 'est '),
            ('testtqestq', 'q', 'testt', 'estq'),
        ]
        for line, sign, left, right in tests_val:
            left_res, sign_res, right_res = line.partition(sign)
            self.assertEqual(left_res, left)
            self.assertEqual(sign_res, sign)
            self.assertEqual(right_res, right)

    def test_many_sign(self):
        tests_val = [
            ('test /t/e/s/t', '/', 'test ', 't/e/s/t'),
            ('test .t.e.s.t.', '.', 'test ', 't.e.s.t.'),
            ('test ,t,e,s,t,', ',', 'test ', 't,e,s,t,'),
            ('testt e s  t ', ' ', 'testt', 'e s  t '),
            ('testqqtqestq', 'q', 'test', 'qtqestq'),
        ]
        for line, sign, left, right in tests_val:
            self.assertEqual(len(line.partition(sign)), 3)
            left_res, sign_res, right_res = line.partition(sign)
            self.assertEqual(left_res, left)
            self.assertEqual(sign_res, sign)
            self.assertEqual(right_res, right)
