# %% [markdown]
"""
\--- Day 7: Handy Haversacks ---
--------------------------------

You land at the regional airport in time for your next flight. In fact, it looks
like you'll even have time to grab some food: all flights are currently delayed
due to **issues in luggage processing**.

Due to recent aviation regulations, many rules (your puzzle input) are being
enforced about bags and their contents; bags must be color-coded and must
contain specific quantities of other color-coded bags. Apparently, nobody
responsible for these regulations considered how long they would take to
enforce!

For example, consider the following rules:

    light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.


These rules specify the required contents for 9 bag types. In this example,
every `faded blue` bag is empty, every `vibrant plum` bag contains 11 bags (5
`faded blue` and 6 `dotted black`), and so on.

You have a **`shiny gold`** bag. If you wanted to carry it in at
least one other bag, how many different bag colors would be valid for the
outermost bag? (In other words: how many colors can, eventually, contain at
least one `shiny gold` bag?)

In the above rules, the following options would be available to you:

-   A `bright white` bag, which can hold your `shiny gold` bag directly.
-   A `muted yellow` bag, which can hold your `shiny gold` bag directly, plus
    some other bags.
-   A `dark orange` bag, which can hold `bright white` and `muted yellow` bags,
    either of which could then hold your `shiny gold` bag.
-   A `light red` bag, which can hold `bright white` and `muted yellow` bags,
    either of which could then hold your `shiny gold` bag.

So, in this example, the number of bag colors that can eventually contain at
least one `shiny gold` bag is **`4`**.

**How many bag colors can eventually contain at least one `shiny gold` bag?**
(The list of rules is quite long; make sure you get all of it.)
"""

# %%
test = """light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags."""

# %%
test.split("\n")


# %%
import time

STARTTIME = time.time()


def find_parents(child_bag):
    for parent in bags_dict:
        contents = bags_dict[parent]
        if child_bag in contents:
            find_parents(parent)
            confirmed_bags.add(parent)
    return


with open("input07.txt", "r") as bags:
    bags = bags.read().split(".\n")[:-1]

bags_dict = {}
for bag in bags:
    bag = bag.replace(" bags", "").replace(" bag", "")  # Remove unnecessary text
    bag = bag.split("contain ")
    bags_dict[bag[0].strip()] = bag[1]
confirmed_bags = set()
find_parents("shiny gold")
print("Total: ", len(confirmed_bags))

print("Elapsed time: ", time.time() - STARTTIME)

# %% [markdown]
# [Python Tutor](https://cscircles.cemc.uwaterloo.ca/visualize/#code=%23+import+time%0A%0A%23+STARTTIME+%3D+time.time()%0A%0A%0Adef+find_parents(child_bag)%3A%0A++++for+parent+in+bags_dict%3A%0A++++++++contents+%3D+bags_dict%5Bparent%5D%0A++++++++if+child_bag+in+contents%3A%0A++++++++++++find_parents(parent)%0A++++++++++++confirmed_bags.add(parent)%0A++++return%0A%0Abags+%3D+%22%22%22light+red+bags+contain+1+bright+white+bag,+2+muted+yellow+bags.%0Adark+orange+bags+contain+3+bright+white+bags,+4+muted+yellow+bags.%0Abright+white+bags+contain+1+shiny+gold+bag.%0Amuted+yellow+bags+contain+2+shiny+gold+bags,+9+faded+blue+bags.%0Ashiny+gold+bags+contain+1+dark+olive+bag,+2+vibrant+plum+bags.%0Adark+olive+bags+contain+3+faded+blue+bags,+4+dotted+black+bags.%0Avibrant+plum+bags+contain+5+faded+blue+bags,+6+dotted+black+bags.%0Afaded+blue+bags+contain+no+other+bags.%0Adotted+black+bags+contain+no+other+bags.%22%22%22+++++++++%0A%0A%23+with+open(%22input07.txt%22,+%22r%22)+as+bags%3A%0Abags+%3D+bags.split(%22.%5Cn%22)%5B%3A-1%5D%0A%0Abags_dict+%3D+%7B%7D%0Afor+bag+in+bags%3A%0A++++bag+%3D+bag.replace(%22+bags%22,+%22%22).replace(%22+bag%22,+%22%22)++%23+Remove+unnecessary+text%0A++++bag+%3D+bag.split(%22contain+%22)%0A++++bags_dict%5Bbag%5B0%5D.strip()%5D+%3D+bag%5B1%5D%0Aconfirmed_bags+%3D+set()%0Afind_parents(%22shiny+gold%22)%0Aprint(%22Total%3A+%22,+len(confirmed_bags))%0A%0A%23+print(%22Elapsed+time%3A+%22,+time.time()+-+STARTTIME)&mode=display&raw_input=&curInstr=248)

# %% [markdown]
"""
\--- Part Two ---
-----------------

It's getting pretty expensive to fly these days - not because of ticket prices,
but because of the ridiculous number of bags you need to buy!

Consider again your `shiny gold` bag and the rules from the above example:

-   `faded blue` bags contain `0` other bags.
-   `dotted black` bags contain `0` other bags.
-   `vibrant plum` bags contain `11` other bags: 5 `faded blue` bags and 6
    `dotted black` bags.
-   `dark olive` bags contain `7` other bags: 3 `faded blue` bags and 4 `dotted
    black` bags.

So, a single `shiny gold` bag must contain 1 `dark olive` bag (and the 7 bags
within it) plus 2 `vibrant plum` bags (and the 11 bags within **each** of
those): `1 + 1*7 + 2 + 2*11` = **`32`** bags!

Of course, the actual rules have a small chance of going several levels deeper
than this example; be sure to count all of the bags, even if the nesting becomes
topologically impractical!

Here's another example:

    shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.


In this example, a single `shiny gold` bag must contain **`126`** other bags.

**How many individual bags are required inside your single `shiny gold` bag?**
"""

# %%
import re
from copy import deepcopy

with open("input07.txt", "r") as file:
    lines = [
        re.sub(" bags?|\.| contain no other", "", line)
        for line in file.read().split("\n")
    ]

rules = {}
for line in lines:
    rule = re.split(" contain |, ", line)
    color = rule[0]
    bag_contents_raw = rule[1:]

    bag_contents = []
    for b in bag_contents_raw:
        content = b.split(" ", 1)
        content[0] = int(content[0])

        bag_contents.append(content)

    rules[color] = bag_contents


def fill_bag(bag, rule):
    """
    Recursively fills the bag.
    Works by replacing each reference to the bag color with the
    bag color's contents.

	Returns a dictionary containing how many of each bag there is.
    """
    num_bags = {}
    for i, content in enumerate(rule):
        content_num = content[0]
        content_color = content[1]
        content_rule = deepcopy(rules[content_color])

        if content_color in num_bags:
            num_bags[content_color] += content_num
        else:
            num_bags[content_color] = content_num

        bag[i][1] = content_rule

        inner_num_bags = fill_bag(bag[i][1], content_rule)
        for color in inner_num_bags:
            num = inner_num_bags[color]
            if color in num_bags:
                num_bags[color] += content_num * num
            else:
                num_bags[color] = content_num * num
    return num_bags


def count_total_bags(num_bags):
    total = 0
    for color in num_bags:
        num = num_bags[color]
        total += num
    return total


bags = deepcopy(rules)

total_bags_all = {}
num_bags_with_shiny_gold = 0
for color in rules:
    rule = rules[color]
    bag = bags[color]

    num_bags = fill_bag(bag, rule)
    total_bags = count_total_bags(num_bags)

    total_bags_all[color] = total_bags

    if "shiny gold" in num_bags:
        num_bags_with_shiny_gold += 1

# Part 1
print("Part 1")
print("Num Bags with Shiny Gold Bag:", num_bags_with_shiny_gold)

print()

# Part 2
print("Part 2")
color = "shiny gold"
if color in total_bags_all:
    print(f"{color:12}Total Bags: {total_bags_all[color]}")
else:
    print(color, "not found!")

print()

# Extra
print("Extra")
# print(total_bags_all) # Warning: This dictionary contains a lot of elements with the actual puzzle input

total_bags_highest_num = max(total_bags_all.values())
total_bags_highest_all = [
    t for t in total_bags_all.items() if t[1] == total_bags_highest_num
]

for t in total_bags_highest_all:
    print(
        f"{t[0]} has the highest number of total bags at {total_bags_highest_num} bags!"
    )
