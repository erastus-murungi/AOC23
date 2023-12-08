from day1 import (
    compute_sum_of_all_calibration_values_str_nums,
    compute_sum_of_all_calibration_values,
)
from day2 import day2
from day3 import day3
from day4 import day4
from day5 import day5
from day6 import day6
from day7 import day7
from day8 import day8


def test_day1_part1():
    with open("input/day1_tiny.txt") as f:
        calibration_document = f.read()
    assert compute_sum_of_all_calibration_values(calibration_document) == 142

    with open("input/day1.txt") as f:
        calibration_document = f.read()
    assert compute_sum_of_all_calibration_values(calibration_document) == 54708


def test_day1_part2():
    with open("input/day1_tiny.txt") as f:
        calibration_document = f.read()
    assert compute_sum_of_all_calibration_values_str_nums(calibration_document) == 281

    with open("input/day1.txt") as f:
        calibration_document = f.read()
    assert compute_sum_of_all_calibration_values_str_nums(calibration_document) == 54087


def test_day2_part1():
    assert day2.part1("input/day2_tiny.txt") == 8
    assert day2.part2("input/day2_tiny.txt") == 2286

    assert day2.part1("input/day2.txt") == 2541
    assert day2.part2("input/day2.txt") == 66016


def test_day3():
    assert day3.part1("input/day3_tiny.txt") == 4361
    assert day3.part2("input/day3_tiny.txt") == 467835

    assert day3.part1("input/day3.txt") == 538046
    assert day3.part2("input/day3.txt") == 81709807


def test_day4():
    assert day4.part1("input/day4_tiny.txt") == 13
    assert day4.part2("input/day4_tiny.txt") == 30

    assert day4.part1("input/day4.txt") == 24160
    assert day4.part2("input/day4.txt") == 5659035


def test_day5():
    assert day5.part1("input/day5_tiny.txt") == 35
    assert day5.part2("input/day5_tiny.txt") == 46

    assert day5.part1("input/day5.txt") == 403695602
    assert day5.part2("input/day5.txt") == 219529182


def test_day6():
    assert day6.part1("input/day6_tiny.txt") == 288
    assert day6.part2("input/day6_tiny.txt") == 71503

    assert day6.part1("input/day6.txt") == 2756160
    assert day6.part2("input/day6.txt") == 34788142


def test_day7():
    assert day7.part1("input/day7_tiny.txt") == 6440
    assert day7.part2("input/day7_tiny.txt") == 5905

    assert day7.part1("input/day7.txt") == 251216224
    assert day7.part2("input/day7.txt") == 250825971


def test_day8():
    assert day8.part1("input/day8_tiny.txt") == 2
    assert day8.part2("input/day8_tiny2.txt") == 6

    assert day8.part1("input/day8.txt") == 13019
    assert day8.part2("input/day8.txt") == 13524038372771
