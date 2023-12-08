from dataclasses import dataclass
from typing import Callable


@dataclass
class AOCChallenge[ReturnType]:
    day: int
    part1: Callable[[str], ReturnType]
    part2: Callable[[str], ReturnType]
