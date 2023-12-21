


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


[list(x) for x in test.splitlines()]


grid = aoc_grid(test)
# grid


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


symbols = ["#", "$", "%", "&", "*", "+", "-", "/", "=", "@"]

# Filter out adjacents that don't exist and symbols to find valid digits
for i, x in enumerate(digits):
    adj = digits[i]["adjacent_coordinates"]
    digits[i]["adjacent_symbols"] = [
        grid[pair] for pair in adj if grid.get(pair, "NaN") != "NaN"
    ]
    adj = digits[i]["adjacent_symbols"]
    digits[i]["valid"] = any(x in symbols for x in adj)


valid_digits = [d for d in digits if d["valid"]]


pd.DataFrame(valid_digits)


for i, x in enumerate(valid_digits):
    row = valid_digits[i]
    adj_sym = row["adjacent_symbols"]
    row["adjacent_num_coordinates"] = [
        row["adjacent_coordinates"][i] for i, sym in enumerate(adj_sym) if sym.isdigit()
    ]


pd.DataFrame(valid_digits)


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
