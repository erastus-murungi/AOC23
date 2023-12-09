from utils import AOCChallenge, extract_numbers


def recurse(history: list[int] | tuple[int], reverse: bool = False) -> int:
    if all(num == 0 for num in history):
        return 0
    else:
        val = recurse(
            [b - a if reverse else a - b for a, b in zip(history[1:], history)], reverse
        )
        return history[0 if reverse else -1] + val


def process_data(filename: str, reverse: bool = False) -> int:
    with open(filename) as f:
        data = f.read().strip()
        lines = list(map(extract_numbers, data.splitlines()))
        return sum(map(lambda x: recurse(x, reverse), lines))


def part1(filename: str) -> int:
    return process_data(filename)


def part2(filename: str) -> int:
    return process_data(filename, reverse=True)


day9 = AOCChallenge(9, part1, part2)
__all__ = [day9]
