# dimensions num_rows, num_cols
def is_symbol(char: str):
    return not char.isdigit() and char != "."


def sum_of_part_numbers_adjacent_to_symbols(
    table: list[str],
    row_index: int,
    col_index: int,
    span: int,
    num_rows: int,
    num_cols: int,
) -> bool:
    for index, symbol in enumerate(
        table[row_index][col_index : col_index + span], col_index
    ):
        # grab the current row
        row = table[row_index]
        # check left, right
        if index > 0 and is_symbol(row[index - 1]):
            return True
        if index < num_cols - 1 and is_symbol(row[index + 1]):
            return True

        # check up, down
        if row_index > 0 and is_symbol(table[row_index - 1][index]):
            return True
        if row_index < num_rows - 1 and is_symbol(table[row_index + 1][index]):
            return True

        # check diagonals
        if row_index > 0 and index > 0 and is_symbol(table[row_index - 1][index - 1]):
            return True
        if (
            row_index > 0
            and index < num_cols - 1
            and is_symbol(table[row_index - 1][index + 1])
        ):
            return True
        if (
            row_index < num_rows - 1
            and index > 0
            and is_symbol(table[row_index + 1][index - 1])
        ):
            return True
        if (
            row_index < num_rows - 1
            and index < num_cols - 1
            and is_symbol(table[row_index + 1][index + 1])
        ):
            return True
    return False


def parse_number(s: str) -> str:
    digits = []
    for char in s:
        if char.isdigit():
            digits.append(char)
        else:
            return "".join(digits)
    return "".join(digits)


def sum_nums_adjacent_to_symbol(s: str):
    s = s.strip()
    sum_nums = 0
    lines = s.splitlines()
    num_rows = len(lines)
    num_cols = len(lines[0])
    for row, line in enumerate(lines):
        col = 0
        while col < len(line):
            char = line[col]
            if char.isdigit():
                number = parse_number(line[col:])
                span = len(number)
                if sum_of_part_numbers_adjacent_to_symbols(
                    lines, row, col, span, num_rows, num_cols
                ):
                    sum_nums += int(number)
                col = col + span
            else:
                col += 1
    return sum_nums


if __name__ == "__main__":
    with open("input/day3.txt") as f:
        print(sum_nums_adjacent_to_symbol(f.read()))
