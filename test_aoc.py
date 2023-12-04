from day1 import (
    compute_sum_of_all_calibration_values_str_nums,
    compute_sum_of_all_calibration_values,
)
from day2 import Game, validate, validate2
from day3 import sum_nums_adjacent_to_symbol, compute_sum_gear_ratios


def test_day1_part1():
    with open("input/day1.txt") as f:
        _calibration_document = f.read()
    assert compute_sum_of_all_calibration_values(_calibration_document) == 54708

    assert (
        compute_sum_of_all_calibration_values_str_nums(
            """1abc2
               pqr3stu8vwx
               a1b2c3d4e5f
               treb7uchet"""
        )
        == 142
    )


def test_day1_part2():
    with open("input/day1_tiny.txt") as f:
        _calibration_document = f.read()
    assert compute_sum_of_all_calibration_values_str_nums(_calibration_document) == 281

    with open("input/day1.txt") as f:
        _calibration_document = f.read()
    assert (
        compute_sum_of_all_calibration_values_str_nums(_calibration_document) == 54087
    )


def test_day2_part1():
    with open("input/day2_tiny.txt") as f:
        games = [Game.parse(game.strip()) for game in f.readlines() if game]
    assert validate(games) == 8

    with open("input/day2.txt") as f:
        games = [Game.parse(game.strip()) for game in f.readlines() if game]
    assert validate(games) == 2541


def test_day2_part2():
    with open("input/day2_tiny.txt") as f:
        games = [Game.parse(game.strip()) for game in f.readlines() if game]
    assert validate2(games) == 2286

    with open("input/day2.txt") as f:
        games = [Game.parse(game.strip()) for game in f.readlines() if game]
    assert validate2(games) == 66016


def test_day3_part1():
    with open("input/day3_tiny.txt") as f:
        assert sum_nums_adjacent_to_symbol(f.read()) == 4361
    with open("input/day3.txt") as f:
        assert sum_nums_adjacent_to_symbol(f.read()) == 538046


def test_day3_part2():
    with open("input/day3_tiny.txt") as f:
        assert compute_sum_gear_ratios(f.read()) == 467835
    with open("input/day3.txt") as f:
        assert compute_sum_gear_ratios(f.read()) == 81709807
