import time


class BaseMetric:
    def __init__(self, name: str) -> None:
        self.__name = name + "." + self.__class__.__name__
        self.__value = 0.

    def get_name(self) -> str:
        return self.__name

    def get_value(self) -> float:
        return self.__value

    def set_value(self, val: float) -> None:
        self.__value = val

    def add(self, value: float) -> None:
        self.__value = value if not self.__value else self.__value + value

    def clear(self) -> None:
        self.__value = 0.


class MetricTimer(BaseMetric):

    def __init__(self, name: str) -> None:
        self._start_value = None
        super().__init__(name)

    def __enter__(self):
        self._start_value = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._start_value:
            self.add(time.time() - self._start_value)


class MetricAvg(BaseMetric):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.count = 0

    def add(self, value: float) -> None:
        if not self.get_value():
            self.set_value(value)
        else:
            self.set_value((self.get_value() * self.count + value) / (self.count + 1))
        self.count += 1


class MetricCount(BaseMetric):

    def add(self, value: float = 1) -> None:
        super().add(value)
