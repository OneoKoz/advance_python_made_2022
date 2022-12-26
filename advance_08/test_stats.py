import collections
import time
import unittest

from stats import Stats


class TestStats(unittest.TestCase):

    def test_timer(self):
        self.assertEqual(Stats.collect(), {})
        Stats.timer("used")
        Stats.timer("unused")
        self.assertEqual(Stats.collect(), collections.defaultdict())
        self.assertEqual(Stats.timer("used").get_value(), 0.0)
        self.assertEqual(Stats.timer("unused").get_name(), "unused.MetricTimer")

        Stats.timer("used").add(0.7)
        self.assertEqual(Stats.timer("used").get_value(), 0.7)
        Stats.timer("used").add(0.3)
        self.assertEqual(Stats.timer("used").get_value(), 1.0)

        time_sleep = 1
        with Stats.timer('used'):
            time.sleep(time_sleep)

        self.assertTrue(Stats.timer('used').get_value() - 2 < 1)

        test_collect = Stats.collect()
        self.assertEqual(len(test_collect), 1)
        self.assertEqual(list(test_collect.keys())[0], "used.MetricTimer")
        self.assertTrue(test_collect["used.MetricTimer"] - 2 < 1)

        self.assertEqual(Stats.timer("used").get_value(), 0.)

        Stats.timer("used").add(0.3)
        self.assertEqual(Stats.timer("used").get_value(), 0.3)
        Stats.timer("used").clear()
        self.assertEqual(Stats.timer("used").get_value(), 0.)

    def test_avg(self):
        self.assertEqual(Stats.collect(), {})
        Stats.avg("used")
        Stats.avg("used_second")

        Stats.avg("unused")
        self.assertEqual(Stats.collect(), collections.defaultdict())
        self.assertEqual(Stats.avg("used").get_value(), 0.)
        self.assertEqual(Stats.avg("unused").get_name(), "unused.MetricAvg")
        Stats.avg("used").add(0.7)

        self.assertEqual(Stats.avg("used").get_value(), 0.7)
        Stats.avg("used").add(0.5)

        Stats.avg("used_second").add(0.5)
        self.assertEqual(Stats.avg("used").get_value(), 0.6)
        self.assertEqual(Stats.collect(), {"used.MetricAvg": 0.6, "used_second.MetricAvg": 0.5})
        self.assertEqual(Stats.avg("used").get_value(), 0.)

        Stats.avg("used").add(0.3)
        self.assertEqual(Stats.avg("used").get_value(), 0.3)
        Stats.avg("used").clear()
        self.assertEqual(Stats.avg("used").get_value(), 0.)

    def test_count(self):
        self.assertEqual(Stats.collect(), {})
        Stats.count("used")
        Stats.count("used_second")

        Stats.count("unused")
        self.assertEqual(Stats.collect(), collections.defaultdict())
        self.assertEqual(Stats.count("used").get_value(), 0.)
        self.assertEqual(Stats.count("unused").get_name(), "unused.MetricCount")

        Stats.count("used").add()
        self.assertEqual(Stats.count("used").get_value(), 1)
        Stats.count("used").add()
        Stats.count("used_second").add()
        self.assertEqual(Stats.count("used").get_value(), 2)

        self.assertEqual(Stats.collect(), {"used.MetricCount": 2, "used_second.MetricCount": 1})
        self.assertEqual(Stats.count("used").get_value(), 0.)
        Stats.count("used").add()

        self.assertEqual(Stats.count("used").get_value(), 1)
        Stats.count("used").clear()
        self.assertEqual(Stats.count("used").get_value(), 0.)

    def test_all_metric(self):
        res = 3
        Stats.count("calc").add()
        Stats.avg("calc").add(res)
        res = 7
        Stats.timer("calc").add(0.2)
        Stats.count("calc").add()
        Stats.avg("calc").add(res)

        Stats.count("http_get_data").add()
        Stats.avg("http_get_data").add(0.7)

        Stats.count("no_used")

        metrics = Stats.collect()
        self.assertEqual(metrics, {"calc.MetricCount": 2,
                                   "calc.MetricAvg": 5.0,
                                   "calc.MetricTimer": 0.2,
                                   "http_get_data.MetricCount": 1,
                                   "http_get_data.MetricAvg": 0.7})

        metrics = Stats.collect()
        self.assertEqual(metrics, {})
