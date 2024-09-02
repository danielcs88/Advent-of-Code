# %% [markdown]
# ## --- Day 18: Like a GIF For Your Yard ---
#
# After the [million lights incident](https://adventofcode.com/2015/day/6), the
# fire code has gotten stricter: now, at most ten thousand lights are allowed.
# You arrange them in a 100x100 grid.
#
# Never one to let you down, Santa again mails you instructions on the ideal
# lighting configuration. With so few lights, he says, you'll have to resort to
# **animation**.
#
# Start by setting your lights to the included initial configuration (your
# puzzle input). A `#` means "on", and a `.` means "off".
#
# Then, animate your grid in steps, where each step decides the next
# configuration based on the current one. Each light's next state (either on or
# off) depends on its current state and the current states of the eight lights
# adjacent to it (including diagonals). Lights on the edge of the grid might
# have fewer than eight neighbors; the missing ones always count as "off".
#
# For example, in a simplified 6x6 grid, the light marked `A` has the neighbors
# numbered `1` through `8`, and the light marked `B`, which is on an edge, only
# has the neighbors marked `1` through `5`:
#
# ```
# 1B5...
# 234...
# ......
# ..123.
# ..8A4.
# ..765.
# ```
#
# The state a light should have next is based on its current state (on or off)
# plus the **number of neighbors that are on**:
#
# - A light which is **on** stays on when `2` or `3` neighbors are on, and turns
#   off otherwise.
# - A light which is **off** turns on if exactly `3` neighbors are on, and stays
#   off otherwise.
#
# All of the lights update simultaneously; they all consider the same current
# state before moving to the next.
#
# Here's a few steps from an example configuration of another 6x6 grid:
#
# ```
# Initial state:
# .#.#.#
# ...##.
# #....#
# ..#...
# #.#..#
# ####..
#
# After 1 step:
# ..##..
# ..##.#
# ...##.
# ......
# #.....
# #.##..
#
# After 2 steps:
# ..###.
# ......
# ..###.
# ......
# .#....
# .#....
#
# After 3 steps:
# ...#..
# ......
# ...#..
# ..##..
# ......
# ......
#
# After 4 steps:
# ......
# ......
# ..##..
# ..##..
# ......
# ......
# ```
#
# After `4` steps, this example has four lights on.
#
# In your grid of 100x100 lights, given your initial configuration, **how many
# lights are on after 100 steps**?

# %%
import numpy as np
from scipy.ndimage import generic_filter

# from utilities import aoc_adjacent_coordinates, aoc_filter_valid_coordinates, aoc_grid

# %%
test = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

INPUT_18 = aoc_open_input("input_18.txt")


# %%
def state_of_light(neighbors: np.ndarray) -> bool:
    light = neighbors[4]
    on = np.sum(neighbors)
    return light and on in {3, 4} or not light and on == 3


def print_grid(grid: np.ndarray):
    for row in grid.tolist():
        print("".join([".#"[i] for i in row]))


def take_steps(
    grid: np.ndarray, steps: int, partb: bool = False, verbose: bool = False
):
    if verbose:
        print("Initial state:")
        print_grid(grid)
    for i in range(steps):
        new_grid = generic_filter(grid, state_of_light, size=3, mode="constant")
        if partb:
            new_grid[:: len(new_grid) - 1, :: len(new_grid[0]) - 1] = True
        if verbose:
            print()
            print(f"After step {i + 1}:")
            print_grid(new_grid)
        grid = new_grid
    return grid


def generate_grid(input_str: str) -> np.ndarray:
    return np.array(
        [[i == "#" for i in line] for line in input_str.splitlines()], dtype=bool
    )


# Example
test = """.#.#.#
...##.
#....#
..#...
#.#..#
####.."""

example_grid = generate_grid(test)
grid = take_steps(example_grid, 4, verbose=True)
print(np.sum(grid))

# %%
# part a
grid = generate_grid(INPUT_18)
print(np.sum(take_steps(grid, 100)))

# %% [markdown]
# ## --- Part Two ---
#
# You flip the instructions over; Santa goes on to point out that this is all
# just an implementation of [Conway's Game of
# Life](https://en.wikipedia.org/wiki/Conway's_Game_of_Life). At least, it was,
# until you notice that something's wrong with the grid of lights you bought:
# four lights, one in each corner, are **stuck on** and can't be turned off. The
# example above will actually run like this:
#
# ```
# Initial state:
# ##.#.#
# ...##.
# #....#
# ..#...
# #.#..#
# ####.#
#
# After 1 step:
# #.##.#
# ####.#
# ...##.
# ......
# #...#.
# #.####
#
# After 2 steps:
# #..#.#
# #....#
# .#.##.
# ...##.
# .#..##
# ##.###
#
# After 3 steps:
# #...##
# ####.#
# ..##.#
# ......
# ##....
# ####.#
#
# After 4 steps:
# #.####
# #....#
# ...#..
# .##...
# #.....
# #.#..#
#
# After 5 steps:
# ##.###
# .##..#
# .##...
# .##...
# #.#...
# ##...#
# ```
#
# After `5` steps, this example now has `17` lights on.
#
# In your grid of 100x100 lights, given your initial configuration, but with the
# four corners always in the **on** state, **how many lights are on after 100
# steps**?

# %%
test_2 = """##.#.#
...##.
#....#
..#...
#.#..#
####.#"""

# %%
np.sum(take_steps(generate_grid(test_2), 5, partb=True, verbose=True))

# %%
# part b
print(np.sum(take_steps(grid, 100, partb=True)))
