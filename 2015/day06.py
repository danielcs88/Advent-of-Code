# %% [markdown]
# ## --- Day 6: Probably a Fire Hazard ---
#
# Because your neighbors keep defeating you in the holiday house decorating
# contest year after year, you've decided to deploy one million lights in a
# 1000x1000 grid.
#
# Furthermore, because you've been especially nice this year, Santa has mailed
# you instructions on how to display the ideal lighting configuration.
#
# Lights in your grid are numbered from 0 to 999 in each direction; the lights
# at each corner are at `0,0`, `0,999`, `999,999`, and `999,0`. The instructions
# include whether to `turn on`, `turn off`, or `toggle` various inclusive ranges
# given as coordinate pairs. Each coordinate pair represents opposite corners of
# a rectangle, inclusive; a coordinate pair like `0,0 through 2,2` therefore
# refers to 9 lights in a 3x3 square. The lights all start turned off.
#
# To defeat your neighbors this year, all you have to do is set up your lights
# by doing the instructions Santa sent you in order.
#
# For example:
#
# - `turn on 0,0 through 999,999` would turn on (or leave on) every light.
# - `toggle 0,0 through 999,0` would toggle the first line of 1000 lights,
#   turning off the ones that were on, and turning on the ones that were off.
# - `turn off 499,499 through 500,500` would turn off (or leave off) the middle
#   four lights.
#
# After following the instructions, **how many lights are lit**?

# %%
import numpy as np
import pyperclip

# %%
input_06 = aoc_open_input("input_06.txt")


# %%
def operation_map(bulb: bool, operation_instruct: str) -> bool:
    instructions = {"on": True, "toggle": not bulb, "off": False}
    return instructions[operation_instruct]


def part_one(input_str: str) -> int:
    lights: dict[tuple[int, int], bool] = aoc_grid_dictionary(
        grid_size=1000, default_value=False
    )
    for line in input_str.replace("turn ", "").splitlines():
        operation, start, _, end = line.split()
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                current_bulb = lights[(x, y)]
                lights[(x, y)] = operation_map(
                    bulb=current_bulb, operation_instruct=operation
                )
    result = sum(lights.values())
    pyperclip.copy(result)
    return result


# %%
def part_one_np(input_str: str) -> int:
    lights = np.full((1000, 1000), 0)

    for line in input_str.replace("turn ", "").splitlines():
        operation, start, _, end = line.split()
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))

        if operation == "on":
            lights[start_x : end_x + 1, start_y : end_y + 1] = 1
        elif operation == "off":
            lights[start_x : end_x + 1, start_y : end_y + 1] = 0
        elif operation == "toggle":
            lights[start_x : end_x + 1, start_y : end_y + 1] = (
                1 - lights[start_x : end_x + 1, start_y : end_y + 1]
            )

    result = lights.sum()
    pyperclip.copy(int(result))
    print(result)
    return result


# %%
part_one_np(input_06)


# %% [markdown]
# ## --- Part Two ---
#
# You just finish implementing your winning light pattern when you realize you mistranslated Santa's message from Ancient Nordic Elvish.
#
# The light grid you bought actually has individual brightness controls; each light can have a brightness of zero or more. The lights all start at zero.
#
# The phrase `turn on` actually means that you should increase the brightness of those lights by `1`.
#
# The phrase `turn off` actually means that you should decrease the brightness of those lights by `1`, to a minimum of zero.
#
# The phrase `toggle` actually means that you should increase the brightness of those lights by `2`.
#
# What is the **total brightness** of all lights combined after following Santa's instructions?
#
# For example:
#
# - `turn on 0,0 through 0,0` would increase the total brightness by `1`.
# - `toggle 0,0 through 999,999` would increase the total brightness by `2000000`.

# %%
def part_two_np(input_str: str) -> int:
    lights = np.full((1000, 1000), 0)

    for line in input_str.replace("turn ", "").splitlines():
        operation, start, _, end = line.split()
        start_x, start_y = map(int, start.split(","))
        end_x, end_y = map(int, end.split(","))

        if operation == "on":
            lights[start_x : end_x + 1, start_y : end_y + 1] = (
                1 + lights[start_x : end_x + 1, start_y : end_y + 1]
            )
        elif operation == "off":
            lights[start_x : end_x + 1, start_y : end_y + 1] = np.maximum(
                lights[start_x : end_x + 1, start_y : end_y + 1] - 1, 0
            )
        elif operation == "toggle":
            lights[start_x : end_x + 1, start_y : end_y + 1] = (
                2 + lights[start_x : end_x + 1, start_y : end_y + 1]
            )

    result = lights.sum()
    pyperclip.copy(int(result))
    print(result)
    return result


# %%
part_two_np(input_06)
