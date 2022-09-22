import numpy as np


def near_zero(all_nums):
    if not all_nums:
        return []

    closest_zero_el = min(np.abs(all_nums))
    close_nums = []

    for num in all_nums:
        if np.isclose(abs(num), closest_zero_el):
            close_nums.append(num)

    return close_nums


def merge_lists(list1, list2):
    if not list1 or not list2:
        return []

    set_list1 = set(list1)

    return sorted(set_list1.intersection(list2))


assert near_zero([-5, 9, 6, -8]) == [-5]
assert near_zero([-1, 2, -5, 1, -1]) == [-1, 1, -1]
assert not near_zero([])
assert near_zero([0, 0]) == [0, 0]
assert near_zero([-1, 2, -5, 1, -1, 0.5]) == [0.5]

assert merge_lists([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]
assert merge_lists([1], [1]) == [1]
assert merge_lists([1, 2, 3, 4, 5], (1, 1, 1, 1, 1, 1)) == [1]
assert not merge_lists([1, 2, 3, 4, 5], [6, 7, 8])
assert not merge_lists([], [1, 2, 3, 4, 5])
assert not merge_lists([1, 2, 3, 4, 5], [])
assert not merge_lists([], ())
