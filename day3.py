"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station;
he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise.
"Sorry, I wasn't expecting anyone!
The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine,
but nobody can figure out which one. If you can add up all the part numbers in the engine schematic,
it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine.
There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol,
even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol:
 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number;
 their sum is 4361.

Of course, the actual engine schematic is much larger.

 What is the sum of all of the part numbers in the engine schematic?
"""
from utils import AOCChallenge


def is_symbol(char: str):
    return not char.isdigit() and char != "."


def parse_schematic(data: str):
    lines = data.strip().splitlines()
    num_rows = len(lines)
    num_cols = len(lines[0])
    return lines, (num_rows, num_cols)


def sum_of_part_numbers_adjacent_to_symbols(
    table: list[str],
    row_index: int,
    col_index: int,
    span: int,
    num_rows: int,
    num_cols: int,
) -> bool:
    for index, symbol in enumerate(
        table[row_index][col_index : col_index + span], col_index
    ):
        # grab the current row
        row = table[row_index]
        # check left, right
        if index > 0 and is_symbol(row[index - 1]):
            return True
        if index < num_cols - 1 and is_symbol(row[index + 1]):
            return True

        # check up, down
        if row_index > 0 and is_symbol(table[row_index - 1][index]):
            return True
        if row_index < num_rows - 1 and is_symbol(table[row_index + 1][index]):
            return True

        # check diagonals
        if row_index > 0 and index > 0 and is_symbol(table[row_index - 1][index - 1]):
            return True
        if (
            row_index > 0
            and index < num_cols - 1
            and is_symbol(table[row_index - 1][index + 1])
        ):
            return True
        if (
            row_index < num_rows - 1
            and index > 0
            and is_symbol(table[row_index + 1][index - 1])
        ):
            return True
        if (
            row_index < num_rows - 1
            and index < num_cols - 1
            and is_symbol(table[row_index + 1][index + 1])
        ):
            return True
    return False


def parse_number(s: str) -> str:
    digits = []
    for char in s:
        if char.isdigit():
            digits.append(char)
        else:
            return "".join(digits)
    return "".join(digits)


def parse_number_around(s: str, index: int) -> tuple[str, tuple[int, int]]:
    digits = []
    # traverse back and the digits
    for char in s[index::-1]:
        if char.isdigit():
            digits.append(char)
        else:
            break
    start_index = index - len(digits)
    digits = digits[::-1]
    # traverse forward and the digits
    for char in s[index + 1 :]:
        if char.isdigit():
            digits.append(char)
        else:
            break
    return "".join(digits), (start_index, start_index + len(digits))


def part1(filename: str):
    with open(filename) as f:
        sum_nums = 0
        lines, (num_rows, num_cols) = parse_schematic(f.read())
        for row, line in enumerate(lines):
            col = 0
            while col < len(line):
                char = line[col]
                if char.isdigit():
                    number = parse_number(line[col:])
                    span = len(number)
                    if sum_of_part_numbers_adjacent_to_symbols(
                        lines, row, col, span, num_rows, num_cols
                    ):
                        sum_nums += int(number)
                    col = col + span
                else:
                    col += 1
        return sum_nums


# --- Part Two ---
# The engineer finds the missing part and installs it in the engine!
# As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.
#
# You don't seem to be going very fast, though. Maybe something is still wrong?
# Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.
#
# Before you can explain the situation, she suggests that you look out the window.
# There stands the engineer, holding a phone in one hand and waving with the other.
# You're going so slowly that you haven't even left the station. You exit the gondola.
#
# The missing part wasn't the only issue - one of the gears in the engine is wrong.
# A gear is any * symbol that is adjacent to exactly two part numbers.
# Its gear ratio is the result of multiplying those two numbers together.
#
# This time, you need to find the gear ratio of every gear and
# add them all up so that the engineer can figure out which gear needs to be replaced.
#
# Consider the same engine schematic again:
#
# 467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..
# In this schematic, there are two gears.
# The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345.
# The second gear is in the lower right; its gear ratio is 451490.
# (The * adjacent to 617 is not a gear because it is only adjacent to one part number.)
# Adding up all of the gear ratios produces 467835.


def compute_gear_ratio(
    table: list[str], row_index: int, col_index: int, num_rows: int, num_cols: int
) -> int:
    assert table[row_index][col_index] == "*", "Not a gear"
    part_numbers = set()
    # go round the gear and collect the part numbers
    # check left, right
    if col_index > 0 and table[row_index][col_index - 1].isdigit():
        part_numbers.add(parse_number_around(table[row_index], col_index - 1))
    if col_index < num_cols - 1 and table[row_index][col_index + 1].isdigit():
        part_numbers.add(parse_number_around(table[row_index], col_index + 1))

    # check up, down
    if row_index > 0 and table[row_index - 1][col_index].isdigit():
        part_numbers.add(parse_number_around(table[row_index - 1], col_index))
    if row_index < num_rows - 1 and table[row_index + 1][col_index].isdigit():
        part_numbers.add(parse_number_around(table[row_index + 1], col_index))

    # check diagonals
    if (
        row_index > 0
        and col_index > 0
        and table[row_index - 1][col_index - 1].isdigit()
    ):
        part_numbers.add(parse_number_around(table[row_index - 1], col_index - 1))
    if (
        row_index > 0
        and col_index < num_cols - 1
        and table[row_index - 1][col_index + 1].isdigit()
    ):
        part_numbers.add(parse_number_around(table[row_index - 1], col_index + 1))
    if (
        row_index < num_rows - 1
        and col_index > 0
        and table[row_index + 1][col_index - 1].isdigit()
    ):
        part_numbers.add(parse_number_around(table[row_index + 1], col_index - 1))
    if (
        row_index < num_rows - 1
        and col_index < num_cols - 1
        and table[row_index + 1][col_index + 1].isdigit()
    ):
        part_numbers.add(parse_number_around(table[row_index + 1], col_index + 1))
    if len(part_numbers) == 2:
        num1, _ = part_numbers.pop()
        num2, _ = part_numbers.pop()
        return int(num1) * int(num2)
    else:
        return 0


def part2(filename: str) -> int:
    with open(filename) as f:
        sum_gear_ratios = 0
        lines, (num_rows, num_cols) = parse_schematic(f.read())
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if char == "*":
                    gear_ratio = compute_gear_ratio(lines, row, col, num_rows, num_cols)
                    sum_gear_ratios += gear_ratio
        return sum_gear_ratios


day3 = AOCChallenge(3, part1, part2)
__all__ = [day3]
