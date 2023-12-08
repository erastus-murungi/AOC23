import re
import numpy as np


def extract_numbers(seeds_str: str, syntax=re.compile(r"(\d+)")) -> tuple[int]:
    return tuple(map(int, syntax.findall(seeds_str)))


def parse_input(race_data: str) -> tuple[tuple[int, int]]:
    time_str, distance_str = race_data.strip().splitlines()
    return tuple(zip(extract_numbers(time_str), extract_numbers(distance_str)))


def parse_input_bad_kerning(race_data: str) -> tuple[int, int]:
    time_str, distance_str = race_data.strip().splitlines()
    return (
        int("".join(re.findall(r"(\d+)", time_str))),
        int("".join(re.findall(r"(\d+)", distance_str))),
    )


def compute_num_winning_ways_one_pair(time_limit: int, record_distance: int) -> int:
    [x1, x2] = np.sort(
        np.floor(np.roots([1, -(time_limit - 0.01), record_distance + 0.01]))
    )
    minimum = int(np.ceil(x1))
    maximum = int(np.floor(x2))
    return maximum - minimum
    # num_ways = 0
    # for charging_time in range(starting_points, time_limit):
    #     if (time_limit - charging_time) * charging_time > record_distance:
    #         # print(
    #         #     f"Hold the button for {charging_time} milliseconds. "
    #         #     f"After its remaining {time_limit - charging_time} milliseconds of travel time, "
    #         #     f"the boat will have gone {(time_limit - charging_time)*charging_time} millimeters."
    #         # )
    #         num_ways += 1
    # return num_ways


def compute_num_winning_ways(data: str) -> int:
    race_info = parse_input(data)
    return np.prod(
        [
            compute_num_winning_ways_one_pair(time_limit, record_distance)
            for time_limit, record_distance in race_info
        ]
    )


def compute_num_winning_ways_bad_kerning(data: str) -> int:
    time_limit, record_distance = parse_input_bad_kerning(data)
    return compute_num_winning_ways_one_pair(time_limit, record_distance)


if __name__ == "__main__":
    with open("input/day6_tiny.txt") as f:
        print(compute_num_winning_ways_bad_kerning(f.read()))
