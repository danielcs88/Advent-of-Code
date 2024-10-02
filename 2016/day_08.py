# %% [markdown]
# ## --- Day 8: Two\-Factor Authentication ---
#
# You come across a door implementing what you can only assume is an
# implementation of [two\-factor
# authentication](https://en.wikipedia.org/wiki/Multi-factor_authentication)
# after a long game of [requirements](https://en.wikipedia.org/wiki/Requirement)
# [telephone](https://en.wikipedia.org/wiki/Chinese_whispers).
#
# To get past the door, you first swipe a keycard (no problem; there was one on
# a nearby desk). Then, it displays a code on a [little
# screen](https://www.google.com/search?q=tiny+lcd&tbm=isch), and you type that
# code on a keypad. Then, presumably, the door unlocks.
#
# Unfortunately, the screen has been smashed. After a few minutes, you've taken
# everything apart and figured out how it works. Now you just have to work out
# what the screen **would** have displayed.
#
# The magnetic strip on the card you swiped encodes a series of instructions for
# the screen; these instructions are your puzzle input. The screen is **`50`
# pixels wide and `6` pixels tall**, all of which start **off**, and is capable
# of three somewhat peculiar operations:
#
# - `rect AxB` turns **on** all of the pixels in a rectangle at the top\-left of
#   the screen which is `A` wide and `B` tall.
# - `rotate row y=A by B` shifts all of the pixels in row `A` (0 is the top row)
#   **right** by `B` pixels. Pixels that would fall off the right end appear at
#   the left end of the row.
# - `rotate column x=A by B` shifts all of the pixels in column `A` (0 is the
#   left column) **down** by `B` pixels. Pixels that would fall off the bottom
#   appear at the top of the column.
#
# For example, here is a simple sequence on a smaller screen:
#
# - `rect 3x2` creates a small rectangle in the top\-left corner:
#
# ```
# ###....
# ###....
# .......
# ```
# - `rotate column x=1 by 1` rotates the second column down by one pixel:
#
# ```
# #.#....
# ###....
# .#.....
# ```
# - `rotate row y=0 by 4` rotates the top row right by four pixels:
#
# ```
# ....#.#
# ###....
# .#.....
# ```
# - `rotate column x=1 by 1` again rotates the second column down by one pixel,
#   causing the bottom pixel to wrap back to the top:
#
# ```
# .#..#.#
# #.#....
# .#.....
# ```
#
# As you can see, this display technology is extremely powerful, and will soon
# dominate the tiny\-code\-displaying\-screen market. That's what the
# advertisement on the back of the display tries to convince you, anyway.
#
# There seems to be an intermediate check of the voltage used by the display:
# after you swipe your card, if the screen did work, **how many pixels should be
# lit?**

# %%
import time

import numpy as np

input_08 = aoc_open_input("input_08.txt")

example_instructions = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""

example_grid_dimensions = (3, 7)


# %%
def rotate_by_n(arr: np.ndarray, n: int, vector_index: int, vector: str) -> np.ndarray:
    result = arr.copy()

    if vector == "column":
        result[:, vector_index] = np.roll(arr[:, vector_index], n)
    elif vector == "row":
        result[vector_index, :] = np.roll(arr[vector_index, :], n)

    return result


# %%
def create_rect(arr: np.ndarray, width: int, height: int) -> np.ndarray:
    result = arr.copy()
    result[:height, :width] = 1
    return result


# %%
def parse_instructions(
    input_str: str, grid_size: tuple[int, int], part: int = 1
) -> int | np.ndarray:
    grid = np.zeros(grid_size[::-1])
    list_instructions = input_str.splitlines()

    for line in list_instructions:
        if line.startswith("rect"):
            width, height = map(int, line.split()[1].split("x"))
            grid = create_rect(grid, width=width, height=height)
        else:
            _, vector, vector_index, _, n = line.split()
            vector_index = int(vector_index.split("=")[1])
            n = int(n)
            grid = rotate_by_n(grid, n=n, vector_index=vector_index, vector=vector)
    return int(grid.sum()) if part == 1 else grid


# %%
parse_instructions(example_instructions, example_grid_dimensions, 2)

# %%
aoc_answer_display(parse_instructions(input_08, (50, 6)))


# %% [markdown]
# ## --- Part Two ---
#
# You notice that the screen is only capable of displaying capital letters; in the font it uses, each letter is `5` pixels wide and `6` tall.
#
# After you swipe your card, **what code is the screen trying to display?**


# %%
def illustrate_part_two(grid: np.ndarray) -> None:
    result = grid.copy().astype("str")

    filled = grid == 1.0
    result[filled] = "█"
    empty = grid == 0.0
    result[empty] = "░"

    for line in result:
        for char in line:
            print(char, end="")
            time.sleep(0.003)
        print()


# %%
illustrate_part_two(parse_instructions(input_08, (50, 6), 2))
