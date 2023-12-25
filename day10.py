from __future__ import annotations

from collections import deque, defaultdict
from enum import Enum
from sys import maxsize, setrecursionlimit
from typing import Literal

from termcolor import colored

from utils import AOCChallenge

inf = maxsize
setrecursionlimit(10000)


class Direction(Enum):
    VERTICAL = "|"
    HORIZONTAL = "─"
    CURVE_RIGHT_DOWN = "└"
    CURVE_LEFT_DOWN = "┘"
    CURVE_RIGHT_UP = "┌"
    CURVE_LEFT_UP = "┐"
    GROUND = " "
    STARTING = "X"

    @staticmethod
    def from_tokens(token: str) -> Direction:
        match token:
            case Direction.VERTICAL.value:
                return Direction.VERTICAL
            case Direction.HORIZONTAL.value:
                return Direction.HORIZONTAL
            case Direction.CURVE_RIGHT_DOWN.value:
                return Direction.CURVE_RIGHT_DOWN
            case Direction.CURVE_LEFT_DOWN.value:
                return Direction.CURVE_LEFT_DOWN
            case Direction.CURVE_RIGHT_UP.value:
                return Direction.CURVE_RIGHT_UP
            case Direction.CURVE_LEFT_UP.value:
                return Direction.CURVE_LEFT_UP
            case Direction.GROUND.value:
                return Direction.GROUND
            case Direction.STARTING.value:
                return Direction.STARTING
            case _:
                raise ValueError(f"Invalid character {token}")


class Grid(list[list[Direction]]):
    def __init__(self, grid: list[list[Direction]]):
        super().__init__(grid)

    @staticmethod
    def parse_input(data: str) -> Grid:
        lines = (
            data.strip()
            .replace("L", Direction.CURVE_RIGHT_DOWN.value)
            .replace("J", Direction.CURVE_LEFT_DOWN.value)
            .replace("F", Direction.CURVE_RIGHT_UP.value)
            .replace("7", Direction.CURVE_LEFT_UP.value)
            .replace("-", Direction.HORIZONTAL.value)
            .replace("S", Direction.STARTING.value)
            .replace(".", " ")
            .splitlines()
        )
        return Grid(
            [[Direction.from_tokens(token) for token in line] for line in lines]
        )

    def can_go_left(self, row: int, col: int) -> bool:
        assert 0 <= row < len(self)
        assert 0 <= col < len(self[row])

        frm = self[row][col]
        if col - 1 >= 0:
            to = self[row][col - 1]
            return frm in (
                Direction.HORIZONTAL,
                Direction.CURVE_LEFT_UP,
                Direction.CURVE_LEFT_DOWN,
                Direction.STARTING,
            ) and to in (
                Direction.HORIZONTAL,
                Direction.CURVE_RIGHT_UP,
                Direction.CURVE_RIGHT_DOWN,
                Direction.STARTING,
            )
        return False

    def can_go_right(self, row: int, col: int) -> bool:
        assert 0 <= row < len(self)
        assert 0 <= col < len(self[row])

        frm = self[row][col]
        if col + 1 < len(self[row]):
            to = self[row][col + 1]
            return frm in (
                Direction.HORIZONTAL,
                Direction.CURVE_RIGHT_UP,
                Direction.CURVE_RIGHT_DOWN,
                Direction.STARTING,
            ) and to in (
                Direction.HORIZONTAL,
                Direction.CURVE_LEFT_UP,
                Direction.CURVE_LEFT_DOWN,
                Direction.STARTING,
            )
        return False

    def can_go_up(self, row: int, col: int) -> bool:
        assert 0 <= row < len(self)
        assert 0 <= col < len(self[row])

        frm = self[row][col]
        if row - 1 >= 0:
            to = self[row - 1][col]
            return frm in (
                Direction.VERTICAL,
                Direction.CURVE_RIGHT_DOWN,
                Direction.CURVE_LEFT_DOWN,
                Direction.STARTING,
            ) and to in (
                Direction.VERTICAL,
                Direction.CURVE_RIGHT_UP,
                Direction.CURVE_LEFT_UP,
                Direction.STARTING,
            )
        return False

    def can_go_down(self, row: int, col: int) -> bool:
        assert 0 <= row < len(self)
        assert 0 <= col < len(self[row])

        frm = self[row][col]
        if row + 1 < len(self):
            to = self[row + 1][col]
            return frm in (
                Direction.VERTICAL,
                Direction.CURVE_RIGHT_UP,
                Direction.CURVE_LEFT_UP,
                Direction.STARTING,
            ) and to in (
                Direction.VERTICAL,
                Direction.CURVE_RIGHT_DOWN,
                Direction.CURVE_LEFT_DOWN,
                Direction.STARTING,
            )
        return False

    def can_move(
        self,
        frm: Direction,
        to: Direction,
        side: Literal["up"] | Literal["down"] | Literal["left"] | Literal["right"],
        row: int,
        col: int,
    ) -> bool:
        assert side in ("up", "down", "left", "right")
        assert 0 <= row < len(self)
        assert 0 <= col < len(self[row])

        if Direction.GROUND in (frm, to):
            return False

        match frm:
            case Direction.STARTING:
                if side == "up" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_UP,
                    Direction.CURVE_LEFT_UP,
                ):
                    return True
                if side == "down" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.CURVE_LEFT_DOWN,
                ):
                    return True
                if side == "left" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.CURVE_RIGHT_UP,
                ):
                    return True
                if side == "right" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_LEFT_DOWN,
                    Direction.CURVE_LEFT_UP,
                ):
                    return True
            case Direction.VERTICAL:
                if side == "up" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_UP,
                    Direction.CURVE_LEFT_UP,
                    Direction.STARTING,
                ):
                    return True
                if side == "down" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.CURVE_LEFT_DOWN,
                    Direction.STARTING,
                ):
                    return True
            case Direction.HORIZONTAL:
                if side == "left" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_RIGHT_UP,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.STARTING,
                ):
                    return True
                if side == "right" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_LEFT_UP,
                    Direction.CURVE_LEFT_DOWN,
                    Direction.STARTING,
                ):
                    return True
            case Direction.CURVE_RIGHT_DOWN:
                if side == "up" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_UP,
                    Direction.CURVE_LEFT_UP,
                    Direction.STARTING,
                ):
                    return True
                if side == "right" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_LEFT_DOWN,
                    Direction.CURVE_LEFT_UP,
                    Direction.STARTING,
                ):
                    return True
            case Direction.CURVE_LEFT_DOWN:
                if side == "up" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_UP,
                    Direction.CURVE_LEFT_UP,
                    Direction.STARTING,
                ):
                    return True
                if side == "left" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.CURVE_RIGHT_UP,
                    Direction.STARTING,
                ):
                    return True
            case Direction.CURVE_RIGHT_UP:
                if side == "down" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.CURVE_LEFT_DOWN,
                    Direction.STARTING,
                ):
                    return True
                if side == "right" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_LEFT_DOWN,
                    Direction.CURVE_LEFT_UP,
                    Direction.STARTING,
                ):
                    return True
            case Direction.CURVE_LEFT_UP:
                if side == "down" and to in (
                    Direction.VERTICAL,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.CURVE_LEFT_DOWN,
                    Direction.STARTING,
                ):
                    return True
                if side == "left" and to in (
                    Direction.HORIZONTAL,
                    Direction.CURVE_RIGHT_DOWN,
                    Direction.CURVE_RIGHT_UP,
                    Direction.STARTING,
                ):
                    return True
        return False

    def possible_moves(self, row: int, col: int) -> list[tuple[int, int]]:
        assert 0 <= row < len(self)
        assert 0 <= col < len(self[row])
        assert self[row][col] != Direction.GROUND

        sources = []
        if row > 0 and self.can_move(
            self[row][col], self[row - 1][col], "up", row - 1, col
        ):
            sources.append((row - 1, col))
        if row < len(self) - 1 and self.can_move(
            self[row][col], self[row + 1][col], "down", row + 1, col
        ):
            sources.append((row + 1, col))
        if col > 0 and self.can_move(
            self[row][col], self[row][col - 1], "left", row, col - 1
        ):
            sources.append((row, col - 1))
        if col < len(self[row]) - 1 and self.can_move(
            self[row][col], self[row][col + 1], "right", row, col + 1
        ):
            sources.append((row, col + 1))
        return sources

    def __str__(self):
        return "\n".join("".join(char.value for char in row) for row in self)

    def find_start_position(self) -> tuple[int, int]:
        for row_index, row in enumerate(self):
            for col_index, char in enumerate(row):
                if char == Direction.STARTING:
                    return row_index, col_index
        raise ValueError("No starting position found")

    def print_dists(self, dists: dict[tuple[int, int], int]):
        max_value = max(dists.values())
        width = len(str(max_value)) + 1
        for row_index, row in enumerate(self):
            print(
                "".join(
                    f"{dists[(row_index, col_index)]:{width}d}"
                    if dists[(row_index, col_index)] != -1
                    else "-" * width
                    for col_index, char in enumerate(row)
                )
            )

    def trace_loop(self, dists: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
        sr, sc = self.find_start_position()
        q = [(sr, sc)]
        visited = set()
        farthest_dist = max(dists.values())
        farthest_dist_reached = False
        pred: dict[tuple[int, int], tuple[int, int]] = defaultdict(lambda: None)  # type: ignore
        while q:
            row, col = q.pop()
            # if self[row][col] == Direction.STARTING and (row, col) in visited:
            #     break
            visited.add((row, col))
            if dists[(row, col)] == farthest_dist:
                farthest_dist_reached = True
            for next_r, next_c in self.possible_moves(row, col):
                if (
                    farthest_dist_reached
                    and dists[(next_r, next_c)] - dists[(row, col)] == -1
                    or not farthest_dist_reached
                    and dists[(next_r, next_c)] - dists[(row, col)] == 1
                ):
                    if (next_r, next_c) in visited and self[next_r][
                        next_c
                    ] != Direction.STARTING:
                        continue
                    pred[(next_r, next_c)] = (row, col)
                    q.append((next_r, next_c))
        loop = []
        current = (sr, sc)
        visited = set()
        while current not in visited:
            visited.add(current)
            loop.append(current)
            current = pred[current]
        return loop

    def find_shortest_path_length(self) -> dict[tuple[int, int], int]:
        sr, sc = self.find_start_position()
        q = deque([(sr, sc)])
        dists = defaultdict(lambda: -1)
        dists[(sr, sc)] = 0

        def travel(r: int, c: int, distance: int):
            if (r, c) not in dists:
                dists[(r, c)] = distance + 1
                q.append((r, c))

        while q:
            row, col = q.popleft()
            d = dists[(row, col)]
            for next_r, next_c in self.possible_moves(row, col):
                travel(next_r, next_c, d)

        return dists

    def print_loop(self, loop):
        loop_set = set(loop)
        for row_index, row in enumerate(self):
            print(
                "".join(
                    "X"
                    if char == Direction.STARTING
                    else colored(char.value, "green")
                    if (row_index, col_index) in loop_set
                    else char.value
                    for col_index, char in enumerate(row)
                )
            )


def calculate_polygon_area(coordinates: list[tuple[int, int]]) -> float:
    """Shoelace formula"""
    x, y = zip(*coordinates)
    return 0.5 * abs(
        sum(x[i] * y[i - 1] - x[i - 1] * y[i] for i in range(len(coordinates)))
    )


def part1(filename: str) -> int:
    with open(filename) as f:
        grid = Grid.parse_input(f.read())
        dists = grid.find_shortest_path_length()
        return max(dists.values())


def part2(filename: str) -> int:
    with open(filename) as f:
        grid = Grid.parse_input(f.read())
        dists = grid.find_shortest_path_length()
        loop = grid.trace_loop(dists)
        return int(calculate_polygon_area(loop) - 0.5 * len(loop) + 1)


day10 = AOCChallenge(10, part1, part2)
__all__ = [day10]
