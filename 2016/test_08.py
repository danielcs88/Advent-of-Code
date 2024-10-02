#!/usr/bin/env python3

import itertools
import pathlib
import sys
import time
from collections import deque


class Screen:
    def __init__(self, puzzle_input, cols=50, rows=6) -> None:
        self.insts = []
        for line in puzzle_input.strip().splitlines():
            tokens = line.split(" ")
            match tokens[0]:
                case "rect":
                    a, b = tokens[1].split("x")
                    self.insts.append(("rect", int(a), int(b)))
                case _:
                    assert tokens[0] == "rotate"
                    a = int(tokens[2][2:])
                    b = int(tokens[4])
                    self.insts.append((tokens[1], a, b))

        self.screen = [deque(0 for _ in range(cols)) for _ in range(rows)]

    def pixels_on(self) -> int:
        """Count the number of on pixels in the current state."""
        return sum(sum(row) for row in self.screen)

    def run(self) -> None:
        """Run the instructions."""
        for inst, a, b in self.insts:
            match inst:
                case "rect":
                    self.rect(a, b)
                case "column":
                    self.rotate_col(a, b)
                case "row":
                    self.rotate_row(a, b)
                case _:
                    raise
            self.animate()

    def rect(self, cols, rows):
        """Turn on a given rectangle."""
        for r, c in itertools.product(range(rows), range(cols)):
            self.screen[r][c] = 1

    def rotate_col(self, x, by):
        """Rotate a column."""
        col = deque(row[x] for row in self.screen)
        col.rotate(by)
        for row, new_val in zip(self.screen, col):
            row[x] = new_val

    def rotate_row(self, y, by):
        """Rotate a row."""
        self.screen[y].rotate(by)

    def to_string(self, fancy=False) -> str:
        """Print the screen."""
        s = ""
        if fancy:
            s = "┌"
            s += "─" * len(self.screen[0])
            s += "┐\n"
        for row in self.screen:
            if fancy:
                s += "│"
            for val in row:
                if val == 0 and fancy:
                    s += " "
                elif val == 0:
                    s += "."
                elif fancy:
                    s += "█"
                else:
                    s += "#"
            if fancy:
                s += "│"
            s += "\n"
        if fancy:
            s += "└"
            s += "─" * len(self.screen[0])
            s += "┘"
        return s.rstrip()

    def animate(self) -> None:
        """Generate an animation for the screen as it changes."""
        print("\033[H", end="")
        print(self.to_string(fancy=True))
        # print(self.to_string(fancy=False))
        time.sleep(0.05)


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    screen = Screen(puzzle_input)
    screen.run()
    solution1 = screen.pixels_on()
    solution2 = "\n" + screen.to_string(True)

    return solution1, solution2


if __name__ == "__main__":
    infile = (
        sys.argv[1]
        if len(sys.argv) > 1
        else pathlib.Path(__file__).parent / "input_08.txt"
    )
    puzzle_input = pathlib.Path(infile).read_text().strip()
    solution1, solution2 = solve(puzzle_input)
    if solution1:
        print(f" part1: {solution1}")
    if solution2:
        print(f" part2: {solution2}")
