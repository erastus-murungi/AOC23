from utils import AOCChallenge, extract_numbers


def recurse_part1(history: list[int]) -> int:
    if all(num == 0 for num in history):
        return 0
    else:
        val = recurse_part1([a - b for a, b in zip(history[1:], history)])
        return history[-1] + val


def recurse_part2(history: list[int]) -> int:
    if all(num == 0 for num in history):
        return 0
    else:
        val = recurse_part2([b - a for a, b in zip(history[1:], history)])
        return history[0] + val


def part1(filename: str) -> int:
    with open(filename) as f:
        data = f.read().strip()
        lines = list(map(extract_numbers, data.splitlines()))
        return sum(map(recurse_part1, lines))


def part2(filename: str) -> int:
    with open(filename) as f:
        data = f.read().strip()
        lines = list(map(extract_numbers, data.splitlines()))
        return sum(map(recurse_part2, lines))


day9 = AOCChallenge(9, part1, part2)
__all__ = [day9]

if __name__ == "__main__":
    print(part1("input/day9.txt"))
