import io
import unittest

from base_reader import TxtReader, JSONReader, CSVReader, read_data
from base_writer import TxtWriter, JSONWriter, CSVWriter, dump_data
from gen_reader import gen_reader_func


class TestReaderWrite(unittest.TestCase):

    def test_txt_read_write(self):
        def _read_write(*args):
            buf = io.StringIO()
            for line in args:
                dump_data(filepath=buf, data=line, writer=TxtWriter())
            self.assertEqual(read_data(buf, reader=TxtReader()), ''.join(map(str, args)))
            buf.close()

        test_str_1 = ""
        test_str_2 = "qwertyui"
        test_str_3 = "{ 1:3, 4:4}"
        test_str_4 = ['231', '4124', 2]

        _read_write()
        _read_write(test_str_1)
        _read_write(test_str_2)
        _read_write(test_str_3)
        _read_write(test_str_4)
        _read_write(test_str_1, test_str_2)
        _read_write(test_str_1, test_str_2, test_str_3, test_str_4)

    def test_json_read_write(self):

        def _read_write(*args):
            buf = io.StringIO()
            for line in args:
                dump_data(filepath=buf, data=line, writer=JSONWriter())

            if not args:
                with self.assertRaises(ValueError):
                    read_data(buf, reader=JSONReader())
            else:
                if isinstance(args[-1], dict):
                    data = {str(k): v for k, v in args[-1].items()}
                else:
                    data = {"key": args[-1]}
                self.assertEqual(read_data(buf, reader=JSONReader()), data)
            buf.close()

        test_str_1 = {1: 3, 4: 4}
        test_str_2 = ""
        test_str_3 = "qwertyui"
        test_str_4 = ['231', '4124', 2]

        _read_write()
        _read_write(test_str_1)
        _read_write(test_str_2)
        _read_write(test_str_3)
        _read_write(test_str_4)
        _read_write(test_str_1, test_str_2)
        _read_write(test_str_1, test_str_2, test_str_3, test_str_4)

    def test_csv_read_write(self):
        def _read_write(*args):
            buf = io.StringIO()
            for line in args:
                dump_data(filepath=buf, data=line, writer=CSVWriter())

            if not args:
                self.assertEqual(read_data(buf, reader=CSVReader()), [])
            elif isinstance(args[-1], list):
                data = [str(el) for el in args[-1]]
                self.assertEqual(read_data(buf, reader=CSVReader()), [data])
            else:
                self.assertEqual(read_data(buf, reader=CSVReader()), [[f"{args[-1]}"]])
            buf.close()

        test_str_1 = ['231', '4124', 2]
        test_str_2 = ""
        test_str_3 = "qwertyui"
        test_str_4 = {1: 3, 4: 4}
        test_str_5 = 123
        test_str_6 = [[131, 131, 11], [133, 1], [345]]

        _read_write()
        _read_write(test_str_1)
        _read_write(test_str_2)
        _read_write(test_str_3)
        _read_write(test_str_4)
        _read_write(test_str_5)
        _read_write(test_str_6)
        _read_write(test_str_1, test_str_2)
        _read_write(test_str_1, test_str_2, test_str_3, test_str_4)


class TestGenReader(unittest.TestCase):

    def test_gen(self):
        test_line = ["key key key",
                     "qqq errr",
                     "Key notKey",
                     "kEY",
                     "notKey keey keys",
                     'qweqw key',
                     '']

        def _check_line(keys, j):
            j += 1
            while j < len(test_line):
                cur_words = test_line[j].split()
                for word in cur_words:
                    for key in keys:
                        if word.lower() == key:
                            return j
                j += 1
            return None

        buf = io.StringIO()
        buf.write('\n'.join(test_line))
        buf.seek(0)
        self.assertEqual(len(list(gen_reader_func(buf, 3))), 0)
        buf.seek(0)
        self.assertEqual(len(list(gen_reader_func(buf, '  key '))), 4)
        buf.seek(0)
        j = -1
        for line in gen_reader_func(buf, '  key '):
            j = _check_line(['key'], j)
            self.assertEqual(line, test_line[j])

        buf.seek(0)
        self.assertEqual(len(list(gen_reader_func(buf, 'qqq  key '))), 5)
        buf.seek(0)
        j = -1
        for line in gen_reader_func(buf, 'qqq  key '):
            j = _check_line(['qqq', 'key'], j)
            self.assertEqual(line, test_line[j])
