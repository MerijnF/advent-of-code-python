from utils.grid import Grid
from utils.load import load_as_line_characters_as_integers


def solve(year: int, day: int, test: bool = False):
    test_input = load_as_line_characters_as_integers(year, day, test)

    grid = Grid(test_input)
    grid.print()
    solution = 0
    for x, y, val in grid.iterate():
        if val == 0:
            result = count_paths(grid, (x, y))
            print(x, y, result)
            solution += result

    print(f"solution: {solution}")


def count_paths(
    grid: Grid,
    pos: tuple[int, int],
    prev_height: int = -1,
) -> int:
    if not grid.in_bounds(*pos):
        return 0

    height = grid.get(*pos)

    if height == prev_height:
        # going backwards
        return 0
    if height != prev_height + 1:
        # too much incline
        return 0
    if height == 9:
        return 1

    result = 0

    up = (pos[0], pos[1] - 1)
    result += count_paths(grid, up, height)
    down = (pos[0], pos[1] + 1)
    result += count_paths(grid, down, height)
    left = (pos[0] - 1, pos[1])
    result += count_paths(grid, left, height)
    right = (pos[0] + 1, pos[1])
    result += count_paths(grid, right, height)
    return result
