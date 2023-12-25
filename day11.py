from itertools import combinations, accumulate
from typing import Callable

from utils import AOCChallenge


def expand_universe(universe: list[str]) -> list[str]:
    expand_rows = []
    for row in universe:
        expand_rows.append(row)
        if "#" not in row:
            expand_rows.append(row)

    expanded_cols = []
    # transpose
    for col in zip(*expand_rows):
        expanded_cols.append(col)
        if "#" not in col:
            expanded_cols.append(col)

    # transpose back
    expanded_rows = []
    for row in zip(*expanded_cols):
        expanded_rows.append("".join(row))

    return expanded_rows


def find_coords_galaxies(universe: list[str]) -> list[tuple[int, int]]:
    return [
        (row_index, col_index)
        for row_index, row in enumerate(universe)
        for col_index, col in enumerate(row)
        if col == "#"
    ]


def count_empty_rows(universe: list[str]) -> list[int]:
    return list(accumulate((1 if "#" not in row else 0 for row in universe), initial=0))


def count_empty_cols(universe: list[str]) -> list[int]:
    return list(
        accumulate((1 if "#" not in col else 0 for col in zip(*universe)), initial=0)
    )


def count_empty_rows_between(
    empty_rows_count: list[int], row_index1: int, row_index2: int
) -> int:
    row_index1, row_index2 = sorted((row_index1, row_index2))
    return empty_rows_count[row_index2] - empty_rows_count[row_index1]


def count_empty_cols_between(
    empty_cols_count: list[int], col_index1: int, col_index2: int
) -> int:
    col_index1, col_index2 = sorted((col_index1, col_index2))
    return empty_cols_count[col_index2] - empty_cols_count[col_index1]


def manhattan_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_weighted_distance_function(
    universe: list[str], factor: int = 2
) -> Callable[[tuple[int, int], tuple[int, int]], int]:
    # manhattan distance
    empty_rows_count = count_empty_rows(universe)
    empty_cols_count = count_empty_cols(universe)

    def modded_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
        num_empty_rows_between = count_empty_rows_between(empty_rows_count, a[0], b[0])
        num_empty_cols_between = count_empty_cols_between(empty_cols_count, a[1], b[1])
        return manhattan_distance(a, b) + (
            num_empty_rows_between + num_empty_cols_between
        ) * (factor - 1)

    return modded_distance


def all_pairs_shortest_paths_manhattan(
    coords_galaxies: list[tuple[int, int]], distance_func=manhattan_distance
) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    return {(a, b): distance_func(a, b) for a, b in combinations(coords_galaxies, 2)}


def solve(filename: str, factor: int = 2):
    with open(filename) as f:
        universe = f.read().strip().splitlines()
        dists = all_pairs_shortest_paths_manhattan(
            find_coords_galaxies(universe),
            get_weighted_distance_function(universe, factor=factor),
        )
        return sum(dists.values())


def part1(filename: str):
    return solve(filename, factor=2)


def part2(filename: str):
    return solve(filename, factor=1_000_000)


day11 = AOCChallenge(11, part1, part2)
__all__ = [day11]
