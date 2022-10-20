import unittest
from anagram import find_anagrams


class TestAnagram(unittest.TestCase):

    def test_anagram(self):
        tests_cases = [["abcba", "abc", [0, 2]],
                       ["aaa", "a", [0, 1, 2]],
                       ["abc cba xabcd", "abc", [0, 4, 9]],
                       ["abcbbabacaabccbcabb ac bb", "abc", [0, 6, 10, 14, 15]],
                       ["dasdas", "", []],
                       ['', 'wee', []],
                       ['qwerty', ' a ', []],
                       ['asasasasasa ssss', 'sssss', []],
                       ['ABC a b c', 'abc', [0]],
                       ['text', 'text1', []]]

        for cur_test in tests_cases:
            self.assertEqual(find_anagrams(cur_test[0], cur_test[1]), cur_test[-1])
