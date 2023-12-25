


test = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i"""

test_results = {
    "d": 72,
    "e": 507,
    "f": 492,
    "g": 114,
    "h": 65412,
    "i": 65079,
    "x": 123,
    "y": 456,
}


input_07 = aoc_open_input("input_07.txt")


def bitwise_not_int16(num: int) -> int:
    return (2**16) + ~num if (~num < 0) else num


bitwise_not_int16(456)


def part_one(input_str: str, wire: str) -> int:
    hail_mary = {}
    variables = []
    operations = []

    for line in (
        input_str.replace("AND", "&")
        .replace("OR", "|")
        .replace("LSHIFT", "<<")
        .replace("RSHIFT", ">>")
        .replace("NOT", "~")
        .splitlines()
    ):
        expression, variable = line.split(" -> ")
        hail_mary[variable] = expression

        if expression.isdigit():
            hail_mary[variable] = int(expression)

    for k, v in hail_mary.items():
        if isinstance(v, int):
            continue
        else:
            print(k, v)


part_one(test, "i")


part_one(input_07, "a")



