import json
import time


def parse_json(json_str: str, callback, required_fields=None, keywords=None):
    if required_fields is None or keywords is None or not json_str:
        return

    json_doc = json.loads(json_str)

    for key in required_fields:
        if key not in json_doc:
            continue

        cur_json_keywords = json_doc[key].split()
        for val in cur_json_keywords:
            if val in keywords:
                callback(val)


def mean(count_call=1):
    all_call_time = []

    def _mean(func):
        def wrapper(*args, **kwargs):
            start_period = time.time()
            res = func(*args, **kwargs)
            end_period = time.time()
            all_call_time.insert(0, end_period - start_period)

            count_time = min(count_call, len(all_call_time))
            mean_val = sum(all_call_time[:count_time])
            mean_val /= count_time
            wrapper.count_time = count_time
            wrapper.count_calls = len(all_call_time)
            print(f'mean time of {count_time} last call = {mean_val}')
            return res

        wrapper.count_time = 0
        wrapper.count_calls = 0
        return wrapper

    return _mean
