# %% [markdown]
# ## --- Day 10: Elves Look, Elves Say ---
#
# Today, the Elves are playing a game called
# [look-and-say](https://en.wikipedia.org/wiki/Look-and-say_sequence). They take
# turns making sequences by reading aloud the previous sequence and using that
# reading as the next sequence. For example, `211` is read as "one two, two
# ones", which becomes `1221` (`1` `2`, `2` `1`s).
#
# Look-and-say sequences are generated iteratively, using the previous value as
# input for the next step. For each step, take the previous value, and replace
# each run of digits (like `111`) with the number of digits (`3`) followed by
# the digit itself (`1`).
#
# For example:
#
# - `1` becomes `11` (`1` copy of digit `1`).
# - `11` becomes `21` (`2` copies of digit `1`).
# - `21` becomes `1211` (one `2` followed by one `1`).
# - `1211` becomes `111221` (one `1`, one `2`, and two `1`s).
# - `111221` becomes `312211` (three `1`s, two `2`s, and one `1`).
#
# Starting with the digits in your puzzle input, apply this process 40 times.
# What is **the length of the result**?
#
# Your puzzle input is `1113122113`.

# %%
from itertools import groupby

import pyperclip

# %%
test = {
    "1": "11",  # (1 copy of digit 1).
    "11": "21",  # (2 copies of digit 1).
    "21": "1211",  # (one 2 followed by one 1).
    "1211": "111221",  # (one 1, one 2, and two 1s).
    "111221": "312211",  # (three 1s, two 2s, and one 1).
}

# %%
input_10 = "1113122113"


# %%
def part_one(input_str: str, n_cycles: int = 1) -> int:
    """Apply the 'look-and-say' algorithm to the given input string.

    Parameters
    ----------
    input_str : str
        The input string to which the 'look-and-say' algorithm is applied.
    n_cycles : int, optional
        The number of cycles to perform the 'look-and-say' algorithm, by
        default 1.

    Returns
    -------
    int
        The length of the resulting string afterapplying the 'look-and-say'
        algorithm to the input string by n times.

    Notes
    -----
    The 'look-and-say' algorithm replaces each run of consecutive identical
    characters in the input string with a pair containing the count and the
    character itself.

    Examples
    --------
    >>> part_one('112233')
    6

    >>> part_one('111222333')
    6
    """
    look_and_say = lambda x: "".join(
        [f"{''.join((str(len(list(g))), k))}" for k, g in groupby(x)]
    )
    result = look_and_say(input_str)
    print(result)
    for _ in range(cycles - 1):
        result = look_and_say(result)
    length_result = len(result)
    pyperclip.copy(length_result)
    return length_result


# %%
print(part_one(input_10, 40))

# %% [markdown]
# ## --- Part Two ---
#
# Neat, right? You might also enjoy hearing [John Conway talking about this
# sequence](https://www.youtube.com/watch?v=ea7lJkEhytA) (that's Conway of
# *Conway's Game of Life* fame).
#
# Now, starting again with the digits in your puzzle input, apply this process
# *50* times. What is *the length of the new result*?

# %%
print(part_one(input_10, 50))
