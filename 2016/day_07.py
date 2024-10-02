# %% [markdown]
# ## --- Day 7: Internet Protocol Version 7 ---
#
# While snooping around the local network of EBHQ, you compile a list of [IP
# addresses](https://en.wikipedia.org/wiki/IP_address) (they're IPv7, of course;
# [IPv6](https://en.wikipedia.org/wiki/IPv6) is much too limited). You'd like to
# figure out which IPs support **TLS** (transport\-layer snooping).
#
# An IP supports TLS if it has an Autonomous Bridge Bypass Annotation, or
# **ABBA**. An ABBA is any four\-character sequence which consists of a pair of
# two different characters followed by the reverse of that pair, such as `xyyx`
# or `abba`. However, the IP also must not have an ABBA within any hypernet
# sequences, which are contained by **square brackets**.
#
# For example:
#
# - `abba[mnop]qrst` supports TLS (`abba` outside square brackets).
# - `abcd[bddb]xyyx` does **not** support TLS (`bddb` is within square brackets,
#   even though `xyyx` is outside square brackets).
# - `aaaa[qwer]tyui` does **not** support TLS (`aaaa` is invalid; the interior
#   characters must be different).
# - `ioxxoj[asdfgh]zxcvbn` supports TLS (`oxxo` is outside square brackets, even
#   though it's within a larger string).
#
# **How many IPs** in your puzzle input support TLS?

# %%
import regex as re

# %%
example = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""


input_07 = aoc_open_input("input_07.txt")


# %%
def has_abba(input_str: str) -> None | re.Match:
    """Check if a string contains an abba."""
    abba = re.compile(r"([a-z])(?!\1)([a-z])\2\1")
    return abba.search(input_str)


# %%
def parse(puzzle_input: str) -> tuple[list[str]]:
    """Parse input."""
    lines = puzzle_input.splitlines()
    ips = []
    for line in lines:
        data = re.split(r"\[|\]", line)
        seq = data[::2]
        hyper = data[1::2]
        ips.append((seq, hyper))
    return ips


# %%
def part1(data: tuple[list[str]]) -> int:
    """Solve part 1."""
    return sum(
        any(has_abba(seq) for seq in ip[0]) and not any(has_abba(seq) for seq in ip[1])
        for ip in data
    )


# %%
parsed = parse(input_07)

# %%
aoc_answer_display(part1(parsed))

# %% [markdown]
# ## --- Part Two ---
#
# You would also like to know which IPs support **SSL** (super-secret
# listening).
#
# An IP supports SSL if it has an Area-Broadcast Accessor, or **ABA**, anywhere
# in the supernet sequences (outside any square bracketed sections), and a
# corresponding Byte Allocation Block, or **BAB**, anywhere in the hypernet
# sequences. An ABA is any three-character sequence which consists of the same
# character twice with a different character between them, such as `xyx` or
# `aba`. A corresponding BAB is the same characters but in reversed positions:
# `yxy` and `bab`, respectively.
#
# For example:
#
# - `aba[bab]xyz` supports SSL (`aba` outside square brackets with corresponding
#   `bab` within square brackets).
# - `xyx[xyx]xyx` does **not** support SSL (`xyx`, but no corresponding `yxy`).
# - `aaa[kek]eke` supports SSL (`eke` in supernet with corresponding `kek` in
#   hypernet; the `aaa` sequence is not related, because the interior character
#   must be different).
# - `zazbz[bzb]cdb` supports SSL (`zaz` has no corresponding `aza`, but `zbz`
#   has a corresponding `bzb`, even though `zaz` and `zbz` overlap).
#
# **How many IPs** in your puzzle input support SSL?


# %%
def get_babs(s):
    """Return list of all the babs in a string."""
    aba = re.compile(r"([a-z])(?!\1)([a-z])\1")
    return [f"{b}{a}{b}" for a, b in aba.findall(s, overlapped=True)]


# %%
def part2(data: tuple[list[str]]) -> int:
    """Solve part 2."""
    return sum(
        any(bab in hyper for bab in babs)
        for ip in data
        if (
            babs := [babs for seq in ip[0] for babs in get_babs(seq)]
        )  # Walrus operator to assign 'babs'
        for hyper in ip[1]
    )


# %%
aoc_answer_display(part2(parsed))
