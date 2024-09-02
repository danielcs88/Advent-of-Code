# %% [markdown]
# ## --- Day 1: No Time for a Taxicab ---
#
# Santa's sleigh uses a very high\-precision clock to guide its movements, and
# the clock's oscillator is regulated by stars. Unfortunately, the stars have
# been stolen... by the Easter Bunny. To save Christmas, Santa needs you to
# retrieve all **fifty stars** by December 25th.
#
# Collect stars by solving puzzles. Two puzzles will be made available on each
# day in the Advent calendar; the second puzzle is unlocked when you complete
# the first. Each puzzle grants **one star**. Good luck!
#
# You're airdropped near **Easter Bunny Headquarters** in a city somewhere.
# "Near", unfortunately, is as close as you can get - the instructions on the
# Easter Bunny Recruiting Document the Elves intercepted start here, and nobody
# had time to work them out further.
#
# The Document indicates that you should start at the given coordinates (where
# you just landed) and face North. Then, follow the provided sequence: either
# turn left (`L`) or right (`R`) 90 degrees, then walk forward the given number
# of blocks, ending at a new intersection.
#
# There's no time to follow such ridiculous instructions on foot, though, so you
# take a moment and work out the destination. Given that you can only walk on
# the [street grid of the city](https://en.wikipedia.org/wiki/Taxicab_geometry),
# how far is the shortest path to the destination?
#
# For example:
#
# - Following `R2, L3` leaves you `2` blocks East and `3` blocks North, or `5`
#   blocks away.
# - `R2, R2, R2` leaves you `2` blocks due South of your starting position,
#   which is `2` blocks away.
# - `R5, L5, R5, R3` leaves you `12` blocks away.
#
# **How many blocks away** is Easter Bunny HQ?

# %%
examples = ("R2, L3", "R2, R2, R2", "R5, L5, R5, R3")

input_01 = aoc_open_input("input01.txt")
# aoc_answer_display(part_one(input_01))


# %%
def parse_instructions(input_str: str):
    return [[i[0], int(i[1:])] for i in input_str.split(", ")]


COMPASS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def part1(input_str: str) -> int:
    """
    Calculate the distance to Easter Bunny HQ.

    This function processes a series of directional instructions to determine
    the final position on a grid and calculates the Manhattan distance from the
    starting point. The instructions consist of turns and steps, which dictate
    how the position changes on the grid.

    Parameters
    ----------
    input_str : str
        A string containing directional instructions in the format "R2, L3",
        where each instruction consists of a turn (either 'R' for right or 'L'
        for left) followed by the number of steps to move forward.

    Returns
    -------
    int
        The Manhattan distance from the starting position to the final position
        after following the instructions.
    """
    direction = 0
    pos = (0, 0)

    for turn, steps in parse_instructions(input_str):
        direction = (direction + (1 if turn == "R" else -1)) % len(COMPASS)
        pos = tuple(p + d * steps for p, d in zip(pos, COMPASS[direction]))
    return sum(map(abs, pos))
    # return pos


# %%
def part2(input_str: str) -> int:
    """
    Calculate the distance to the first location visited twice.

    This function processes a series of directional instructions to determine
    the first location that is visited more than once on a grid and calculates
    the Manhattan distance from the starting point to that location. The
    instructions consist of turns and steps, which dictate how the position
    changes on the grid.

    Parameters
    ----------
    input_str : str
        A string containing directional instructions in the
        format "R2, L3", where each instruction consists of a turn (either
        'R' for right or 'L' for left) followed by the number of steps to
        move forward.

    Returns
    -------
    int
        The Manhattan distance from the starting position to the first
        location that is visited twice.
    """
    direction = 0
    current_position = (0, 0)

    points_visited = {current_position}

    for turn, steps in parse_instructions(input_str):
        direction = (direction + (1 if turn == "R" else -1)) % len(COMPASS)

        for _ in range(steps):
            dx, dy = COMPASS[direction]
            current_position = (current_position[0] + dx, current_position[1] + dy)

            if current_position in points_visited:
                return abs(current_position[0]) + abs(current_position[1])

            points_visited.add(current_position)


# %%
aoc_answer_display(part1(input_01))

# %%
aoc_answer_display(part2(input_01))
