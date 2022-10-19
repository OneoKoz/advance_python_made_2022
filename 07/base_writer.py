import csv
import json
from abc import ABC

from numpy import shape


class BaseWriter(ABC):

    def __init__(self, decoding='utf-8'):
        self.decoding = decoding

    def write(self, data, file4write):
        raise NotImplementedError('this method must be implemented')


class TxtWriter(BaseWriter):

    def write(self, data, file4write):
        if not isinstance(data, str):
            data = str(data)

        if isinstance(file4write, str):
            with open(file4write, "w", encoding=self.decoding) as file:
                file.write(data)
        else:
            file4write.write(data)


class JSONWriter(BaseWriter):

    def write(self, data, file4write):
        if not isinstance(data, dict):
            data = {"key": data}

        if isinstance(file4write, str):
            with open(file4write, "w", encoding=self.decoding) as file:
                json.dump(data, file)
        else:
            file4write.seek(0)
            file4write.truncate()
            json.dump(data, file4write)


class CSVWriter(BaseWriter):
    def write(self, data, file4write):
        if not isinstance(data, list):
            data = [data]

        if isinstance(file4write, str):
            with open(file4write, 'w', encoding=self.decoding) as file:
                csv.writer(file).writerows(data)
        else:
            file4write.seek(0)
            file4write.truncate()
            if len(shape(data)) == 1:
                csv.writer(file4write).writerow(data)
            else:
                csv.writer(file4write).writerows(data)


def dump_data(data, filepath, writer: BaseWriter):
    return writer.write(data, filepath)
