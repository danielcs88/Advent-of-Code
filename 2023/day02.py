# %% [markdown]
# ## --- Day 2: Cube Conundrum ---
#
# You're launched high into the atmosphere! The apex of your trajectory just
# barely reaches the surface of a large island floating in the sky. You gently
# land in a fluffy pile of leaves. It's quite cold, but you don't see much snow.
# An Elf runs over to greet you.
#
# The Elf explains that you've arrived at *Snow Island* and apologizes for the
# lack of snow. He'll be happy to explain the situation, but it's a bit of a
# walk, so you have some time. They don't get many visitors up here; would you
# like to play a game in the meantime?
#
# As you walk, the Elf shows you a small bag and some cubes which are either
# red, green, or blue. Each time you play this game, he will hide a secret
# number of cubes of each color in the bag, and your goal is to figure out
# information about the number of cubes.
#
# To get information, once a bag has been loaded with cubes, the Elf will reach
# into the bag, grab a handful of random cubes, show them to you, and then put
# them back in the bag. He'll do this a few times per game.
#
# You play several games and record the information from each game (your puzzle
# input). Each game is listed with its ID number (like the `11` in `Game 11:
# ...`) followed by a semicolon-separated list of subsets of cubes that were
# revealed from the bag (like `3 red, 5 green, 4 blue`).
#
# For example, the record of a few games might look like this:
#
# ```
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# ```
#
# In game 1, three sets of cubes are revealed from the bag (and then put back
# again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red
# cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.
#
# The Elf would first like to know which games would have been possible if the
# bag contained *only 12 red cubes, 13 green cubes, and 14 blue cubes*?
#
# In the example above, games 1, 2, and 5 would have been *possible* if the bag
# had been loaded with that configuration. However, game 3 would have been
# *impossible* because at one point the Elf showed you 20 red cubes at once;
# similarly, game 4 would also have been *impossible* because the Elf showed you
# 15 blue cubes at once. If you add up the IDs of the games that would have been
# possible, you get **`8`**.
#
# Determine which games would have been possible if the bag had been loaded with
# only 12 red cubes, 13 green cubes, and 14 blue cubes. *What is the sum of the
# IDs of those games?*


# %%
import io

import pandas as pd
import polars as pl
import polars.selectors as cs

test_1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


# %%
MAX_COLOR_COUNTS = {"red": 12, "green": 13, "blue": 14}


# %%
def pl_game_set(input_str: str) -> pl.DataFrame:
    return (
        pl.read_csv(input_str, has_header=False, separator="\n")
        .with_columns(pl.col("column_1").str.split(": "))
        .select(
            (
                pl.col("column_1")
                .list[0]
                .str.replace("Game ", "")
                .cast(pl.Int32)
                .alias("id_game")
            ),
            pl.col("column_1").list[1].alias("sets").str.split("; "),
        )
        .explode("sets")
        .with_columns(pl.lit(1).alias("id_set"))
        .with_columns(pl.col("id_set").cum_sum().over("id_game"))
        .with_columns(pl.col("sets").str.split(", "))
        .explode("sets")
        .with_columns(pl.col("sets").str.extract_groups(r"(\d+) ([a-zA-Z]+)"))
        .unnest("sets")
        .rename({"1": "value", "2": "color"})
        .with_columns(pl.col("value").cast(pl.Int64))
        .pivot(index=["id_game", "id_set"], columns="color", values="value")
        .fill_null(0)
    )


# %%
def pl_part_one(df: pl.DataFrame) -> pd.DataFrame:
    return (
        df.pipe(
            lambda x: (
                x.with_columns(
                    [
                        pl.col(color).le(MAX_COLOR_COUNTS[color])
                        for color in x.select(~cs.contains("id")).columns
                    ]
                ).with_columns(
                    pl.fold(
                        acc=pl.lit(True),
                        function=lambda s1, s2: s1 & s2,
                        exprs=~cs.contains("id"),
                    ).alias("is_valid")
                )
            )
        )
        .group_by("id_game", maintain_order=True)
        .agg(pl.col("is_valid").all())
        .filter(pl.col("is_valid"))
        .sum()
    )


# %%
pl_game_set("input_02.txt").pipe(pl_part_one)
# %%
pl_game_set(io.StringIO(test_1))


# %%
def pd_game_set(input_str: str) -> pd.DataFrame:
    return (
        (
            pd.read_csv(input_str, header=None, sep=r"\n", engine="python")
            .assign(column_1=lambda d: d[0].str.split(": "))
            .loc[:, ["column_1"]]
        )
        .assign(
            id_game=(
                lambda d: d["column_1"]
                .map(lambda x: x[0])
                .str.replace("Game ", "")
                .astype("int8")
            ),
            sets=lambda d: d["column_1"].map(lambda x: x[1]).str.split("; "),
        )
        .loc[:, ["id_game", "sets"]]
        .explode("sets")
        .assign(
            id_set=lambda d: d.groupby("id_game").transform("cumcount") + 1,
            sets=lambda d: d["sets"].str.split(", "),
        )
        .explode("sets")
        .pipe(
            lambda d: pd.concat(
                [
                    d,
                    (
                        d["sets"]
                        .str.split(" ", expand=True)
                        .set_axis(["value", "color"], axis="columns")
                    ),
                ],
                axis=1,
            )
        )
        .astype({"value": "int"})
        .pivot_table(
            index=["id_game", "id_set"], columns="color", values="value", fill_value=0
        )
        .reset_index()
        .set_axis(["id_game", "id_set", "blue", "green", "red"], axis="columns")
        .loc[:, ["id_game", "id_set", "red", "green", "blue"]]
        .set_index(["id_game", "id_set"])
    )


# %%
def check_valid_game_counts_per_set(df: pd.DataFrame):
    return (
        (
            (df <= df.assign(**MAX_COLOR_COUNTS))
            .assign(is_valid=lambda d: d.all(axis=1))
            .reset_index()
        )
        .groupby("id_game", as_index=False)
        .agg({"is_valid": "all"})
        .loc[lambda d: d["is_valid"]]
        .agg("sum")
    )


# %%
pd_game_set("input_02.txt").pipe(check_valid_game_counts_per_set)

# %%
# %time pl_game_set("input_02.txt").pipe(pl_part_one)

# %%
# %time pd_game_set("input_02.txt").pipe(check_valid_game_counts_per_set)

# %% [markdown]
# ## --- Part Two ---
#
# The Elf says they've stopped producing snow because they aren't getting any
# *water*! He isn't sure why the water stopped; however, he can show you how to
# get to the water source to check it out for yourself. It's just up ahead!
#
# As you continue your walk, the Elf poses a second question: in each game you
# played, what is the **fewest number of cubes of each color** that could have
# been in the bag to make the game possible?
#
# Again consider the example games from earlier:
#
# ```
# Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
# Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
# Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
# Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
# Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
# ```
#
# - In game 1, the game could have been played with as few as 4 red, 2 green,
#   and 6 blue cubes. If any color had even one fewer cube, the game would have
#   been impossible.
# - Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue
#   cubes.
# -
# - Game 3 must have been played with at least 20 red, 13 green, and 6 blue
#   cubes.
# - Game 4 required at least 14 red, 3 green, and 15 blue cubes.
# - Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
#
# The **power** of a set of cubes is equal to the numbers of red, green, and
# blue cubes multiplied together. The power of the minimum set of cubes in game
# 1 is `48`. In games 2-5 it was `12`, `1560`, `630`, and `36`, respectively.
# Adding up these five powers produces the sum **`2286`**.
#
# For each game, find the minimum set of cubes that must have been present.
# **What is the sum of the power of these sets?**


# %%
def pl_part_two(df: pl.DataFrame) -> int:
    return (
        df.group_by("id_game", maintain_order=True)
        .agg(pl.all().max())
        .select(~cs.contains("id"))
        .fold(lambda s1, s2: s1 * s2)
        .sum()
    )


# %%
pl_game_set("input_02.txt").pipe(pl_part_two)


# %%
def pd_part_two(df: pd.DataFrame) -> int:
    return df.groupby("id_game").agg("max").prod(axis=1).sum().astype("int")


# %%
pd_game_set("input_02.txt").pipe(pd_part_two)


# %%
def p1(f: list[str]) -> int:
    ans = 0
    for line in f:
        game_id, game = line.split(": ")
        for game_set in game.split("; "):
            colors = [x.split() for x in game_set.split(", ")]
            counts = {b: int(a) for a, b in colors}
            if not (
                counts.get("red", 0) <= 12
                and counts.get("green", 0) <= 13
                and counts.get("blue", 0) <= 14
            ):
                break
        else:
            ans += int(game_id.split()[-1])
    return ans


def p2(f: list[str]) -> int:
    ans = 0
    for line in f:
        _, game = line.split(": ")
        needed = {"red": 0, "green": 0, "blue": 0}
        for game_set in game.split("; "):
            colors = [x.split() for x in game_set.split(", ")]
            counts = {b: int(a) for a, b in colors}
            needed["red"] = max(needed["red"], counts.get("red", 0))
            needed["green"] = max(needed["green"], counts.get("green", 0))
            needed["blue"] = max(needed["blue"], counts.get("blue", 0))
        ans += needed["red"] * needed["green"] * needed["blue"]
    return ans


# %%
p1(aoc_open_input("input_02.txt").splitlines())

# %%
p2(aoc_open_input("input_02.txt").splitlines())
