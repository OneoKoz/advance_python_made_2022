import csv
import json

from abc import ABC


class BaseReader(ABC):

    def __init__(self, encoding='utf-8'):
        self.encoding = encoding

    def read(self, file4read):
        raise NotImplementedError('this method must be implemented')


class TxtReader(BaseReader):

    def read(self, file4read):
        if isinstance(file4read, str):
            with open(file4read, "r", encoding=self.encoding) as file:
                return ''.join(file.readlines())
        else:
            if file4read.seekable():
                file4read.seek(0)
            return ''.join(file4read.readlines())


class JSONReader(BaseReader):

    def read(self, file4read):
        if isinstance(file4read, str):
            with open(file4read, "r", encoding=self.encoding) as file:
                return json.load(file)
        else:
            if file4read.seekable():
                file4read.seek(0)
            try:
                return json.load(file4read)
            except ValueError as err:
                raise ValueError("file content is not JSON") from err


class CSVReader(BaseReader):
    def read(self, file4read):
        if isinstance(file4read, str):
            with open(file4read, 'r', encoding=self.encoding) as file:
                return list(csv.reader(file))
        else:
            if file4read.seekable():
                file4read.seek(0)

            return list(csv.reader(file4read))


def read_data(file4read, reader: BaseReader):
    return reader.read(file4read)
