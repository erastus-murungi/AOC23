"""
--- Day 2: Cube Conundrum ---
You're launched high into the atmosphere!
The apex of your trajectory just barely reaches the surface of a large island floating in the sky.
You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow.
He'll be happy to explain the situation, but it's a bit of a walk, so you have some time.
They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue.
Each time you play this game, he will hide a secret number of cubes of each color in the bag,
and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag,
grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input).
Each game is listed with its ID number (like the 11 in Game 11: ...)
followed by a semicolon-separated list of subsets of cubes that were revealed from the bag
(like 3 red, 5 green, 4 blue).

You play several games and record the information from each game (your puzzle input).
Each game is listed with its ID number (like the 11 in Game 11: ...)
followed by a semicolon-separated list of subsets of cubes that were revealed from
the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again).
The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes;
the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes,
13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration.
 However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once;
 similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once.
 If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes,
 and 14 blue cubes. What is the sum of the IDs of those games?
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from pprint import pprint


class ColorChoice(Enum):
    red = "red"
    green = "green"
    blue = "blue"


@dataclass(frozen=True)
class ColorPick:
    color: ColorChoice
    quantity: int


@dataclass
class GameRound:
    picks: list[ColorPick]


@dataclass
class Game:
    game_id: int
    game_rounds: list[GameRound]

    @staticmethod
    def parse(game_description: str) -> Game:
        """
        Parses a game string into a Game object

        :param game_description: The game string to parse
        :return: A ColorGame object
        """
        game_id_str, *sets_str = game_description.split(":")
        assert (
            len(sets_str) == 1
        ), f"Game description {game_description} should only have one set"
        game_rounds = []
        for round_str in sets_str[0].split(";"):
            color_picks_in_round = []
            for match in re.finditer(r"(\d+)(\s*)(blue|red|green)", round_str):
                quantity = int(match.group(1))
                color_name = match.group(3)
                color_picks_in_round.append(
                    ColorPick(ColorChoice[color_name], quantity)
                )
            game_rounds.append(GameRound(color_picks_in_round))
        return Game(int(re.findall(r"(\d+)", game_id_str)[0]), game_rounds)


def validate(
    list_games: list[Game],
    max_red_cubes: int = 12,
    max_green_cubes: int = 13,
    max_blue_cubes: int = 14,
) -> int:
    sum_games_ids = 0
    for game in list_games:
        game_valid = True
        for game_round in game.game_rounds:
            red_cubes = 0
            green_cubes = 0
            blue_cubes = 0
            for color_pick in game_round.picks:
                if color_pick.color == ColorChoice.red:
                    red_cubes += color_pick.quantity
                elif color_pick.color == ColorChoice.green:
                    green_cubes += color_pick.quantity
                elif color_pick.color == ColorChoice.blue:
                    blue_cubes += color_pick.quantity
            if (
                red_cubes > max_red_cubes
                or green_cubes > max_green_cubes
                or blue_cubes > max_blue_cubes
            ):
                game_valid = False
                break
        if game_valid:
            sum_games_ids += game.game_id
    return sum_games_ids


if __name__ == "__main__":
    # game_str = """  Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    #                 Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    #                 Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    #                 Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    #                 Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    #             """
    # games = [Game.parse(game.strip()) for game in game_str.strip().splitlines() if game]
    # pprint(games)
    # pprint(
    #     validate(
    #         games,
    #         max_red_cubes=12,
    #         max_green_cubes=13,
    #         max_blue_cubes=14,
    #     )
    # )
    with open("day2.txt") as f:
        games = [Game.parse(game.strip()) for game in f.readlines() if game]
    pprint(
        validate(
            games,
            max_red_cubes=12,
            max_green_cubes=13,
            max_blue_cubes=14,
        )
    )
