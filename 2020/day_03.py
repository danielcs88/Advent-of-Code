# %% [markdown]
"""
\--- Day 3: Toboggan Trajectory ---
-----------------------------------

With the toboggan login problems resolved, you set off toward the airport. While
travel by toboggan might be easy, it's certainly not safe: there's very minimal
steering and the area is covered in trees. You'll need to see which angles will
take you near the fewest trees.

Due to the local geology, trees in this area only grow on exact integer
coordinates in a grid. You make a map (your puzzle input) of the open squares
(`.`) and trees (`#`) you can see. For example:

    ..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#


These aren't the only trees, though; due to something you read about once
involving arboreal genetics and biome stability, the same pattern repeats to the
right many times:

    ..##.........##.........##.........##.........##.........##.......  --->
    #...#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
    .#....#..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
    ..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
    .#...##..#..#...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
    ..#.##.......#.##.......#.##.......#.##.......#.##.......#.##.....  --->
    .#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
    .#........#.#........#.#........#.#........#.#........#.#........#
    #.##...#...#.##...#...#.##...#...#.##...#...#.##...#...#.##...#...
    #...##....##...##....##...##....##...##....##...##....##...##....#
    .#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#.#..#...#.#  --->


You start on the open square (`.`) in the top-left corner and need to reach the
bottom (below the bottom-most row on your map).

The toboggan can only follow a few specific slopes (you opted for a cheaper
model that prefers rational numbers); start by **counting all the trees** you
would encounter for the slope **right 3, down 1**:

From your starting position at the top-left, check the position that is right 3
and down 1. Then, check the position that is right 3 and down 1 from there, and
so on until you go past the bottom of the map.

The locations you'd check in the above example are marked here with `**O**`
where there was an open square and `**X**` where there was a tree:

    ..##.........##.........##.........##.........##.........##.......  --->
    #..O#...#..#...#...#..#...#...#..#...#...#..#...#...#..#...#...#..
    .#....X..#..#....#..#..#....#..#..#....#..#..#....#..#..#....#..#.
    ..#.#...#O#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#..#.#...#.#
    .#...##..#..X...##..#..#...##..#..#...##..#..#...##..#..#...##..#.
    ..#.##.......#.X#.......#.##.......#.##.......#.##.......#.##.....  --->
    .#.#.#....#.#.#.#.O..#.#.#.#....#.#.#.#....#.#.#.#....#.#.#.#....#
    .#........#.#........X.#........#.#........#.#........#.#........#
    #.##...#...#.##...#...#.X#...#...#.##...#...#.##...#...#.##...#...
    #...##....##...##....##...#X....##...##....##...##....##...##....#
    .#..#...#.#.#..#...#.#.#..#...X.#.#..#...#.#.#..#...#.#.#..#...#.#  --->


In this example, traversing the map using this slope would cause you to
encounter `**7**` trees.

Starting at the top-left corner of your map and following a slope of right 3 and
down 1, **how many trees would you encounter?**
"""


# %%
test_data = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""

# %%
list({len(i) for i in test_data.splitlines()})[0]

# %%
print(sorted(list(range(3, 11, 3))))
print(sorted(list(range(0, 11, 3))))
print(sorted(list(range(2, 11, 3))))

# %%
with open("input03.txt", "r") as file:
    data = file.read()

# %%
len(data.splitlines())

# %%
print(sorted(list(range(3, 31, 3))))

# %%
test = [sorted(list(range(3, 31, 3)))]

for _ in range(11):
    test.append(sorted(list(range(2, 31, 3))))
    test.append(sorted(list(range(1, 31, 3))))
    test.append(sorted(list(range(0, 31, 3))))

# %%
def flatten(t):
    return [item for sublist in t for item in sublist]

# %%
len(test)

# %%
len(flatten(test))

# %%
criteria = flatten(test)[:323]

# %%
from collections import Counter

Counter([d[c] for c, d in zip(criteria[:-1], data.splitlines()[1:])])

# %% [markdown]
"""
\--- Part Two ---
-----------------

Time to check the rest of the slopes - you need to minimize the probability of a
sudden arboreal stop, after all.

Determine the number of trees you would encounter if, for each of the following
slopes, you start at the top-left corner and traverse the map all the way to the
bottom:

- Right 1, down 1.
- Right 3, down 1. (This is the slope you already checked.)
- Right 5, down 1.
- Right 7, down 1.
- Right 1, down 2.

In the above example, these slopes would find `2`, `7`, `3`, `4`, and `2`
tree(s) respectively; multiplied together, these produce the answer `**336**`.

**What do you get if you multiply together the number of trees encountered on
each of the listed slopes?**
"""

# %%
import numpy as np

np.ceil(2.1)


# %%
def toboggan_trajectory(forest, x, y):
    """
    Traverses through "forest" and counts trees (#) found in trajectory.

    Parameters
    ----------
    forest : string
        The string containing the mapped grid of the forest.
    x : str
        The second parameter.s

    Returns
    -------
    Counter summary
        Counter summary of elements found
    """

    line_len = list({len(i) for i in forest.splitlines()})[0]

    # first_step
    steps = [sorted(list(range(x, line_len, x)))]

    # Last item on first step
    first_tail = steps[0][-1]

    def tail(x):
        return x[-1]

    def algo(tailed):
        return list(range(tailed + x - line_len, line_len, x))

    #     def factorial_recursion(n):
    #         init_vals = []
    #         if n == 1:
    #             return n
    #         else:
    #             return n * factorial_recursion(n - 1)

    #     test = [tail(x) for x in algo(first_tail)]

    #     init_vals = []

    #     test = {algo(first_tail)[0] for algo(first_tail)}

    int(np.ceil(len(forest.splitlines()) / line_len))

    #     for _ in range(range_num):
    #         steps.append(sorted(list(range(2, 31, 3))))
    #         steps.append(sorted(list(range(1, 31, 3))))
    #         steps.append(sorted(list(range(0, 31, 3))))

    return map(tail(first_tail), first_tail)


# %%
def count(dx, dy, lines):
    return len([1 for n, l in enumerate(lines[::dy]) if l[n * dx % len(l)] == "#"])


with open("input3.txt") as f:
    lines = f.read().splitlines()
print(count(3, 1, lines))
print(
    count(1, 1, lines)
    * count(3, 1, lines)
    * count(5, 1, lines)
    * count(7, 1, lines)
    * count(1, 2, lines)
)

# %%
m = [e for e in test.split()]


def count(m: list, r: int, b: int) -> int:
    w = len(m[0])
    p = 0
    c = 0
    for i in range(0, len(m), b):
        if m[i][p] == "#":
            c += 1
        p = (p + r) % w
    return c


print(count(m, 3, 1))

p = 1
for r, b in ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2)):
    p *= count(m, r, b)
print(p)

# %%
forest = data
x = 3

line_len = list({len(i) for i in forest.splitlines()})[0]
limit = line_len - 1

# first_step
steps = [sorted(list(range(x, line_len, x)))]

# Last item on first step
first_tail = steps[0][-1]

def tail(x):
    return x[-1]

def algo(tailed):
    return list(range(tailed + x - line_len, line_len, x))

range_num = int(np.ceil(len(forest.splitlines()) / line_len))


#     for _ in range(range_num):
#         steps.append(sorted(list(range(2, 31, 3))))
#         steps.append(sorted(list(range(1, 31, 3))))
#         steps.append(sorted(list(range(0, 31, 3))))
first_tail
