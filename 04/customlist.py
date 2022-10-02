"""
This module created for class CustomList
"""
from math import isclose


class CustomList(list):
    """
    CustomList
    list inheritance
    """

    def __add_or_sub_with_lists(self, other, is_sub=True, is_right=False):
        res_list = CustomList([0]) * max(len(self), len(other))
        for i, _ in enumerate(res_list):
            first_el = 0
            second_el = 0

            if i < len(self):
                first_el = self[i] * (-1) ** int(is_sub and is_right)

            if i < len(other):
                second_el = other[i] * (-1) ** int(is_sub and not is_right)

            res_list[i] = first_el + second_el
        return res_list

    def __sub__(self, other):
        return self.__add_or_sub_with_lists(other, is_sub=True, is_right=False)

    def __add__(self, other):
        return self.__add_or_sub_with_lists(other, is_sub=False, is_right=False)

    def __rsub__(self, other):
        return self.__add_or_sub_with_lists(other, is_sub=True, is_right=True)

    def __radd__(self, other):
        return self.__add_or_sub_with_lists(other, is_sub=False, is_right=True)

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __eq__(self, other):
        return isclose(sum(self), sum(other))

    def __ne__(self, other):
        return not isclose(sum(self), sum(other))

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __str__(self):
        return f"{self=}, sum={sum(self)}"
