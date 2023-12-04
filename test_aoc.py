from day1 import (
    compute_sum_of_all_calibration_values_str_nums,
    compute_sum_of_all_calibration_values,
)
from day2 import Game, validate, validate2
from day3 import sum_nums_adjacent_to_symbol, compute_sum_gear_ratios
from day4 import compute_total_card_value, compute_num_scratchcards_won


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


def test_day4_part1():
    with open("input/day4_tiny.txt") as f:
        cards = f.read()
    assert compute_total_card_value(cards) == 13

    with open("input/day4.txt") as f:
        cards = f.read()
    assert compute_total_card_value(cards) == 24160


def test_day4_part2():
    with open("input/day4_tiny.txt") as f:
        cards = f.read()
    assert compute_num_scratchcards_won(cards) == 30

    with open("input/day4.txt") as f:
        cards = f.read()
    assert compute_num_scratchcards_won(cards) == 5659035
