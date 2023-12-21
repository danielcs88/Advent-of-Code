# ```
# Day       Time  Rank  Score       Time  Rank  Score
#  12   00:10:03   231      0   00:11:14   163      0
# ```


# +
from collections import deque

from utils import open_input


# -

def adj(i, j):
    return (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)


def p1(f):
    grid: dict[tuple[int, int], str] = {
        (i, j): x for i, row in enumerate(f.splitlines()) for j, x in enumerate(row)
    }

    start = next(k for k, v in grid.items() if v == "S")
    end = next(k for k, v in grid.items() if v == "E")

    # print(start)
    # print(end)

    grid[start] = "a"
    grid[end] = "z"

    dist = {}
    bfs = deque([(0, start)])

    while len(bfs) > 0:
        # t: tuple[int, int]
        # p: str
        t, p = bfs.popleft()
        if p in dist:
            continue
        dist[p] = t

        for q in adj(*p):
            # print("q", q)
            # print(ord(grid.get(q, "~")))
            if ord(grid.get(q, "{")) - ord(grid[p]) > 1:
                continue
            bfs.append((t + 1, q))

    return dist[end]


test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def grid(f: str) -> dict[tuple[int, int], str]:
    return {
        (i, j): x for i, row in enumerate(f.splitlines()) for j, x in enumerate(row)
    }


p1(test)

from utils import open_input

input_12 = open_input("input_12.txt")

print(p1(input_12))


