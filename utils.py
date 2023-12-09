from dataclasses import dataclass
from typing import Callable
import re


@dataclass
class AOCChallenge[ReturnType]:
    day: int
    part1: Callable[[str], ReturnType]
    part2: Callable[[str], ReturnType]


def extract_numbers(s: str, syntax=re.compile(r"-?\d+")) -> tuple[int]:
    return tuple(map(int, syntax.findall(s)))
