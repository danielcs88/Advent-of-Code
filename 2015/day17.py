# %% [markdown]
# ## --- Day 17: No Such Thing as Too Much ---
#
# The elves bought too much eggnog again - `150` liters this time. To fit it all
# into your refrigerator, you'll need to move it into smaller containers. You
# take an inventory of the capacities of the available containers.
#
# For example, suppose you have containers of size `20`, `15`, `10`, `5`, and
# `5` liters. If you need to store `25` liters, there are four ways to do it:
#
# - `15` and `10`
# - `20` and `5` (the first `5`)
# - `20` and `5` (the second `5`)
# - `15`, `5`, and `5`
#
# Filling all containers entirely, how many different **combinations of
# containers** can exactly fit all `150` liters of eggnog?

# %%
from itertools import combinations

# %%
test = [20, 15, 10, 5, 5]
test_capacity = 25

INPUT_17 = """50
44
11
49
42
46
18
32
26
40
21
7
18
43
10
47
36
24
22
40"""


# %%
def combos_for_size(containers: list[int], size: int) -> int:
    return sum(
        sum(c) == size
        for count in range(len(containers))
        for c in combinations(containers, count + 1)
    )


# %%
combos_for_size(test, 25)

# %%
combos_for_size([int(_) for _ in INPUT_17.splitlines()], 150)


# %% [markdown]
# ## --- Part Two ---
#
# While playing with all the containers in the kitchen, another load of eggnog
# arrives! The shipping and receiving department is requesting as many
# containers as you can spare.
#
# Find the minimum number of containers that can exactly fit all `150` liters of
# eggnog. **How many different ways** can you fill that number of containers and
# still hold exactly `150` litres?
#
# In the example above, the minimum number of containers was two. There were
# three ways to use that many containers, and so the answer there would be `3`.

# %%
def combos_for_min_size(containers: list[int], size: int) -> int:
    min_count = next(
        count
        for count in range(len(containers))
        for c in combinations(containers, count + 1)
        if sum(c) == size
    )
    return sum(sum(c) == size for c in combinations(containers, min_count + 1))


# %%
combos_for_min_size(test, 25)

# %%
combos_for_min_size([int(_) for _ in INPUT_17.splitlines()], 150)
