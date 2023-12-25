# %% [markdown]
# ## --- Day 7: Some Assembly Required ---
#
# This year, Santa brought little Bobby Tables a set of wires and [bitwise logic
# gates](https://en.wikipedia.org/wiki/Bitwise_operation)! Unfortunately, little
# Bobby is a little under the recommended age range, and he needs help
# assembling the circuit.
#
# Each wire has an identifier (some lowercase letters) and can carry a
# [16-bit](https://en.wikipedia.org/wiki/16-bit) signal (a number from `0` to
# `65535`). A signal is provided to each wire by a gate, another wire, or some
# specific value. Each wire can only get a signal from one source, but can
# provide its signal to multiple destinations. A gate provides no signal until
# all of its inputs have a signal.
#
# The included instructions booklet describes how to connect the parts together:
# `x AND y -> z` means to connect wires `x` and `y` to an AND gate, and then
# connect its output to wire `z`.
#
# For example:
#
# - `123 -> x` means that the signal `123` is provided to wire `x`.
# - `x AND y -> z` means that the [bitwise
#   AND](https://en.wikipedia.org/wiki/Bitwise_operation#AND) of wire `x` and
#   wire `y` is provided to wire `z`.
# - `p LSHIFT 2 -> q` means that the value from wire `p` is
#   [left-shifted](https://en.wikipedia.org/wiki/Logical_shift) by `2` and then
#   provided to wire `q`.
# - `NOT e -> f` means that the [bitwise
#   complement](https://en.wikipedia.org/wiki/Bitwise_operation#NOT) of the
#   value from wire `e` is provided to wire `f`.
#
# Other possible gates include `OR` ([bitwise
# OR](https://en.wikipedia.org/wiki/Bitwise_operation#OR)) and `RSHIFT`
# ([right-shift](https://en.wikipedia.org/wiki/Logical_shift)). If, for some
# reason, you'd like to **emulate** the circuit instead, almost all programming
# languages (for example,
# [C](https://en.wikipedia.org/wiki/Bitwise_operations_in_C),
# [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Bitwise_Operators),
# or [Python](https://wiki.python.org/moin/BitwiseOperators)) provide operators
# for these gates.
#
# For example, here is a simple circuit:
#
# ```
# 123 -> x
# 456 -> y
# x AND y -> d
# x OR y -> e
# x LSHIFT 2 -> f
# y RSHIFT 2 -> g
# NOT x -> h
# NOT y -> i
# ```
#
# After it is run, these are the signals on the wires:
#
# ```
# d: 72
# e: 507
# f: 492
# g: 114
# h: 65412
# i: 65079
# x: 123
# y: 456
# ```
#
# In little Bobby's kit's instructions booklet (provided as your puzzle input),
# what signal is ultimately provided to **wire `a`**?

# %%
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

# %%
input_07 = aoc_open_input("input_07.txt")


# %%


# %%
def part_one_and_two(
    input_str: str, wire: str, prior_instructions: dict | dict[str, int] = {}
) -> int:
    """
    Evaluate a circuit of logic gates and wires to determine the value of a
    specific wire.

    This function simulates a circuit with logic gates and wires to calculate
    the value of a specified wire. The circuit is represented by a series of
    instructions provided in the input string.

    Parameters
    ----------
    input_str : str
        A string containing instructions for the circuit. Each line consists of
        an expression followed by the variable it assigns to, separated by
        " -> ".
    wire : str
        The target wire for which the value needs to be calculated.
    prior_instructions : dict | dict[str, int], optional
        A dictionary containing prior instructions or values for variables in
        the circuit. This is useful for memoization to avoid redundant
        calculations. The default is an empty dictionary.

    Returns
    -------
    int
        The calculated value of the specified wire in the circuit.

    Notes
    -----
    The function uses a recursive approach to evaluate expressions involving
    logic gates and wires. It supports basic logic gate operations such as AND,
    OR, LSHIFT, RSHIFT, and NOT.
    """
    original_instructions = {}

    for line in input_str.splitlines():
        expression, variable = line.split(" -> ")
        original_instructions[variable] = expression

    actual_instructions = prior_instructions or {}

    def bitwise_not_int16(num: int) -> int:
        return 2**16 + ~num if ~num < 0 else num

    def get_value(key: str):
        if key.isdigit():
            return int(key)
        if key in actual_instructions:
            return actual_instructions[key]

        value = original_instructions[key]

        if value.isdigit():
            actual_instructions[key] = int(value)
            return actual_instructions[key]
        if value.startswith("NOT"):
            s1 = get_value(value[4:])
            result = bitwise_not_int16(s1)
            actual_instructions[value] = result
            return actual_instructions[value]
        if "OR" in value:
            s1, s2 = value.split(" OR ")
            actual_instructions[key] = get_value(s1) | get_value(s2)
            return actual_instructions[key]
        if "AND" in value:
            s1, s2 = value.split(" AND ")
            actual_instructions[key] = get_value(s1) & get_value(s2)
            return actual_instructions[key]
        if "LSHIFT" in value:
            s1, digit = value.split(" LSHIFT ")
            actual_instructions[key] = get_value(s1) << int(digit)
            return actual_instructions[key]
        if "RSHIFT" in value:
            s1, digit = value.split(" RSHIFT ")
            actual_instructions[key] = get_value(s1) >> int(digit)
            return actual_instructions[key]
        actual_instructions[key] = get_value(value)
        return actual_instructions[key]

    return get_value(wire)


# %%
test_case = part_one_and_two(test, "i")
print("Test Case:", test_case)

# %%
part_one = part_one_and_two(input_07, "a")
print("Part One:", part_one_and_two(input_07, "a"))

# %%
part_two = part_one_and_two(input_07, "a", {"b": part_one})
print("Part Two:", part_two)
