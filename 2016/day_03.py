# %% [markdown]
# ## --- Day 3: Squares With Three Sides ---
#
# Now that you can think clearly, you move deeper into the labyrinth of hallways
# and office furniture that makes up this part of Easter Bunny HQ. This must be
# a graphic design department; the walls are covered in specifications for
# triangles.
#
# Or are they?
#
# The design document gives the side lengths of each triangle it describes,
# but... `5 10 25`? Some of these aren't triangles. You can't help but mark the
# impossible ones.
#
# In a valid triangle, the sum of any two sides must be larger than the
# remaining side. For example, the "triangle" given above is impossible, because
# `5 + 10` is not larger than `25`.
#
# In your puzzle input, **how many** of the listed triangles are **possible**?

# %%
input_03 = aoc_open_input("input_03.txt")


# %%
def valid_triangle(triangle: list[int]) -> bool:
    a, b, c = triangle
    return a + b > c and b + c > a and c + a > b


# %%
def input_str_to_array(input_str: str) -> list[list[int]]:
    return [list(map(int, row.split())) for row in input_str.splitlines()]


# %%
def part_one(input_str: str) -> int:
    return sum(valid_triangle(l) for l in input_str_to_array(input_str))


# %%
aoc_answer_display(part_one(input_03))

# %% [markdown]
# ## --- Part Two ---
#
# Now that you've helpfully marked up their design documents, it occurs to you
# that triangles are specified in groups of three **vertically**. Each set of
# three numbers in a column specifies a triangle. Rows are unrelated.
#
# For example, given the following specification, numbers with the same hundreds
# digit would be part of the same triangle:
#
# ```
# 101 301 501
# 102 302 502
# 103 303 503
# 201 401 601
# 202 402 602
# 203 403 603
# ```
#
# In your puzzle input, and instead reading by columns, **how many** of the
# listed triangles are **possible**?

# %%
import itertools

# %%
example_02 = """101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603"""


# %%
def batched(iterable, n):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        yield batch


# %%
def aoc_transpose_list_of_lists(input_list: list[list]) -> list[list]:
    """
    Parameters
    ----------
    input_list : list[list[Any]]

    Returns
    -------
    list
    """
    return list(map(lambda *x: list(x), *(input_list)))


# %%
def part_two(input_str: str) -> int:
    return sum(
        valid_triangle(item)
        for column in aoc_transpose_list_of_lists(input_str_to_array(input_str))
        for item in batched(column, 3)
    )


# %%
aoc_answer_display(part_two(input_03))
