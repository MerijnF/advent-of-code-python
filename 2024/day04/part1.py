from utils.load import load_as_line_characters

SEARCH_CHARS: list[str] = ["X", "M", "A", "S"]


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_line_characters(year, day, test)

    solution = 0
    for x, line in enumerate(test_input):
        for y, char in enumerate(line):
            if char == SEARCH_CHARS[0]:
                solution += count_checks(x, y, test_input)

    print(f"solution: {solution}")


def check_up(x: int, y: int, grid: list[list[str]]) -> bool:
    s_x = x
    for i, char in enumerate(SEARCH_CHARS):
        s_y = y - i
        if s_y < 0:
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def check_down(x: int, y: int, grid: list[list[str]]) -> bool:
    s_x = x
    for i, char in enumerate(SEARCH_CHARS):
        s_y = y + i
        if s_y >= len(grid):
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def check_left(x: int, y: int, grid: list[list[str]]) -> bool:
    s_y = y
    for i, char in enumerate(SEARCH_CHARS):
        s_x = x - i
        if s_x < 0:
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def check_right(x: int, y: int, grid: list[list[str]]) -> bool:
    s_y = y
    for i, char in enumerate(SEARCH_CHARS):
        s_x = x + i
        if s_x >= len(grid):
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def check_diagonal_up_right(x: int, y: int, grid: list[list[str]]) -> bool:
    for i, char in enumerate(SEARCH_CHARS):
        s_x = x + i
        s_y = y - i
        if s_x >= len(grid) or s_y < 0:
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def check_diagonal_up_left(x: int, y: int, grid: list[list[str]]) -> bool:
    for i, char in enumerate(SEARCH_CHARS):
        s_x = x - i
        s_y = y - i
        if s_x < 0 or s_y < 0:
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def check_diagonal_down_right(x: int, y: int, grid: list[list[str]]) -> bool:
    for i, char in enumerate(SEARCH_CHARS):
        s_x = x + i
        s_y = y + i
        if s_x >= len(grid) or s_y >= len(grid):
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def check_diagonal_down_left(x: int, y: int, grid: list[list[str]]) -> bool:
    for i, char in enumerate(SEARCH_CHARS):
        s_x = x - i
        s_y = y + i
        if s_x < 0 or s_y >= len(grid):
            return False
        if grid[s_x][s_y] != char:
            return False
    return True


def count_checks(x: int, y: int, grid: list[list[str]]) -> int:
    count = 0
    if check_up(x, y, grid):
        count += 1
    if check_down(x, y, grid):
        count += 1
    if check_left(x, y, grid):
        count += 1
    if check_right(x, y, grid):
        count += 1
    if check_diagonal_up_right(x, y, grid):
        count += 1
    if check_diagonal_up_left(x, y, grid):
        count += 1
    if check_diagonal_down_right(x, y, grid):
        count += 1
    if check_diagonal_down_left(x, y, grid):
        count += 1
    return count
