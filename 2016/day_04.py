# %% [markdown]
# ## --- Day 4: Security Through Obscurity ---
#
# Finally, you come across an information kiosk with a list of rooms. Of course,
# the list is encrypted and full of decoy data, but the instructions to decode
# the list are barely hidden nearby. Better remove the decoy data first.
#
# Each room consists of an encrypted name (lowercase letters separated by
# dashes) followed by a dash, a sector ID, and a checksum in square brackets.
#
# A room is real (not a decoy) if the checksum is the five most common letters
# in the encrypted name, in order, with ties broken by alphabetization. For
# example:
#
# - `aaaaa-bbb-z-y-x-123[abxyz]` is a real room because the most common letters
#   are `a` (5\), `b` (3\), and then a tie between `x`, `y`, and `z`, which are
#   listed alphabetically.
# - `a-b-c-d-e-f-g-h-987[abcde]` is a real room because although the letters are
#   all tied (1 of each), the first five are listed alphabetically.
# - `not-a-real-room-404[oarel]` is a real room.
# - `totally-real-room-200[decoy]` is not.
#
# Of the real rooms from the list above, the sum of their sector IDs is `1514`.
#
# What is the **sum of the sector IDs of the real rooms**?

# %%
import re
from collections import Counter

# %%
examples = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""

input_04 = aoc_open_input("input_04.txt")


# %%
def generate_checksum(input_room: str) -> str:
    counter_elements = Counter(re.findall(r"[A-Za-z]", input_room.split("[")[0]))
    sorted_by_value_then_key = dict(
        sorted(counter_elements.items(), key=lambda x: (-x[1], x[0]))
    )
    return "".join(sorted_by_value_then_key.keys())[:5]


# %%
def extract_checksum(input_room: str) -> str:
    return re.findall(r"(?:\[)(\w+)(?:\])", input_room)[0]


# %%
def extract_sector_id(input_room: str) -> int:
    return int(re.findall(r"\d+", input_room)[0])


# %%
def part_one(input_str: str) -> int:
    splitted = input_str.splitlines()
    return sum(
        extract_sector_id(x)
        for x in splitted
        if generate_checksum(x) == extract_checksum(x)
    )


# %%
part_one(examples)

# %%
aoc_answer_display(part_one(input_04))

# %% [markdown]
# ## --- Part Two ---
#
# With all the decoy data out of the way, it's time to decrypt this list and get
# moving.
#
# The room names are encrypted by a state-of-the-art [shift
# cipher](https://en.wikipedia.org/wiki/Caesar_cipher), which is nearly
# unbreakable without the right software. However, the information kiosk
# designers at Easter Bunny HQ were not expecting to deal with a master
# cryptographer like yourself.
#
# To decrypt a room name, rotate each letter forward through the alphabet a
# number of times equal to the room's sector ID. `A` becomes `B`, `B` becomes
# `C`, `Z` becomes `A`, and so on. Dashes become spaces.
#
# For example, the real name for `qzmt-zixmtkozy-ivhz-343` is `very encrypted
# name`.
#
# **What is the sector ID** of the room where North Pole objects are stored?

# %%
example_02 = "qzmt-zixmtkozy-ivhz-343"


# %%
def decrypt_row(input_row: str) -> tuple[str, int]:
    """
    Decrypts a given row string by shifting each letter forward in the alphabet
    based on the sector ID. The sector ID is extracted from the input string,
    and the shift is calculated as the sector ID modulo 26. Hyphens in the input
    are converted to spaces in the output.

    Parameters
    ----------
    input_row : str
        A string containing encrypted text and a sector ID. The sector ID is
        assumed to be the numeric part of the string, and the rest of the string
        is the encrypted text.

    Returns
    -------
    tuple[str, int]
        A tuple where the first element is the decrypted string (with letters
        shifted according to the sector ID and hyphens replaced by spaces), and
        the second element is the sector ID extracted from the input string.

    Examples
    --------
    >>> decrypt_row("qzmt-zixmtkozy-ivhz-343")
    ('very encrypted name', 343)
    """
    sector_id = extract_sector_id(input_row)
    offset = sector_id % 26

    decrypted = "".join(
        " " if letter == "-" else chr((ord(letter) - ord("a") + offset) % 26 + ord("a"))
        for letter in input_row
        if not letter.isdigit()
    )

    return decrypted.strip(), sector_id


# %%
decrypt_row(example_02)


# %%
def part_two(input_str: str = input_04, verbose: bool = False) -> int:
    """
    Processes a string of encrypted rows to find the one that, when decrypted,
    contains the word "pole". The function decrypts each row using the
    `decrypt_row` function and checks if the word "pole" is present in the
    decrypted string. If found, it returns the corresponding sector ID.

    Parameters
    ----------
    input_str : str, optional
        A string containing multiple encrypted rows, where each row is assumed
        to include an encrypted name followed by a sector ID. The default value
        is `input_04`.

    Returns
    -------
    int
        The sector ID of the row whose decrypted name contains the word "pole".
        If no such row is found, the function returns `None`.
    """
    for line in input_str.splitlines():
        real_name, sector_id = decrypt_row(line)
        if "pole" in real_name:
            if verbose:
                print(line, real_name)
            return sector_id


# %%
aoc_answer_display(part_two())
