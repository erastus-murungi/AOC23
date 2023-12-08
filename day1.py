"""
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look.
The Elves have even given you a map;
on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations,
you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar;
the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you
("the sky") and why your map looks mostly blank ("you sure ask a lot of questions")
and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves
are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration
document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her
art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text;
each line originally contained a specific calibration value that the Elves now need to recover.
On each line, the calibration value can be found by combining the first digit and the last digit (in that order)
to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all the calibration values?
"""
import re
from typing import Iterable

from utils import AOCChallenge


def first_true(iterable: Iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


def part1(filename: str) -> int:
    with open(filename) as f:
        calibration_document = f.read().strip()
        return sum(
            int(
                f"{first_true(line, pred=str.isdigit)}{first_true(reversed(line), pred=str.isdigit)}"
            )
            for line in calibration_document.splitlines()
        )


# --- Part Two ---
# It looks like some of the digits are actually spelled out with letters:
# one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
#
# Equipped with this new information, you now need to find the real first and last digit on each line. For example:

STRING_NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def part2(filename: str) -> int:
    with open(filename) as f:
        calibration_document = f.read().strip()
        cleaned_lines = []
        for line in calibration_document.splitlines():
            cleaned_line = []
            for index, char in enumerate(line):
                if re_match := re.match(
                    r"one|two|three|four|five|six|seven|eight|nine", line[index:]
                ):
                    cleaned_line.append(STRING_NUMBERS.get(re_match.group(0)))
                else:
                    cleaned_line.append(char)
            cleaned_lines.append("".join(cleaned_line))
        return sum(
            int(
                f"{first_true(line, pred=str.isdigit)}{first_true(reversed(line), pred=str.isdigit)}"
            )
            for line in cleaned_lines
        )


day1 = AOCChallenge(1, part1, part2)
__all__ = [day1]
