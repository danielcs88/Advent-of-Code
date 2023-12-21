# %% [markdown]
# ## --- Day 3: Gear Ratios ---
#
# You and the Elf eventually reach a [gondola
# lift](https://en.wikipedia.org/wiki/Gondola_lift) station; he says the gondola
# lift will take you up to the **water source**, but this is as far as he can
# bring you. You go inside.
#
# It doesn't take long to find the gondolas, but there seems to be a problem:
# they're not moving.
#
# "Aaah!"
#
# You turn around to see a slightly-greasy Elf with a wrench and a look of
# surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working
# right now; it'll still be a while before I can fix it." You offer to help.
#
# The engineer explains that an engine part seems to be missing from the engine,
# but nobody can figure out which one. If you can **add up all the part
# numbers** in the engine schematic, it should be easy to work out which part is
# missing.
#
# The engine schematic (your puzzle input) consists of a visual representation
# of the engine. There are lots of numbers and symbols you don't really
# understand, but apparently **any number adjacent to a symbol**, even
# diagonally, is a "part number" and should be included in your sum. (Periods
# (`.`) do not count as a symbol.)
#
# Here is an example engine schematic:
#
# ```
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# ```
#
# In this schematic, two numbers are **not** part numbers because they are not
# adjacent to a symbol: `114` (top right) and `58` (middle right). Every other
# number is adjacent to a symbol and so **is** a part number; their sum is
# **`4361`**.
#
# Of course, the actual engine schematic is much larger. **What is the sum of
# all of the part numbers in the engine schematic?**

# %%
test = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

# %%
[list(x) for x in test.splitlines()]

# %%
grid = aoc_grid(test)
# grid

# %%
digits = [
    {
        "coordinates": pair,
        "value": value,
        "adjacent_coordinates": aoc_adj(
            *pair, include_diagonals=True, only_positive_indices=True
        ),
    }
    for pair, value in grid.items()
    if value.isdigit()
]
# digits

# %%
symbols = ["#", "$", "%", "&", "*", "+", "-", "/", "=", "@"]

# Filter out adjacents that don't exist and symbols to find valid digits
for i, x in enumerate(digits):
    adj = digits[i]["adjacent_coordinates"]
    digits[i]["adjacent_symbols"] = [
        grid[pair] for pair in adj if grid.get(pair, "NaN") != "NaN"
    ]
    adj = digits[i]["adjacent_symbols"]
    digits[i]["valid"] = any(x in symbols for x in adj)

# %%
valid_digits = [d for d in digits if d["valid"]]

# %%
pd.DataFrame(valid_digits)

# %%
for i, x in enumerate(valid_digits):
    row = valid_digits[i]
    adj_sym = row["adjacent_symbols"]
    row["adjacent_num_coordinates"] = [
        row["adjacent_coordinates"][i] for i, sym in enumerate(adj_sym) if sym.isdigit()
    ]

# %%
pd.DataFrame(valid_digits)


# %%
def p1(f):
    lines = f.read().splitlines()
    ans = 0
    for i, line in enumerate(lines):
        for m in re.finditer(r"\d+", line):
            idxs = [(i, m.start() - 1), (i, m.end())]
            idxs += [(i - 1, j) for j in range(m.start() - 1, m.end() + 1)]
            idxs += [(i + 1, j) for j in range(m.start() - 1, m.end() + 1)]
            count = sum(
                0 <= a < len(lines) and 0 <= b < len(lines[a]) and lines[a][b] != "."
                for a, b in idxs
            )
            if count > 0:
                ans += int(m.group())
    return ans
