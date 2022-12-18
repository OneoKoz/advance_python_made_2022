import unittest


class TestInt(unittest.TestCase):

    def test_str_to_int(self):
        test_val = [
            ("0", 0),
            ("10", 10),
            ("-0", 0),
            ("-1", -1),
            ("10000000", 10000000),
            ("10_000_000", 10000000)
        ]

        for line, exp in test_val:
            res = int(line)
            self.assertEqual(res, exp)
            self.assertIsInstance(res, int)

    def test_str_to_int_error(self):
        test_val = [
            "0.0",
            "0.",
            "--1",
            "qwe",
            '1-'
        ]

        for line in test_val:
            self.assertRaises(ValueError, int, line)

    def test_int_notation(self):

        test_vals = [
            ('100', 2, 4),
            ('120', 3, 15),
            ('0b11011000', 2, 216),
            ('0b_1101_1000', 2, 216),
            ('0o12', 8, 10),
            ('0x12', 16, 18)
        ]

        for line, notation, int_val in test_vals:
            self.assertEqual(int(line, notation), int_val)

    def test_float_to_int(self):
        test_vals = [
            (1.0, 1),
            (1.2, 1),
            (-0.0, 0),
            (1.2, 1),
            (123_45.222_013, 12345),
            (1e3, 1000)
        ]
        for float_val, int_val in test_vals:
            self.assertIsInstance(float_val, float)
            self.assertIsInstance(int_val, int)
            self.assertEqual(int(float_val), int_val)
