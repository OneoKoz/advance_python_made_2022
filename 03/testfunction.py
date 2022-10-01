from main import parse_json, mean

COUNT_TIME_FOO = 10
COUNT_TIME_BOO = 5


def test_parse_json(*, json_str, required_fields=None, keywords_count=None):
    counter = {}

    def callback(word, count_dict=counter):
        if word in count_dict:
            count_dict[word] += 1
        else:
            count_dict[word] = 1

    keywords, count_call = None, None
    if keywords_count:
        keywords, count_call = zip(*keywords_count)

    parse_json(json_str, callback=callback, required_fields=required_fields, keywords=keywords)

    if not required_fields or not keywords:
        assert len(counter) == 0
        return

    for i in range(len(count_call)):
        if keywords[i] not in counter:
            assert count_call[i] == 0
        else:
            assert counter[keywords[i]] == count_call[i]


@mean(COUNT_TIME_FOO)
def foo(count_num):
    sum_el = 0
    for i in range(count_num):
        sum_el += i
    return sum_el


@mean(COUNT_TIME_BOO)
def boo(count_num):
    sum_el = 0
    for i in range(count_num):
        sum_el += i
    return sum_el


@mean()
def coo():
    sum_el = 0
    for i in range(3):
        sum_el += i
    return sum_el


test_parse_json(json_str='{"key1": "Word1 word2", "key2": "word2 word3"}',
                required_fields=["key1", "key2"],
                keywords_count=[("word2", 2),
                                ("Word1", 1)])

test_parse_json(json_str='{"key1": "Word1 word2", "key2": "word2 word3"}',
                required_fields=[],
                keywords_count=[("word2", 2),
                                ("Word1", 1)])

test_parse_json(json_str='{"key1": "Word1 word2", "key2": "word2 word3"}',
                required_fields=[])

test_parse_json(json_str='{"key1": "Word1 word2", "key2": "word2 word3"}',
                required_fields=["key3"],
                keywords_count=[("word2", 0),
                                ("Word1", 0)])

test_parse_json(json_str='{"key1": "Word1 word2", "key2": "word2 word3 word2 word2"}',
                required_fields=["key2"],
                keywords_count=[("word2", 3),
                                ("Word1", 0)])

for i in range(1, 100):
    assert foo(i) == sum(range(i))
    assert foo.count_time == min(i, COUNT_TIME_FOO)
    assert foo.count_calls == i
    boo(i)
    assert boo.count_time == min(i, COUNT_TIME_BOO)
    assert boo.count_calls == i
    assert coo.count_time == 0
    assert coo.count_calls == 0
