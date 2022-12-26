import collections
from typing import Union

from metrics import BaseMetric, MetricAvg, MetricCount, MetricTimer


class Stats:
    __all_metrics: dict = collections.defaultdict(list[BaseMetric])

    @classmethod
    def get_metric_from_all(cls, type_name: str, name: str) -> Union[BaseMetric, None]:
        for metric in cls.__all_metrics[type_name]:
            if metric.get_name().split('.')[0] == name:
                return metric
        return None

    @classmethod
    def timer(cls, name: str) -> Union[BaseMetric, MetricTimer]:
        if timer := cls.get_metric_from_all("timer", name):
            return timer

        new_timer = MetricTimer(name)
        cls.__all_metrics["timer"].append(new_timer)
        return new_timer

    @classmethod
    def avg(cls, name: str) -> Union[BaseMetric, MetricAvg]:
        if avg := cls.get_metric_from_all("avg", name):
            return avg

        new_avg = MetricAvg(name)
        cls.__all_metrics["avg"].append(new_avg)
        return new_avg

    @classmethod
    def count(cls, name: str) -> Union[BaseMetric, MetricCount]:

        if count := cls.get_metric_from_all("count", name):
            return count

        new_count = MetricCount(name)
        cls.__all_metrics["count"].append(new_count)
        return new_count

    @classmethod
    def collect(cls) -> dict:
        result = {}
        for _, value in cls.__all_metrics.items():
            for metric in value:
                if metric.get_value():
                    result[metric.get_name()] = metric.get_value()
        cls.__all_metrics = collections.defaultdict(list[BaseMetric])
        return result
