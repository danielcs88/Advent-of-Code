# %% [markdown]
# ## --- Day 14: Reindeer Olympics ---
#
# This year is the Reindeer Olympics! Reindeer can fly at high speeds, but must
# rest occasionally to recover their energy. Santa would like to know which of
# his reindeer is fastest, and so he has them race.
#
# Reindeer can only either be **flying** (always at their top speed) or
# **resting** (not moving at all), and always spend whole seconds in either
# state.
#
# For example, suppose you have the following Reindeer:
#
# - Comet can fly **14 km/s for 10 seconds**, but then must rest for **127
#   seconds**.
# - Dancer can fly **16 km/s for 11 seconds**, but then must rest for **162
#   seconds**.
#
# After one second, Comet has gone 14 km, while Dancer has gone 16 km. After ten
# seconds, Comet has gone 140 km, while Dancer has gone 160 km. On the eleventh
# second, Comet begins resting (staying at 140 km), and Dancer continues on for
# a total distance of 176 km. On the 12th second, both reindeer are resting.
# They continue to rest until the 138th second, when Comet flies for another ten
# seconds. On the 174th second, Dancer flies for another 11 seconds.
#
# In this example, after the 1000th second, both reindeer are resting, and Comet
# is in the lead at **`1120`** km (poor Dancer has only gotten `1056` km by that
# point). So, in this situation, Comet would win (if the race ended at 1000
# seconds).
#
# Given the descriptions of each reindeer (in your puzzle input), after exactly
# `2503` seconds, **what distance has the winning reindeer traveled**?

# %%
import re

import pandas as pd
from IPython.display import display

# %%
test = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""

# %%
INPUT_14 = aoc_open_input("input_14.txt")


# %%
def parse_reindeer_specs(input_str: str) -> dict[str, dict[str, int]]:
    regex = re.compile(
        r"(\w+)(\s)(can fly)(\s)(\d+)(\s)(km/s for)(\s)(\d+)(\s)(seconds, but then must rest for )(\d+)",
    )
    match_array = regex.findall(input_str)

    reindeer_specs = {}

    for m in match_array:
        name = m[0]
        speed, flight_time, rest_time = map(int, (m[4], m[8], m[11]))
        reindeer_specs[name] = {
            "speed": speed,
            "flight_time": flight_time,
            "rest_time": rest_time,
        }

    return reindeer_specs


def calculate_total_miles(
    reindeer_specs: dict[str, dict[str, int]], time_threshold: int
) -> int:
    total_miles = []

    for _, specs in reindeer_specs.items():
        turns = 0
        time = 0
        miles = 0

        speed = specs["speed"]
        flight_time = specs["flight_time"]
        rest_time = specs["rest_time"]

        while time < time_threshold:
            flight_turn = turns % 2 == 0

            if flight_turn:
                time_left = time_threshold - time
                if time_left > (speed * flight_time):
                    miles += speed * flight_time
                    time += flight_time
                    time_left -= flight_time
                else:
                    miles += speed * min(time_left, flight_time)
                    time += time_left
            elif time_left > rest_time:
                time += rest_time
                time_left -= rest_time
            else:
                time += time_left
                time_left = 0

            turns += 1

        total_miles.append(miles)
        specs["total_travelled"] = miles

    display(
        pd.DataFrame(reindeer_specs).T.sort_values("total_travelled", ascending=False)
    )

    return max(total_miles)


def part_one(input_str: str, time_threshold: int) -> int:
    reindeer_specs = parse_reindeer_specs(input_str)
    return calculate_total_miles(reindeer_specs, time_threshold)


# %%
aoc_answer_display(part_one(test, 1000))

# %%
# part_one(INPUT_14, 2503)

# %% [markdown]
# ## --- Part Two ---
#
# Seeing how reindeer move in bursts, Santa decides he's not pleased with the
# old scoring system.
#
# Instead, at the end of each second, he awards one point to the reindeer
# currently in the lead. (If there are multiple reindeer tied for the lead, they
# each get one point.) He keeps the traditional 2503 second time limit, of
# course, as doing otherwise would be entirely ridiculous.
#
# Given the example reindeer from above, after the first second, Dancer is in
# the lead and gets one point. He stays in the lead until several seconds into
# Comet's second burst: after the 140th second, Comet pulls into the lead and
# gets his first point. Of course, since Dancer had been in the lead for the 139
# seconds before that, he has accumulated 139 points by the 140th second.
#
# After the 1000th second, Dancer has accumulated **`689`** points, while poor
# Comet, our old champion, only has `312`. So, with the new scoring system,
# Dancer would win (if the race ended at 1000 seconds).
#
# Again given the descriptions of each reindeer (in your puzzle input), after
# exactly `2503` seconds, **how many points does the winning reindeer have**?

# %%
from IPython.core.debugger import set_trace

# %%
test_specs = parse_reindeer_specs(test)
test_specs


# %%
def max_pole_position_count(
    reindeer_specs: dict[str, dict[str, int]], time_threshold: int
) -> int:
    position_sec_by_sec = {}

    for r, s in reindeer_specs.items():
        position = []
        miles = 0
        turns = 0

        speed, flight_time, rest_time = s.values()

        while len(position) < time_threshold:
            if turns % 2 == 0:
                for _ in range(flight_time):
                    miles += speed
                    position.append(miles)

            else:
                for _ in range(rest_time):
                    miles += 0
                    position.append(miles)

            turns += 1
        position_sec_by_sec[r] = position[:time_threshold]

    all_pos = pd.DataFrame(position_sec_by_sec)
    all_pos.plot(title="Positions")
    final_results = (
        all_pos.T.pipe(lambda d: (d >= d.max()))
        .T.map(int)
        .sum()
        .sort_values(ascending=False)
    )

    display(final_results.to_frame("Pole Position Counts"))
    return final_results.max()


# %%
def part_two(input_str: str, time_threshold: int) -> int:
    reindeer_specs = parse_reindeer_specs(input_str)
    return max_pole_position_count(reindeer_specs, time_threshold)


# %%
aoc_answer_display(part_two(test, 1000))

# %%
aoc_answer_display(part_two(INPUT_14, 2503))
