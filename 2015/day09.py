# %% [markdown]
# ## --- Day 9: All in a Single Night ---
#
# Every year, Santa manages to deliver all of his presents in a single night.
#
# This year, however, he has some new locations to visit; his elves have
# provided him the distances between every pair of locations. He can start and
# end at any two (different) locations he wants, but he must visit each location
# exactly once. What is the **shortest distance** he can travel to achieve this?
#
# For example, given the following distances:
#
# ```
# London to Dublin = 464
# London to Belfast = 518
# Dublin to Belfast = 141
# ```
#
# The possible routes are therefore:
#
# ```
# Dublin -> London -> Belfast = 982
# London -> Dublin -> Belfast = 605
# London -> Belfast -> Dublin = 659
# Dublin -> Belfast -> London = 659
# Belfast -> Dublin -> London = 605
# Belfast -> London -> Dublin = 982
# ```
#
# The shortest of these is `London -> Dublin -> Belfast = 605`, and so the
# answer is `605` in this example.
#
# What is the distance of the shortest route?

# %%
from itertools import pairwise, permutations

import pyperclip

# %%
test = """London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""

input_09 = aoc_open_input("input_09.txt")


# %%
def part_one_and_two(input_str: str, agg_type: str) -> int:
    """
    Calculate the minimum or maximum distance of trips based on given routes.

    Parameters
    ----------
    input_str : str
        A multiline string containing information about routes, each line in the
        format: 'origin to destination = distance', where origin and destination
        are city names, and distance is an integer representing the distance
        between them.
    agg_type : str
        The type of aggregation to perform. Should be either 'min' to calculate
        the minimum distance or 'max' to calculate the maximum distance.

    Returns
    -------
    int
        The minimum or maximum distance of trips based on the specified
        aggregation type.

    Raises
    ------
    AssertionError
        If agg_type is not 'min' or 'max'.

    Notes
    -----
    This function assumes a symmetric distance matrix, meaning that the distance
    from city A to city B is the same as the distance from city B to city A.

    The result is copied to the clipboard using the Pyperclip library.

    Examples
    --------
    >>> input_str = 'A to B = 10\\nB to C = 15\\nC to A = 20'
    >>> part_one_and_two(input_str, 'min')
    25
    >>> part_one_and_two(input_str, 'max')
    35
    """

    assert agg_type in {"min", "max"}, "`agg_type` must be 'min' or 'max'"

    routes = {}
    cities = set()

    for line in input_str.splitlines():
        origin, _, destination, _, distance = line.split()

        cities.add(origin)
        cities.add(destination)

        routes[(origin, destination)] = int(distance)
        routes[(destination, origin)] = int(distance)

    final_trips_lens = []

    for trips in permutations(cities, len(cities)):
        miles = sum(routes[trip] for trip in pairwise(trips))
        final_trips_lens.append(miles)

    result = min(final_trips_lens) if agg_type == "min" else max(final_trips_lens)
    pyperclip.copy(result)
    return result


# %%
print(part_one_and_two(test, "min"))

# %%
print(part_one_and_two(input_09, "min"))

# %% [markdown]
# ## -- Part Two ---
#
# The next year, just to show off, Santa decides to take the route with the
# **longest distance** instead.
#
# He can still start and end at any two (different) locations he wants, and he
# still must visit each location exactly once.
#
# For example, given the distances above, the longest route would be `982` via
# (for example) `Dublin -> London -> Belfast`.
#
# What is the distance of the longest route?

# %%
print(part_one_and_two(test, "max"))

# %%
print(part_one_and_two(input_09, "max"))

# %%
part_one_and_two(test, "median")
