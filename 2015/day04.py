# %% [markdown]
# ## --- Day 4: The Ideal Stocking Stuffer ---
#
# Santa needs help [mining](https://en.wikipedia.org/wiki/Bitcoin#Mining) some
# AdventCoins (very similar to
# [bitcoins](https://en.wikipedia.org/wiki/Bitcoin)) to use as gifts for all the
# economically forward-thinking little girls and boys.
#
# To do this, he needs to find [MD5](https://en.wikipedia.org/wiki/MD5) hashes
# which, in [hexadecimal](https://en.wikipedia.org/wiki/Hexadecimal), start with
# at least **five zeroes**. The input to the MD5 hash is some secret key (your
# puzzle input, given below) followed by a number in decimal. To mine
# AdventCoins, you must find Santa the lowest positive number (no leading
# zeroes: `1`, `2`, `3`, ...) that produces such a hash.
#
# For example:
#
# - If your secret key is `abcdef`, the answer is `609043`, because the MD5 hash
#   of `abcdef609043` starts with five zeroes (`000001dbbfa...`), and it is the
#   lowest such number to do so.
# - If your secret key is `pqrstuv`, the lowest number it combines with to make
#   an MD5 hash starting with five zeroes is `1048970`; that is, the MD5 hash of
#   `pqrstuv1048970` looks like `000006136ef...`.
#
# Your puzzle input is `yzbqklnj`.

# %%
input_04 = "yzbqklnj"

# %%
import hashlib
import pyperclip


def solve(input_str: str, leading_zeros: int = 5) -> int:
    max_iterations = (
        10**6
    )  # Set a maximum number of iterations to avoid infinite loops

    for idx, _ in enumerate(range(1, max_iterations)):
        key = f"{input_str}{idx}".encode("utf-8")
        digest = hashlib.md5(key).hexdigest()
        if digest.startswith(leading_zeros * "0"):
            break

    print(idx, input_str)
    pyperclip.copy(idx)
    return idx


# %%
solve(input_04, 5)

# %% [markdown]
# ## Part Two
# Now find one that starts with six zeroes.

# %%
solve(input_04, 6)
