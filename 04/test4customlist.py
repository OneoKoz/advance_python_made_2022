"""
Tests function for check Customlist
"""
from customlist import CustomList


def test_oper_add_sub():
    """
    function for testing add/sub operations with lists
    :return: asserts results
    """
    empty_parent_list = []
    parent_list = [-2, -1, 0, 5, 6, 7, 8, 9]
    empty_custom_list = CustomList()
    custom_list = CustomList([1, 2, 3, 4])

    assert empty_custom_list - empty_parent_list == []
    assert empty_parent_list - empty_custom_list == []
    assert empty_custom_list + empty_parent_list == []
    assert empty_parent_list + empty_custom_list == []

    new_add_list = parent_list - custom_list
    for i, _ in enumerate(parent_list):
        if i < len(custom_list):
            assert new_add_list[i] == (parent_list[i] - custom_list[i])
        else:
            assert new_add_list[i] == parent_list[i]

    new_add_list[0] = 1000
    assert parent_list[0] != 1000
    assert custom_list[0] != 1000

    new_add_list = custom_list + empty_custom_list
    for i, val in enumerate(custom_list):
        assert new_add_list[i] == val

    new_add_list[0] = 1000
    assert not empty_custom_list
    assert custom_list[0] != 1000


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
