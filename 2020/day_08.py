# %% [markdown]
"""
\--- Day 8: Handheld Halting ---
--------------------------------

Your flight to the major airline hub reaches cruising altitude without incident.
While you consider checking the in-flight menu for one of those drinks that come
with a little umbrella, you are interrupted by the kid sitting next to you.

Their [handheld game
console](https://en.wikipedia.org/wiki/Handheld**game**console) won't turn on!
They ask if you can take a look.

You narrow the problem down to a strange **infinite loop** in the boot code
(your puzzle input) of the device. You should be able to fix it, but first you
need to be able to run the code in isolation.

The boot code is represented as a text file with one **instruction** per line of
text. Each instruction consists of an **operation** (`acc`, `jmp`, or `nop`) and
an **argument** (a signed number like `+4` or `-20`).

-   `acc` increases or decreases a single global value called the
    **accumulator** by the value given in the argument. For example, `acc +7`
    would increase the accumulator by 7. The accumulator starts at `0`. After an
    `acc` instruction, the instruction immediately below it is executed next.

-   `jmp` **jumps** to a new instruction relative to itself. The next
    instruction to execute is found using the argument as an **offset** from the
    `jmp` instruction; for example, `jmp +2` would skip the next instruction,
    `jmp +1` would continue to the instruction immediately below it, and `jmp
    -20` would cause the instruction 20 lines above to be executed next.

-   `nop` stands for **No OPeration** - it does nothing. The instruction
    immediately below it is executed next.

For example, consider the following program:

    nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6


These instructions are visited in this order:

    nop +0  | 1
    acc +1  | 2, 8(!)
    jmp +4  | 3
    acc +3  | 6
    jmp -3  | 7
    acc -99 |
    acc +1  | 4
    jmp -4  | 5
    acc +6  |


First, the `nop +0` does nothing. Then, the accumulator is increased from 0 to 1
(`acc +1`) and `jmp +4` sets the next instruction to the other `acc +1` near the
bottom. After it increases the accumulator from 1 to 2, `jmp -4` executes,
setting the next instruction to the only `acc +3`. It sets the accumulator to 5,
and `jmp -3` causes the program to continue back at the first `acc +1`.

This is an **infinite loop**: with this sequence of jumps, the program will run
forever. The moment the program tries to run any instruction a second time, you
know it will never terminate.

Immediately **before** the program would run an instruction a second time, the
value in the accumulator is **`5`**.

Run your copy of the boot code. Immediately before any instruction is executed a
second time, **what value is in the accumulator?**
"""

# %%

instructions = [line.strip() for line in open("input08.txt", "r")]
ACC = 0


def part1():
    global ACC
    completedIndexes = []
    lineIndex = 0
    while lineIndex < len(instructions):
        # first test to make sure if this line has been repeated
        if lineIndex in completedIndexes:
            print("Loop detected. ACC value is", ACC)
            break
        else:
            # no loop detected, execute instruction
            completedIndexes.append(lineIndex)
            instruction, value = instructions[lineIndex].split(" ")
            value = int(value)
            if instruction == "acc":
                ACC += value
                lineIndex += 1
            elif instruction == "jmp":
                lineIndex += value
            elif instruction == "nop":
                lineIndex += 1


part1()

"""
For testing:
BaseInstructions = [
        "nop +0",
        "acc +1",
        "jmp +4",
        "acc +3",
        "jmp -3",
        "acc -99",
        "acc +1",
        "jmp -4",   # this needs to be changed to nop to avoid loop
        "acc +6"
        ]
"""

BaseInstructions = open("input08.txt", "r").readlines()

ACC = 0


def execute(instructions):
    """
        runs through each line of the code, executing it accordingly.
        before it runs a line, it checks to see if that particular line
        has been run once before. if so, we know we have a loop.
    """

    global ACC

    # reset ACC to 0 because we want only to count the ACC value for this
    # single iteration that has a single line changed
    ACC = 0

    # execute the instructions and return the line number at which loop occurs
    completedIndexes = []
    lineIndex = 0
    while lineIndex < len(instructions):
        # first test to make sure if this line has been repeated
        if lineIndex in completedIndexes:
            return False
        # no loop detected, execute instruction
        completedIndexes.append(lineIndex)
        instruction, value = instructions[lineIndex].split(" ")
        value = int(value)
        if instruction == "acc":
            ACC += value
            lineIndex += 1
        elif instruction == "jmp":
            lineIndex += value
        elif instruction == "nop":
            lineIndex += 1
    # looped through all instructions without a double-line execution
    return True


def swapLine(i):
    """
        resets the instructions to the original version, then swaps the one
        line at index i and returns the new instructions to be tested.
    """

    # copy the original instructions
    instructions = BaseInstructions.copy()
    lineArray = instructions[i].split(" ")

    # inelegant but straightforward toggle of jmp/nop
    if lineArray[0] == "jmp":
        lineArray[0] = "nop"
        instructions[i] = " ".join(lineArray)
    elif lineArray[0] == "nop":
        lineArray[0] = "jmp"
        instructions[i] = " ".join(lineArray)

    # return the new instructions to check, with a single line switched
    return instructions


# array of lines we've already tried swapping, to prevent infinite loop
# of trying the same line over and over
triedLines = []


def part2(instructions):
    """
        check if execute() returns true, in which case this particular version of
        the instructions executes fine.
        if false, iterate through the lines, finding the first line that hasn't been
        tried yet (not in triedLines). swap that line and call this function again
        with the new instructions and try again.
    """
    global triedLines

    # if this executes fine and returns True, great! done.
    if execute(instructions):
        print(ACC)

    # otherwise,
    else:
        # iterate through each line
        i = 0
        while i < len(instructions):

            # if the line hasn't been tried before
            if i not in triedLines:

                # get a new set of instructions with this new line swapped
                instructions = swapLine(i)
                triedLines.append(i)
                break

            i += 1

        # with the new instructions, with one line swapped, try to run it again
        part2(instructions)


# run main program
part2(BaseInstructions)
