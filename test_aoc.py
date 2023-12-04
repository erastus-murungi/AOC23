from day1 import (
    compute_sum_of_all_calibration_values_str_nums,
    compute_sum_of_all_calibration_values,
)
from day2 import Game, validate, validate2


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


game_str = """  Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
                Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
                Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
                Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
                Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
            """


def test_day2_part1():
    games = [Game.parse(game.strip()) for game in game_str.strip().splitlines() if game]
    assert validate(games) == 8

    with open("input/day2.txt") as f:
        games = [Game.parse(game.strip()) for game in f.readlines() if game]
    assert validate(games) == 2541


def test_day2_part2():
    games = [Game.parse(game.strip()) for game in game_str.strip().splitlines() if game]
    assert validate2(games) == 2286

    with open("input/day2.txt") as f:
        games = [Game.parse(game.strip()) for game in f.readlines() if game]
    assert validate2(games) == 66016
