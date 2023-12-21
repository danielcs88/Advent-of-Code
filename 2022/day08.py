# %% [markdown]
# ## --- Day 8: Treetop Tree House ---
#
# The expedition comes across a peculiar patch of tall trees all planted
# carefully in a grid. The Elves explain that a previous expedition planted
# these trees as a reforestation effort. Now, they're curious if this would be a
# good location for a [tree house](https://en.wikipedia.org/wiki/Tree_house).
#
# First, determine whether there is enough tree cover here to keep a tree house
# **hidden**. To do this, you need to count the number of trees that are
# **visible from outside the grid** when looking directly along a row or column.
#
# The Elves have already launched a
# [quadcopter](https://en.wikipedia.org/wiki/Quadcopter) to generate a map with
# the height of each tree (your puzzle input). For example:
#
# ```
# 30373
# 25512
# 65332
# 33549
# 35390
# ```
#
# Each tree is represented as a single digit whose value is its height, where
# `0` is the shortest and `9` is the tallest.
#
# A tree is **visible** if all of the other trees between it and an edge of the
# grid are **shorter** than it. Only consider trees in the same row or column;
# that is, only look up, down, left, or right from any given tree.
#
# All of the trees around the edge of the grid are **visible** - since they are
# already on the edge, there are no trees to block the view. In this example,
# that only leaves the **interior nine trees** to consider:
#
# - The top-left `5` is **visible** from the left and top. (It isn't visible
#   from the right or bottom since other trees of height `5` are in the way.)
# - The top-middle `5` is **visible** from the top and right.
# - The top-right `1` is not visible from any direction; for it to be visible,
#   there would need to only be trees of height **0** between it and an edge.
# - The left-middle `5` is **visible**, but only from the right.
# - The center `3` is not visible from any direction; for it to be visible,
#   there would need to be only trees of at most height `2` between it and an
#   edge.
# - The right-middle `3` is **visible** from the right.
# - In the bottom row, the middle `5` is **visible**, but the `3` and `4` are
#   not.
#
# With 16 trees visible on the edge and another 5 visible in the interior, a
# total of **`21`** trees are visible in this arrangement.
#
# Consider your map; **how many trees are visible from outside the grid?**
#

# %%
import pprint
from math import prod

from utils import open_input, three_dimensional_array

test = """30373
25512 65332 33549 35390"""


def array_grid(grid):
    grid.find("\n")
    # entire_grid_size = n**2 interior_grid_size = (n - 2) ** 2 perimeter_length
    # = n**2 - interior_grid_size
    return [list(map(int, str(x))) for x in grid.splitlines()]


def part_one(grid: str, verbose=False) -> int:
    n = grid.find("\n")
    interior_grid_size = (n - 2) ** 2
    perimeter_length = n**2 - interior_grid_size
    visible = perimeter_length
    array = [list(map(int, str(x))) for x in grid.splitlines()]
    interior_range = range(1, n - 1)

    for y in interior_range:
        for x in interior_range:

            up = max(col[x] for col in array[:y])
            left = max(array[y][:x])

            down = max(col[x] for col in array[y + 1 :])
            right = max(array[y][x + 1 :])

            current_position = array[y][x]

            if any(current_position > quadrant for quadrant in [up, left, down, right]):
                visible += 1

                if verbose:
                    print("Visible")

            elif verbose:
                print("Not visible")

            if verbose:
                pprint.pprint(array)
                print(y, x)
                print(f"  {up}\n{left} {current_position} {right}\n  {down}")
                print()

    return visible


# %%
print(part_one(test))

# %% from aocd import get_data

# input_08 = get_data(day=8, year=2022)

input_08 = open_input("input_08.txt")

# %% %%time
print(part_one(input_08))


# %% [markdown]
# ## --- Part Two ---
#
# Content with the amount of tree cover available, the Elves just need to know
# the best spot to build their tree house: they would like to be able to see a
# lot of **trees**.
#
# To measure the viewing distance from a given tree, look up, down, left, and
# right from that tree; stop if you reach an edge or at the first tree that is
# the same height or taller than the tree under consideration. (If a tree is
# right on the edge, at least one of its viewing distances will be zero.)
#
# The Elves don't care about distant trees taller than those found by the rules
# above; the proposed tree house has large
# [eaves](https://en.wikipedia.org/wiki/Eaves) to keep it dry, so they wouldn't
# be able to see higher than the tree house anyway.
#
# In the example above, consider the middle `5` in the second row:
#
# <pre><code>30373
# 25<span style="color: #3366ff; background-color: #ffff00;"><strong>5</strong></span>12
# 65332
# 33549
# 35390</code></pre>
#
# - Looking up, its view is not blocked; it can see **`1`** tree (of height
#   `3`).
# - Looking left, its view is blocked immediately; it can see only **`1`** tree
#   (of height `5`, right next to it).
# - Looking right, its view is not blocked; it can see **`2`** trees.
# - Looking down, its view is blocked eventually; it can see **`2`** trees (one
#   of height `3`, then the tree of height `5` that blocks its view).
#
# A tree's **scenic score** is found by **multiplying together** its viewing
# distance in each of the four directions. For this tree, this is **`4`** (found
# by multiplying `1 ** 1 ** 2 ** 2`).
#
# However, you can do even better: consider the tree of height `5` in the middle
# of the fourth row:
#
# <pre><code>30373
# 25512
# 65332
# 33<span style="text-decoration: underline; background-color: #00ffff; color: #ff0000;"><strong>5</strong></span>49
# 35390</code></pre>
#
# - Looking up, its view is blocked at **`2`** trees (by another tree with a
#   height of `5`).
# - Looking left, its view is not blocked; it can see **`2`** trees.
# - Looking down, its view is also not blocked; it can see **`1`** tree.
# - Looking right, its view is blocked at **`2`** trees (by a massive tree of
#   height `9`).
#
# This tree's scenic score is **`8`** (`2 * 2 * 1 * 2`); this is the ideal spot
# for the tree house.
#
# Consider each tree on your map. **What is the highest scenic score possible
# for any tree?**

# %%
def part_two(grid: str) -> list:
    n = grid.find("\n")
    array = [list(map(int, str(x))) for x in grid.splitlines()]
    interior_range = range(1, n - 1)
    scenic_scores = three_dimensional_array(n - 2, n - 2, 4)

    for x in interior_range:
        for y in interior_range:
            up = list(reversed([col[y] for col in array[:x]]))
            left = list(reversed(array[x][:y]))

            down = [col[y] for col in array[x + 1 :]]
            right = array[x][y + 1 :]

            current_position = array[x][y]

            for n, quadrant in enumerate([up, left, down, right]):
                # print(y-1, x-1)
                current_bool = [current_position > element for element in quadrant]
                # print(n)
                scenic_scores[y - 1][x - 1][n] = current_bool

    return scenic_scores


# %%
def height_score(entry: list) -> int:
    scores = []
    for x in entry:
        try:
            score = x.index(False) + 1
            scores.append(score)
        except ValueError:
            score = sum(x)
            scores.append(score)
    # return scores
    return prod(scores)


# %%
def get_max_score(scores):
    tally = []
    for x in range(len(scores)):
        tally.extend(height_score(scores[y][x]) for y in range(len(scores)))
    return max(tally)


# %%
print(get_max_score(part_two(test)))

# %%
print(get_max_score(part_two(input_08)))
