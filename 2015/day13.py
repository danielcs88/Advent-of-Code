# %% [markdown]
# ## --- Day 13: Knights of the Dinner Table ---
#
# In years past, the holiday feast with your family hasn't gone so well. Not
# everyone gets along! This year, you resolve, will be different. You're going
# to find the **optimal seating arrangement** and avoid all those awkward
# conversations.
#
# You start by writing up a list of everyone invited and the amount their
# happiness would increase or decrease if they were to find themselves sitting
# next to each other person. You have a circular table that will be just big
# enough to fit everyone comfortably, and so each person will have exactly two
# neighbors.
#
# For example, suppose you have only four attendees planned, and you calculate
# their potential happiness as follows:
#
# ```
# Alice would gain 54 happiness units by sitting next to Bob.
# Alice would lose 79 happiness units by sitting next to Carol.
# Alice would lose 2 happiness units by sitting next to David.
# Bob would gain 83 happiness units by sitting next to Alice.
# Bob would lose 7 happiness units by sitting next to Carol.
# Bob would lose 63 happiness units by sitting next to David.
# Carol would lose 62 happiness units by sitting next to Alice.
# Carol would gain 60 happiness units by sitting next to Bob.
# Carol would gain 55 happiness units by sitting next to David.
# David would gain 46 happiness units by sitting next to Alice.
# David would lose 7 happiness units by sitting next to Bob.
# David would gain 41 happiness units by sitting next to Carol.
# ```
#
# Then, if you seat Alice next to David, Alice would lose `2` happiness units
# (because David talks so much), but David would gain `46` happiness units
# (because Alice is such a good listener), for a total change of `44`.
#
# If you continue around the table, you could then seat Bob next to Alice (Bob
# gains `83`, Alice gains `54`). Finally, seat Carol, who sits next to Bob
# (Carol gains `60`, Bob loses `7`) and David (Carol gains `55`, David gains
# `41`). The arrangement looks like this:
#
# ```
#      +41 +46
# +55   David    -2
# Carol       Alice
# +60    Bob    +54
#      -7  +83
# ```
#
# After trying every other seating arrangement in this hypothetical scenario,
# you find that this one is the most optimal, with a total change in happiness
# of `330`.
#
# What is the **total change in happiness** for the optimal seating arrangement
# of the actual guest list?

# %%
from collections import defaultdict
from itertools import permutations

# %%
INPUT_13 = aoc_open_input("input_13.txt")

# %%
test = """Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol."""


# %%
def solution(input_str: str, joining_dinner: bool = False) -> int:
    """
    Compute the maximum total happiness for a given seating arrangement.

    Parameters
    ----------
    input_str : str
        A string containing information about guests' happiness changes.
        Each line in the string represents a statement like:
        "A gains/loses B happiness units."
    joining_dinner : bool, optional
        If True, include "Daniel" as a guest, by default False.

    Returns
    -------
    int
        The maximum total happiness achievable for any seating arrangement.
    """
    scores = defaultdict(int)
    guests = set()

    # Parse input string and update scores and guests
    for line in (
        input_str.replace(" gain ", " ")
        .replace(" lose ", " -")
        .replace(".", "")
        .splitlines()
    ):
        parts = line.split()
        person, happiness, next_person = parts[0], int(parts[2]), parts[-1]

        guests.add(person)
        scores[(person, next_person)] = happiness

    # If joining dinner, add Daniel to the guests
    if joining_dinner:
        guests.add("Daniel")

    # Calculate happiness for all permutations
    best = 0
    for arrangement in permutations(guests):
        happiness_neighbors = sum(
            scores[(arrangement[i], arrangement[(i + 1) % len(arrangement)])]
            + scores[(arrangement[i], arrangement[(i - 1) % len(arrangement)])]
            for i in range(len(arrangement))
        )
        best = max(best, happiness_neighbors)

    return best


# %%
# %timeit solution(INPUT_13)

# %%
# %timeit solution_gpt(INPUT_13)

# %%
aoc_answer_display(solution(test))
aoc_answer_display(solution(test, True))

# %%
aoc_answer_display(solution(INPUT_13))

# %% [markdown]
# ## --- Part Two ---
#
# In all the commotion, you realize that you forgot to seat yourself. At this
# point, you're pretty apathetic toward the whole thing, and your happiness
# wouldn't really go up or down regardless of who you sit next to. You assume
# everyone else would be just as ambivalent about sitting next to you, too.
#
# So, add yourself to the list, and give all happiness relationships that
# involve you a score of `0`.
#
# What is the **total change in happiness** for the optimal seating arrangement
# that actually includes yourself?

# %%
aoc_answer_display(solution(INPUT_13, True))
