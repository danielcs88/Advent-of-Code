# %% [markdown]
# ## --- Day 3: Perfectly Spherical Houses in a Vacuum ---
# Santa is delivering presents to an infinite two-dimensional grid of houses.
#
# He begins by delivering a present to the house at his starting location, and
# then an elf at the North Pole calls him via radio and tells him where to move
# next. Moves are always exactly one house to the north (`^`), south (`v`), east
# (`>`), or west (`<`). After each move, he delivers another present to the
# house at his new location.
#
# However, the elf back at the north pole has had a little too much eggnog, and
# so his directions are a little off, and Santa ends up visiting some houses
# more than once. How many houses receive at least one present?
#
# For example:
#
# - `>` delivers presents to 2 houses: one at the starting location, and one to
#   `>` the east.
# - `^>v<` delivers presents to 4 houses in a square, including twice to the
#   house at his starting/ending location.
# - `^v^v^v^v^v` delivers a bunch of presents to some very lucky children at
#   only 2 houses.

# %%
input_03 = aoc_open_input("input_03.txt")
# %%
sorted(set(input_03))
# %%
test_cases = [">", "^>v<", "^v^v^v^v^v"]


# %%
def part_one(input_str: str) -> int:
    houses = {}
    x, y = 0, 0
    houses[(x, y)] = 1

    for sign in input_str:
        match sign:
            case "<":
                x -= 1
            case ">":
                x += 1
            case "^":
                y += 1
            case "v":
                y -= 1
        houses[(x, y)] = 1
    return len(houses)


# %%
{t: part_one(t) for t in test_cases}

# %%
part_one(input_03)

# %% [markdown]
# ## --- Part Two ---
#
# The next year, to speed up the process, Santa creates a robot version of
# himself, **Robo-Santa**, to deliver presents with him.
#
# Santa and Robo-Santa start at the same location (delivering two presents to
# the same starting house), then take turns moving based on instructions from
# the elf, who is eggnoggedly reading from the same script as the previous year.
#
# This year, how many houses receive **at least one present**?
#
# For example:
#
# - `^v` delivers presents to `3` houses, because Santa goes north, and then
#   Robo-Santa goes south.
# - `^>v<` now delivers presents to `3` houses, and Santa and Robo-Santa end up
#   back where they started.
# - `^v^v^v^v^v` now delivers presents to `11` houses, with Santa going one
#   direction and Robo-Santa going the other.


# %%
def part_two_simple(input_str: str) -> dict[tuple[int, int], int]:
    houses = {}
    x, y = 0, 0
    houses[(x, y)] = 1

    for sign in input_str:
        match sign:
            case "<":
                x -= 1
            case ">":
                x += 1
            case "^":
                y += 1
            case "v":
                y -= 1
        houses[(x, y)] = 1
    return houses


def part_two_chatgpt(input_str: str) -> int:
    def move(x: int, y: int, direction: str) -> tuple[int, int]:
        moves = {"<": (-1, 0), ">": (1, 0), "^": (0, 1), "v": (0, -1)}
        dx, dy = moves[direction]
        return x + dx, y + dy

    def visit_houses(instructions: str) -> set[tuple[int, int]]:
        houses = {(0, 0)}
        x, y = 0, 0
        for sign in instructions:
            x, y = move(x, y, sign)
            houses.add((x, y))
        return houses

    santa_houses = visit_houses(input_str[::2])
    robo_houses = visit_houses(input_str[1::2])

    return len(santa_houses | robo_houses)


# %%
{t: part_two_chatgpt(t) for t in ["^v", "^>v<", "^v^v^v^v^v"]}

# %%
part_one(input_03[::2]) + part_one(input_03[1::2])
# %%
part_two_chatgpt(input_03)
# %%
part_two(input_03)


# %%
len(part_two_simple(input_03[::2]) | part_two_simple(input_03[1::2]))
