# %% [markdown]
# ## --- Day 15: Science for Hungry People ---
#
# Today, you set out on the task of perfecting your milk-dunking cookie recipe.
# All you have to do is find the right balance of ingredients.
#
# Your recipe leaves room for exactly `100` teaspoons of ingredients. You make a
# list of the **remaining ingredients you could use to finish the recipe** (your
# puzzle input) and their **properties per teaspoon**:
#
# - `capacity` (how well it helps the cookie absorb milk)
# - `durability` (how well it keeps the cookie intact when full of milk)
# - `flavor` (how tasty it makes the cookie)
# - `texture` (how it improves the feel of the cookie)
# - `calories` (how many calories it adds to the cookie)
#
# You can only measure ingredients in whole-teaspoon amounts accurately, and you
# have to be accurate so you can reproduce your results in the future. The
# **total score** of a cookie can be found by adding up each of the properties
# (negative totals become `0`) and then multiplying together everything except
# calories.
#
# For instance, suppose you have these two ingredients:
#
# ```
# Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
# Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3
# ```
#
# Then, choosing to use `44` teaspoons of butterscotch and `56` teaspoons of
# cinnamon (because the amounts of each ingredient must add up to `100`) would
# result in a cookie with the following properties:
#
# - A `capacity` of $44 \cdot -1 + 56 \cdot 2 = 68$
# - A `durability` of $44 \cdot -2 + 56 \cdot 3 = 80$
# - A `flavor` of $44 \cdot 6 + 56 \cdot -2 = 152$
# - A `texture` of $44 \cdot 3 + 56 \cdot -1 = 76$
#
# Multiplying these together (`68 * 80 * 152 * 76`, ignoring `calories` for
# now) results in a total score of `62842880`, which happens to be the best
# score possible given these ingredients. If any properties had produced a
# negative total, it would have instead become zero, causing the whole score to
# multiply to zero.
#
# Given the ingredients in your kitchen and their properties, what is the
# **total score** of the highest-scoring cookie you can make?

# %%
test = """Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""

INPUT_15 = aoc_open_input("input_15.txt")

# %%
import re

import numpy as np
import pandas as pd


def ingredient_stats(input_str: str, verbose: bool = True):
    regex = re.compile(
        r"(\w+): capacity (-?\d), durability (-?\d), flavor (-?\d), texture (-?\d), calories (-?\d)"
    )

    matches = regex.findall(input_str)

    data = {}

    for i in matches:
        name = i[0]
        scores = map(int, i[1:])
        data[name] = dict(
            zip(["capacity", "durability", "flavor", "texture", "calories"], scores)
        )
    return pd.DataFrame(data) if verbose else data


# %%
from itertools import permutations


def find_permutations(numbers, target_sum: int, factors: int):
    return np.fromiter(
        (comb for comb in permutations(numbers, factors) if sum(comb) == target_sum),
        dtype=np.dtype((int, factors)),
    )


# %%
def max_total_score(ingredient_data: pd.DataFrame, verbose: bool = False) -> int:
    factor_count = ingredient_data.shape[1]
    perms = find_permutations(range(101), 100, factor_count)
    return (
        pd.DataFrame(
            np.dot(
                perms,
                ingredient_data.T.values,
            ),
            index=map(tuple, perms),
            columns=ingredient_data.index,
        )
        .map(lambda x: max(x, 0))
        .prod(axis=1)
        .pipe(lambda d: d.pipe(z_descriptive_min_max, "max") if verbose else d.max())
    )


# %%
def part_one(input_str: str, verbose: bool = False) -> int:
    COOKIE_DATA = ingredient_stats(input_str).iloc[:4]
    return max_total_score(COOKIE_DATA, verbose)


# %%
aoc_answer_display(part_one(test))
part_one(test, True)

# %%
aoc_answer_display(part_one(INPUT_15))
part_one(INPUT_15, True)


# %% [markdown]
# ## --- Part Two ---
#
# Your cookie recipe becomes wildly popular! Someone asks if you can make
# another recipe that has exactly `500` calories per cookie (so they can use it
# as a meal replacement). Keep the rest of your award-winning process the same
# (100 teaspoons, same ingredients, same scoring system).
#
# For example, given the ingredients above, if you had instead selected `40`
# teaspoons of butterscotch and `60` teaspoons of cinnamon (which still adds to
# `100`), the total calorie count would be `40*8 + 60*3 = 500`. The total score
# would go down, though: only `57600000`, the best you can do in such trying
# circumstances.
#
# Given the ingredients in your kitchen and their properties, what is the *total
# score* of the highest-scoring cookie you can make with a calorie total of
# `500`?

# %%
def max_total_score_with_calorie_restriction(
    ingredient_data: pd.DataFrame, calorie_restriction: int = 500, verbose: bool = False
) -> int:
    factor_count = ingredient_data.shape[1]
    perms = find_permutations(range(101), 100, factor_count)
    return (
        pd.DataFrame(
            np.dot(
                perms,
                ingredient_data.T.values,
            ),
            index=map(tuple, perms),
            columns=ingredient_data.index,
        )
        .map(lambda x: max(x, 0))
        .loc[lambda d: d["calories"] == calorie_restriction]
        .iloc[:, :4]
        .prod(axis=1)
        .pipe(lambda d: d.pipe(z_descriptive_min_max, "max") if verbose else d.max())
    )


# %%
def part_two(input_str: str, verbose: bool = False) -> int:
    COOKIE_DATA = ingredient_stats(input_str)
    return max_total_score_with_calorie_restriction(COOKIE_DATA, 500, verbose)


# %%
aoc_answer_display(part_two(test, False))
part_two(test, True)

# %%
aoc_answer_display(part_two(INPUT_15))
part_two(INPUT_15, True)
