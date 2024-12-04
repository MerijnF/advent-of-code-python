from utils.load import load_as_line_characters

START_CHAR: chr = "A"
DIR_A_CHARS: list[chr] = ["M"]
DIR_B_CHARS: list[chr] = ["S"]


def solve(year: int, day: int, test: bool = False):
    input = load_as_line_characters(year, day, test)

    solution = 0
    for x, line in enumerate(input):
        for y, char in enumerate(line):
            if char == START_CHAR:
                if check_diagonal_cross(x, y, input):
                    solution += 1

    print(f"solution: {solution}")


def check_diagonal_cross(x: int, y: int, grid: list[list[chr]]) -> bool:
    if check_left_down_up_right(x, y, grid):
        if check_right_down_up_left(x, y, grid):
            return True
    return False


def check_left_down_up_right(x: int, y: int, grid: list[list[chr]]) -> bool:
    if check_diagonal_down_left(x, y, grid, DIR_A_CHARS):
        if check_diagonal_up_right(x, y, grid, DIR_B_CHARS):
            return True
    elif check_diagonal_up_right(x, y, grid, DIR_A_CHARS):
        if check_diagonal_down_left(x, y, grid, DIR_B_CHARS):
            return True
    return False


def check_right_down_up_left(x: int, y: int, grid: list[list[chr]]) -> bool:
    if check_diagonal_down_right(x, y, grid, DIR_A_CHARS):
        if check_diagonal_up_left(x, y, grid, DIR_B_CHARS):
            return True
    elif check_diagonal_up_left(x, y, grid, DIR_A_CHARS):
        if check_diagonal_down_right(x, y, grid, DIR_B_CHARS):
            return True
    return False


def check_diagonal_up_right(
    x: int, y: int, grid: list[list[chr]], chars: list[chr]
) -> bool:
    for i in range(len(chars)):
        s_x = x + i + 1
        s_y = y - i - 1
        if s_x >= len(grid) or s_y < 0:
            return False
        if grid[s_x][s_y] != chars[i]:
            return False
    return True


def check_diagonal_up_left(
    x: int, y: int, grid: list[list[chr]], chars: list[chr]
) -> bool:
    for i in range(len(chars)):
        s_x = x - i - 1
        s_y = y - i - 1
        if s_x < 0 or s_y < 0:
            return False
        if grid[s_x][s_y] != chars[i]:
            return False
    return True


def check_diagonal_down_right(
    x: int, y: int, grid: list[list[chr]], chars: list[chr]
) -> bool:
    for i in range(len(chars)):
        s_x = x + i + 1
        s_y = y + i + 1
        if s_x >= len(grid) or s_y >= len(grid):
            return False
        if grid[s_x][s_y] != chars[i]:
            return False
    return True


def check_diagonal_down_left(
    x: int, y: int, grid: list[list[chr]], chars: list[chr]
) -> bool:
    for i in range(len(chars)):
        s_x = x - i - 1
        s_y = y + i + 1
        if s_x < 0 or s_y >= len(grid):
            return False
        if grid[s_x][s_y] != chars[i]:
            return False
    return True
