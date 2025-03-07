import numpy as np


def sol_eq(a, b, c):
    assert None not in (a, b, c), "a, b, c must be numbers"
    d = b ** 2 - 4 * a * c

    if np.isclose(a, 0):
        if np.isclose(b, 0):
            return np.nan
        return -c / b, np.nan

    if d < 0:
        return np.nan

    x1 = (-b + d ** 0.5) / (2 * a)
    x2 = (-b + d ** 0.5) / (2 * a)

    return x1, x2


def div_par(all_nums):
    assert all_nums is not None, "all_nums must be a list"
    odd_nums = []
    even_nums = []

    for el in all_nums:
        if el % 2:
            odd_nums.append(el)
        else:
            even_nums.append(el)

    return even_nums, odd_nums


assert (np.allclose(sol_eq(1, 4, 4), (-2, -2)))
assert (sol_eq(-1, -3, -5) is np.nan)
assert (np.allclose(sol_eq(0, 3, 6), (-2, np.nan), equal_nan=True))
assert (sol_eq(0, 0, 1) is np.nan)

assert (div_par([1, 2, 3, 4, 5, 6]) == ([2, 4, 6], [1, 3, 5]))
assert (div_par([2, 2, 2, 2, 2]) == ([2, 2, 2, 2, 2], []))
assert (div_par([1]) == ([], [1]))
assert (div_par([]) == ([], []))
