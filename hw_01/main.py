def sol_eq(a, b, c):
    assert None not in (a, b, c), "a, b, c must be numbers"
    d = b ** 2 - 4 * a * c

    if d < 0:
        return None

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