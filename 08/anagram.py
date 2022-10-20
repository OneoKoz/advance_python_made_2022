from collections import defaultdict
from typing import List


def find_anagrams(text: str, pattern: str) -> List[int]:
    text = text.lower().strip()
    pattern = pattern.lower().strip()
    if not pattern or not text:
        return []

    all_word_patt = defaultdict(lambda: 0)
    count_pat_word = len(pattern)
    count_neg = 0
    ans_list = []
    for letter in pattern:
        all_word_patt[letter] += 1

    for i, letter in enumerate(text):
        if i >= len(pattern):
            if text[i - len(pattern)] in all_word_patt:
                if all_word_patt[text[i - len(pattern)]] < 0:
                    count_neg += 1
                all_word_patt[text[i - len(pattern)]] += 1
                count_pat_word += 1

        if letter in all_word_patt:
            all_word_patt[letter] -= 1
            count_pat_word -= 1
            if all_word_patt[letter] < 0:
                count_neg -= 1

        if not count_pat_word and not count_neg:
            ans_list.append(i - len(pattern) + 1)
    return ans_list
