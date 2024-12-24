# %% [markdown]
# ## --- Day 4: Ceres Search ---
#
# "Looks like the Chief's not here. Next!" One of The Historians pulls out a
# device and pushes the only button on it. After a brief flash, you recognize
# the interior of the [Ceres monitoring
# station](https://adventofcode.com/2019/day/10)!
#
# As the search for the Chief continues, a small Elf who lives on the station
# tugs on your shirt; she'd like to know if you could help her with her **word
# search** (your puzzle input). She only has to find one word: `XMAS`.
#
# This word search allows words to be horizontal, vertical, diagonal, written
# backwards, or even overlapping other words. It's a little unusual, though, as
# you don't merely need to find one instance of `XMAS` - you need to find **all
# of them**. Here are a few ways `XMAS` might appear, where irrelevant
# characters have been replaced with `.`:
#
# ```
# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....
# ```
#
# The actual word search will be full of letters instead. For example:
#
# ```
# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX
# ```
#
# In this word search, `XMAS` occurs a total of `18` times; here's the same word
# search again, but where letters not involved in any `XMAS` have been replaced
# with `.`:
#
# ```
# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX
# ```
#
# Take a look at the little Elf's word search. **How many times does `XMAS`
# appear?**
#

# %%
import contextlib
import re

example = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

input_04 = aoc_open_input("input_04.txt")


# %%
def aoc_retrieve_diagonals(input_grid: str) -> str:
    grid = input_grid.splitlines()
    rows = len(grid)
    cols = len(grid[0])

    assert rows == cols, "Input Grid is not nxn"

    diagonals = []

    # Down-right diagonals
    for d in range(rows + cols - 1):
        diagonal = [
            grid[i][d - i] for i in range(max(d - cols + 1, 0), min(d + 1, rows))
        ]
        diagonals.append("".join(diagonal))

    # Up-right diagonals
    for d in range(rows + cols - 1):
        diagonal = [
            grid[rows - i - 1][d - i]
            for i in range(max(d - cols + 1, 0), min(d + 1, rows))
        ]
        diagonals.append("".join(diagonal))

    return "\n".join(diagonals)


# %%
def aoc_transpose_block_text(input_grid: str) -> str:
    return "\n".join("".join(i) for i in zip(*input_grid.split()))


# %%
@aoc_answer_display
def ceres_search(input_str: str) -> int:
    return sum(
        1
        for cases in (
            input_str,
            aoc_transpose_block_text(input_str),
            aoc_retrieve_diagonals(input_str),
        )
        for _ in re.finditer(r"(?=(XMAS|SAMX))", cases)
    )


# %%
# sourcery skip: remove-redundant-if, use-contextlib-suppress
ceres_search(input_04)

# %% [markdown]
# ## --- Part Two ---
#
# The Elf looks quizzically at you. Did you misunderstand the assignment?
#
# Looking for the instructions, you flip over the word search to find that this
# isn't actually an **XMAS** puzzle; it's an **X-MAS** puzzle in which you're
# supposed to find two MAS in the shape of an X. One way to achieve that is like
# this:
#
# ```
# M.S
# .A.
# M.S
# ```
#
# Irrelevant characters have again been replaced with . in the above diagram.
# Within the X, each MAS can be written forwards or backwards.
#
# Here's the same example from before, but this time all of the X-MASes have
# been kept instead:
#
# ```
# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........
# ```
# In this example, an X-MAS appears 9 times.
#
# Flip the word search from the instructions back over to the word search side
# and try again. **How many times does an X-MAS appear**?


# %%
def aoc_grid(test_string: str) -> dict:
    """
    Create a dictionary representing a grid from a string.

    Parameters
    ----------
    test_string : str
        Input string representing the grid.

    Returns
    -------
    dict
        A dictionary where keys are tuple coordinates (i, j) and values are
        corresponding characters from the grid.
    """

    return {
        (i, j): x
        for i, row in enumerate(test_string.splitlines())
        for j, x in enumerate(row)
        if x in {"S", "A", "M"}  # Only store relevant characters
    }


# %%
@aoc_answer_display
def x_mas_counts(input_str: str) -> int:
    grid = aoc_grid(input_str)
    counts = 0

    for key, value in grid.items():
        if value == "A":
            middle_row, middle_column = key

            top_row = middle_row - 1
            bottom_row = middle_row + 1

            left_col = middle_column - 1
            right_col = middle_column + 1

            with contextlib.suppress(KeyError):
                diagonal1 = (
                    f"{grid[top_row, left_col]}"
                    f"{grid[middle_row, middle_column]}"
                    f"{grid[bottom_row, right_col]}"
                )
                diagonal2 = (
                    f"{grid[top_row, right_col]}"
                    f"{grid[middle_row, middle_column]}"
                    f"{grid[bottom_row, left_col]}"
                )
                if (diagonal1 in ["SAM", "MAS"]) and (diagonal2 in ["SAM", "MAS"]):
                    counts += 1
    return counts


# %%
x_mas_counts(input_04)
