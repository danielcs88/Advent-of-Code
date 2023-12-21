class lol(tuple):
    def __add__(self, other):
        return lol(a + b for a, b in zip(self, other))

    def __sub__(self, other):
        return lol(a - b for a, b in zip(self, other))


DIRS = {
    "R": lol((1, 0)),
    "L": lol((-1, 0)),
    "U": lol((0, 1)),
    "D": lol((0, -1)),
}


def move(h, t):
    diff = lol(min(1, max(-1, x)) for x in h - t)
    return t if h - t == diff else t + diff


def p1(f):
    h = t = lol((0, 0))
    pos = set()

    for line in f.splitlines():
        dir, step = line.split()

        for _ in range(int(step)):
            h += DIRS[dir]
            t = move(h, t)
            pos.add(t)

    return len(pos)


test = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

print(p1(test))
