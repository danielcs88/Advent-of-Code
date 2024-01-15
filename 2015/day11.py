# %% [markdown]
# ## --- Day 11: Corporate Policy ---
#
# Santa's previous password expired, and he needs help choosing a new one.
#
# To help him remember his new password after the old one expires, Santa has
# devised a method of coming up with a password based on the previous one.
# Corporate policy dictates that passwords must be exactly eight lowercase
# letters (for security reasons), so he finds his new password by
# **incrementing** his old password string repeatedly until it is valid.
#
# Incrementing is just like counting with numbers: `xx`, `xy`, `xz`, `ya`, `yb`,
# and so on. Increase the rightmost letter one step; if it was `z`, it wraps
# around to `a`, and repeat with the next letter to the left until one doesn't
# wrap around.
#
# Unfortunately for Santa, a new Security-Elf recently started, and he has
# imposed some additional password requirements:
#
# - Passwords must include one increasing straight of at least three letters,
#   like `abc`, `bcd`, `cde`, and so on, up to `xyz`. They cannot skip letters;
#   `abd` doesn't count.
# - Passwords may not contain the letters `i`, `o`, or `l`, as these letters can
#   be mistaken for other characters and are therefore confusing.
# - Passwords must contain at least two different, non-overlapping pairs of
#   letters, like `aa`, `bb`, or `zz`.
#
# For example:
#
# - `hijklmmn` meets the first requirement (because it contains the straight
#   `hij`) but fails the second requirement requirement (because it contains `i`
#   and `l`).
# - `abbceffg` meets the third requirement (because it repeats `bb` and `ff`)
#   but fails the first requirement.
# - `abbcegjk` fails the third requirement, because it only has one double
#   letter (`bb`).
# - The next password after `abcdefgh` is `abcdffaa`.
# - The next password after `ghijklmn` is `ghjaabcc`, because you eventually
#   skip all the passwords that start with `ghi...`, since `i` is not allowed.
#
# Given Santa's current password (your puzzle input), what should his **next
# password** be?
#
# Your puzzle input is `hxbxwxba`.

# %%
import re

import pyperclip

INPUT_11 = "hxbxwxba"


# Rules for correct password
def is_contain_straight_increasing_symbols(input_str: str) -> bool:
    char_codes = [ord(char) for char in input_str]
    return any(
        char == char_codes[index + 1] - 1 == char_codes[index + 2] - 2
        for index, char in enumerate(char_codes[:-2])
    )


def is_contain_restricted_symbols(input_str: str) -> bool:
    return re.search(r"i|o|l", input_str) is not None


def is_contain_pairs(input_str: str) -> bool:
    return re.search(r"(\w)\1.*(\w)\2", input_str) is not None


# Increments one char
def increment_char(input_char: str) -> str:
    return "a" if input_char == "z" else chr(ord(input_char) + 1)


# Increments the whole string by one char recursively
def increment_string(input_str: str) -> str:
    next_char = increment_char(input_str[-1])
    return (
        f"{increment_string(input_str[:-1])}a"
        if next_char == "a"
        else input_str[:-1] + next_char
    )


# Checks if password is valid (based on rules above)
def is_valid_password(input_str: str) -> bool:
    return (
        is_contain_straight_increasing_symbols(input_str)
        and not is_contain_restricted_symbols(input_str)
        and is_contain_pairs(input_str)
    )


def part_one(input_str: str) -> str:
    # count = 0
    result = input_str
    while not is_valid_password(result):
        # count += 1
        # print(count, "temp result", result)
        result = increment_string(result)
    pyperclip.copy(result)
    print(result)
    return result


# %%
print(part_one(INPUT_11))

# %% [markdown]
# ## --- Part Two ---
#
# Santa's password expired again. What's the next one?

# %%
part_one(increment_string(part_one(INPUT_11)))
