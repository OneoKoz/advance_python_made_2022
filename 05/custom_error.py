from abc import ABC


class CustomError(Exception, ABC):

    def __init__(self, value):
        self._value = value
        super().__init__(str(self))

    @property
    def message(self):
        raise NotImplementedError

    def __str__(self):
        return f'{self._value} - {self.message}'


class NotDigitError(CustomError):
    message = "value must be digits"


class ValueNotInRangeError(CustomError):
    message = "value must be in range 0-8"
