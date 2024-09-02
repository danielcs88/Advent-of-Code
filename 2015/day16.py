# %% [markdown]
# ## --- Day 16: Aunt Sue ---
#
# Your Aunt Sue has given you a wonderful gift, and you'd like to send her a
# thank you card. However, there's a small problem: she signed it "From, Aunt
# Sue".
#
# You have 500 Aunts named "Sue".
#
# So, to avoid sending the card to the wrong person, you need to figure out
# which Aunt Sue (which you conveniently number 1 to 500, for sanity) gave you
# the gift. You open the present and, as luck would have it, good ol' Aunt Sue
# got you a My First Crime Scene Analysis Machine! Just what you wanted. Or
# needed, as the case may be.
#
# The My First Crime Scene Analysis Machine (MFCSAM for short) can detect a few
# specific compounds in a given sample, as well as how many distinct kinds of
# those compounds there are. According to the instructions, these are what the
# MFCSAM can detect:
#
# - `children`, by human DNA age analysis.
# - `cats`. It doesn't differentiate individual breeds.
# - Several seemingly random breeds of dog: `samoyeds`, `pomeranians`, `akitas`,
#   and `vizslas`.
# - `goldfish`. No other kinds of fish.
# - `trees`, all in one group.
# - `cars`, presumably by exhaust or gasoline or something.
# - `perfumes`, which is handy, since many of your Aunts Sue wear a few kinds.
#
# In fact, many of your Aunts Sue have many of these. You put the wrapping from
# the gift into the MFCSAM. It beeps inquisitively at you a few times and then
# prints out a message on [ticker
# tape](https://en.wikipedia.org/wiki/Ticker_tape):
#
# ```
# children: 3
# cats: 7
# samoyeds: 2
# pomeranians: 3
# akitas: 0
# vizslas: 0
# goldfish: 5
# trees: 3
# cars: 2
# perfumes: 1
# ```
#
# You make a list of the things you can remember about each Aunt Sue. Things
# missing from your list aren't zero - you simply don't remember the value.
#
# What is the **number** of the Sue that got you the gift?

# %%
import re

# %%
ticker_tape = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

INPUT_16 = aoc_open_input("input_16.txt")


# %%
def generate_sue_dict(input_str: str) -> dict[int, dict[str, int]]:
    REGEX = re.compile(r"Sue (\d+): (\w+): (\d+), (\w+): (\d+), (\w+): (\d+)")
    SUES = {}
    for line in re.findall(REGEX, INPUT_16):
        chars = line[1::2]
        counts = map(int, line[2::2])

        SUES[int(line[0])] = dict(zip(chars, counts))
    return SUES


# %%
def part_one(sue_dict: dict[int, dict[str, int]]) -> int:
    return int(pd.DataFrame(sue_dict).T.eq(pd.Series(ticker_tape)).sum(axis=1).idxmax())


# %%
aoc_answer_display(part_one(generate_sue_dict(INPUT_16)))


# %% [markdown]
# ## --- Part Two ---
#
# As you're about to send the thank you note, something in the MFCSAM's
# instructions catches your eye. Apparently, it has an outdated
# [retroencabulator](https://www.youtube.com/watch?v=RXJKdh1KZ0w), and so the
# output from the machine isn't exact values - some of them indicate ranges.
#
# In particular, the `cats` and `trees` readings indicates that there are
# **greater than** that many (due to the unpredictable nuclear decay of cat
# dander and tree pollen), while the `pomeranians` and `goldfish` readings
# indicate that there are **fewer than** that many (due to the modial
# interaction of magnetoreluctance).
#
# What is the **number** of the real Aunt Sue?


# %%
def part_two(sue_dict: dict[int, dict[str, int]]) -> int:
    greater_than = ["cats", "trees"]
    less_than = ["pomeranians", "goldfish"]
    without_range_cols = list(ticker_tape.keys() - (greater_than + less_than))
    sue_df = pd.DataFrame(sue_dict)
    ticker_series = pd.Series(ticker_tape)
    return int(
        (
            sue_df.loc[without_range_cols]
            .T.eq(ticker_series.loc[without_range_cols])
            .sum(axis=1)
            + sue_df.loc[greater_than].T.gt(ticker_series.loc[greater_than]).sum(axis=1)
            + sue_df.loc[less_than].T.lt(ticker_series.loc[less_than]).sum(axis=1)
        ).idxmax()
    )


# %%
aoc_answer_display(part_two(generate_sue_dict(INPUT_16)))
