import re


def gen_reader_func(file4gen, keywords):
    all_keywords = keywords.strip().split() if isinstance(keywords, str) else str(keywords)

    def _gen_reader_func(cur_file):
        for cur_line in cur_file:
            for cur_key_word in all_keywords:
                if re.search(f'(\\W|\\A){cur_key_word}(\\W|\\Z)', cur_line, re.IGNORECASE):
                    yield cur_line.strip()
                    break

    if isinstance(file4gen, str):
        with open(file4gen, "r", encoding='utf-8') as file_:
            for gen_line in _gen_reader_func(file_):
                yield gen_line
    else:
        for gen_line in _gen_reader_func(file4gen):
            yield gen_line
