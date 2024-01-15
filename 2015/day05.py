# %% [markdown]
# ## --- Day 5: Doesn't He Have Intern-Elves For This? ---
#
# Santa needs help figuring out which strings in his text file are naughty or
# nice.
#
# A **nice string** is one with all of the following properties:
#
# - It contains at least three vowels (`aeiou` only), like `aei`, `xazegov`, or
#   `aeiouaeiouaeiou`.
# - It contains at least one letter that appears twice in a row, like `xx`,
#   `abcdde` (`dd`), or `aabbccdd` (`aa`, `bb`, `cc`, or `dd`).
# - It does **not** contain the strings `ab`, `cd`, `pq`, or `xy`, even if they
#   are part of one of the other requirements.
#
# For example:
#
# - `ugknbfddgicrmopn` is nice because it has at least three vowels
#   (`u...i...o...`), a double letter (`...dd...`), and none of the disallowed
#   substrings.
# - `aaa` is nice because it has at least three vowels and a double letter, even
#   though the letters used by different rules overlap.
# - `jchzalrnumimnmhp` is naughty because it has no double letter.
# - `haegwjzuvuyypxyu` is naughty because it contains the string `xy`.
# - `dvszwmarrgswjxmb` is naughty because it contains only one vowel.
#
# How many strings are nice?

# %%
tests = {
    "ugknbfddgicrmopn": True,
    "aaa": True,
    "jchzalrnumimnmhp": False,
    "haegwjzuvuyypxyu": False,
    "dvszwmarrgswjxmb": False,
}


# %%
def is_nice_string(s: str) -> bool:
    # Check for at least three vowels
    vowels = set("aeiou")
    vowel_count = sum(char in vowels for char in s)
    if vowel_count < 3:
        return False

    # Check for at least one letter that appears twice in a row
    if all(s[i] != s[i + 1] for i in range(len(s) - 1)):
        return False

    # Check for disallowed substrings
    disallowed_substrings = {"ab", "cd", "pq", "xy"}
    return all(substring not in s for substring in disallowed_substrings)


def count_nice_strings(strings: list[str]) -> int:
    return sum(is_nice_string(s) for s in strings)


# Example usage:
input_strings = [
    "ugknbfddgicrmopn",
    "aaa",
    "jchzalrnumimnmhp",
    "haegwjzuvuyypxyu",
    "dvszwmarrgswjxmb",
]
count_nice_strings(input_strings)

# %%
input_05 = aoc_open_input("input_05.txt")
count_nice_strings(input_05.splitlines())


# %% [markdown]
# ## --- Part Two ---
#
# Realizing the error of his ways, Santa has switched to a better model of
# determining whether a string is naughty or nice. None of the old rules apply,
# as they are all clearly ridiculous.
#
# Now, a nice string is one with all of the following properties:
#
# - It contains a pair of any two letters that appears at least twice in the
#   string without overlapping, like `xyxy` (`xy`) or `aabcdefgaa` (`aa`), but
#   not like `aaa` (`aa`, but it overlaps).
# - It contains at least one letter which repeats with exactly one letter
#   between them, like `xyx`, `abcdefeghi` (`efe`), or even `aaa`.
#
# For example:
#
# - `qjhvhtzxzqqjkmpb` is nice because is has a pair that appears twice (`qj`)
#   and a letter that repeats with exactly one letter between them (`zxz`).
# - `xxyxx` is nice because it has a pair that appears twice and a letter that
#   repeats with one between, even though the letters used by each rule overlap.
# - `uurcxstgmygtbstg` is naughty because it has a pair (`tg`) but no repeat
#   with a single letter between them.
# - `ieodomkazucvgmuy` is naughty because it has a repeating letter with one
#   between (`odo`), but no pair that appears twice.
#
# How many strings are nice under these new rules?


# %%
def is_nice_string_new_rules(s: str) -> bool:
    def has_pair_repeating(s: str) -> bool:
        for i in range(len(s) - 1):
            pair = s[i : i + 2]
            if s.count(pair) >= 2:
                return True
        return False

    def has_repeating_letter_with_one_between(s: str) -> bool:
        for i in range(len(s) - 2):
            if s[i] == s[i + 2]:
                return True
        return False

    return has_pair_repeating(s) and has_repeating_letter_with_one_between(s)


def count_nice_strings_new_rules(strings: list[str]) -> int:
    return sum(is_nice_string_new_rules(s) for s in strings)


# %%
# Example usage:
input_strings = ["qjhvhtzxzqqjkmpb", "xxyxx", "uurcxstgmygtbstg", "ieodomkazucvgmuy"]
count_nice_strings_new_rules(input_strings)


# %%
count_nice_strings_new_rules(input_05.splitlines())
# %%
