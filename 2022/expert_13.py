from ast import literal_eval

from IPython.display import display

from utils import open_input

# from functools import total_ordering


# from math import prod


def cmp(a, b):
    if isinstance(a, int) and isinstance(b, int):
        return a - b

    if isinstance(a, list) and isinstance(b, list):
        for x, y in zip(a, b):
            if result := cmp(x, y):
                return result
        return len(a) - len(b)

    if isinstance(a, list):
        return cmp(a, [b])

    if isinstance(b, list):
        return cmp([a], b)

    # assert False


def p1(f):
    pairs = [[literal_eval(x) for x in pair.splitlines()] for pair in f.split("\n\n")]
    # return sum(i + 1 for i, (a, b) in enumerate(pairs) if cmp(a, b) < 0)
    return sum(i + 1 for i, (a, b) in enumerate(pairs) if cmp(a, b) < 0)


if __name__ == "__main__":

    test = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""

    input_13 = open_input("input_13.txt")
    display(p1(input_13))
    display(p1(test))
