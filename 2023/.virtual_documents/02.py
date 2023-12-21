


import io

import pandas as pd
import polars as pl
import polars.selectors as cs

test_1 = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""


MAX_COLOR_COUNTS = {"red": 12, "green": 13, "blue": 14}


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


pl_game_set("input_02.txt").pipe(pl_part_one)


pl_game_set(io.StringIO(test_1))


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


pd_game_set("input_02.txt").pipe(check_valid_game_counts_per_set)


get_ipython().run_line_magic("time", " pl_game_set(\"input_02.txt\").pipe(pl_part_one)")


get_ipython().run_line_magic("time", " pd_game_set(\"input_02.txt\").pipe(check_valid_game_counts_per_set)")






