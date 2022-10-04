"""
Tests function for check Customlist
"""
from customlist import CustomList


def check_oper_with_list(list1, list2, sub=True, left=True, val_4_check=0.5):
    """
    functions for checking operation between 2 lists
    :param list1: first list
    :param list2: second list
    :param sub: sub = True if operation is sub, else - False
    :param left: left = True if list1 stay on the first position, else - False
    :param val_4_check: param for checking the oper_list for dependence
    :return: assert results
    """

    list1_copy = list1.copy()
    list2_copy = list2.copy()

    if sub:
        oper_list = list1 - list2 if left else list2 - list1
    else:
        oper_list = list1 + list2 if left else list2 + list1

    for i, val in enumerate(oper_list):
        first_el = 0
        second_el = 0
        if i < len(list1):
            first_el = list1[i]
        if i < len(list2):
            second_el = list2[i]

        real_val = ((-1) ** (int(sub and not left)) * first_el +
                    (-1) ** (int(sub and left)) * second_el)

        assert val == real_val

    # checking that the result of the operation is a new list
    for i, _ in enumerate(oper_list):
        oper_list[i] = val_4_check
        if i < len(list1):
            assert oper_list[i] != list1[i]
        if i < len(list2):
            assert oper_list[i] != list2[i]

    # checking that the original lists have remained unchanged
    assert len(list1_copy) == len(list1)
    for ind, val in enumerate(list1_copy):
        assert list1[ind] == val

    assert len(list2_copy) == len(list2)
    for ind, val in enumerate(list2_copy):
        assert list2[ind] == val


def test_oper_add_sub():
    """
    function for testing add/sub operations with lists
    :return: asserts results
    """

    # checking operations on empty lists
    check_oper_with_list([], CustomList(), sub=True, left=True)
    check_oper_with_list([], CustomList(), sub=False, left=True)
    check_oper_with_list([], CustomList(), sub=True, left=False)
    check_oper_with_list([], CustomList(), sub=False, left=False)

    # checking operations on lists with diff size
    check_oper_with_list([-2, -1, 0, 5, 6, 7, 8, 9], CustomList([1, 2, 3, 4]), sub=True, left=True)
    check_oper_with_list([-2, -1, 0, 5, 6, 7, 8, 9], CustomList([1, 2, 3, 4]), sub=False, left=True)
    check_oper_with_list([-2, -1, 0, 5, 6, 7, 8, 9], CustomList([1, 2, 3, 4]), sub=True, left=False)
    check_oper_with_list([-2, -1, 0, 5, 6, 7, 8], CustomList([1, 2, 3, 4]), sub=False, left=False)

    check_oper_with_list([], CustomList([1, 2, 3, 4]), sub=True, left=True)
    check_oper_with_list([-2, -1, 0, 5, 6, 7, 8, 9], CustomList([]), sub=False, left=True)
    check_oper_with_list([-2, -1, 0, 5, 6, 7, 8, 9],
                         CustomList([-2, -1, 0, 5, 6, 7, 8, 9]), sub=True, left=False)
    check_oper_with_list([1, 2, 3, 4], CustomList([1, 2, 3, 4]), sub=False, left=False)


def test_compare_oper():
    """
    function for testing comparatives operations with lists
    :return: asserts results
    """
    empty_parent_list = []
    parent_list = [-2, -1, 0, 5, 6, 7, 8, 9]
    equal_parent_list = [1, 1, 1, 1, 1, 1, 1]
    empty_custom_list = CustomList()
    custom_list = CustomList([1, 2, 3, 1])
    equal_custom_list = CustomList([1, 1, 1, 1, 1, 1, 1])

    assert empty_custom_list >= empty_parent_list
    assert empty_custom_list == empty_parent_list
    assert empty_custom_list >= empty_parent_list

    assert equal_custom_list == custom_list
    assert equal_custom_list == equal_parent_list
    assert equal_parent_list == equal_custom_list
    assert parent_list > custom_list
    assert empty_custom_list != equal_custom_list


def test_str_list():
    """
    function for testing str operations with list
    :return: assert results
    """
    first_custom_list = CustomList()
    second_custom_list = CustomList([1, 2, 3, 4])

    assert str(first_custom_list) == "self=[], sum=0"
    assert str(second_custom_list) == "self=[1, 2, 3, 4], sum=10"


test_oper_add_sub()
test_compare_oper()
test_str_list()
