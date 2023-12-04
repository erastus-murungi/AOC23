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


def first_true(iterable: Iterable, default=False, pred=None):
    """Returns the first true value in the iterable.

    If no true value is found, returns *default*

    If *pred* is not None, returns the first item
    for which pred(item) is true.

    """
    # first_true([a,b,c], x) --> a or b or c or x
    # first_true([a,b], x, f) --> a if f(a) else b if f(b) else x
    return next(filter(pred, iterable), default)


def compute_sum_of_all_calibration_values(calibration_document: str) -> int:
    """
    :param calibration_document: A string containing the calibration document
    :return: The sum of all the calibration values

    >>> compute_sum_of_all_calibration_values("1abc2\\npqr3stu8vwx\\na1b2c3d4e5f\\ntreb7uchet")
    142
    """
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


def compute_sum_of_all_calibration_values_str_nums(calibration_document: str) -> int:
    """
    :param calibration_document: A string containing the calibration document
    :return: The sum of all the calibration values

    >>> compute_sum_of_all_calibration_values_str_nums("1abc2\\npqr3stu8vwx\\na1b2c3d4e5f\\ntreb7uchet")
    101
    """

    def first_digit(input_str):
        return next((char for char in input_str if char.isdigit()), None)

    cleaned_lines = []
    for line in calibration_document.splitlines():
        cleaned_line = "".join(
            STRING_NUMBERS.get(match.group(0), char)
            for char in line
            if (
                match := re.match(
                    r"(one|two|three|four|five|six|seven|eight|nine)", char
                )
            )
        )
        cleaned_lines.append(cleaned_line)
    return sum(
        int(f"{first_digit(line)}{first_digit(line[::-1])}")
        for line in cleaned_lines
        if first_digit(line) and first_digit(line[::-1])
    )


if __name__ == "__main__":
    with open("day1.txt") as f:
        _calibration_document = f.read()
    print(compute_sum_of_all_calibration_values_str_nums(_calibration_document))
