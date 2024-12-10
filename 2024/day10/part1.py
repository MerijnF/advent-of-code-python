from utils.grid import Grid
from utils.load import load_as_line_characters_as_integers


def solve(year: int, day: int, test: bool = False):
    test_input = load_as_line_characters_as_integers(year, day, test)

    grid = Grid(test_input)
    grid.print()
    solution = 0
    for x, y, val in grid.iterate():
        if val == 0:
            result = find_ends(grid, (x, y))
            print(x, y, list(result))
            solution += len(result)

    print(f"solution: {solution}")


def find_ends(
    grid: Grid,
    pos: tuple[int, int],
    prev_height: int = -1,
) -> set[tuple[int, int]]:
    if not grid.in_bounds(*pos):
        return set()

    height = grid.get(*pos)

    if height == prev_height:
        # going backwards
        return set()
    if height != prev_height + 1:
        # too much incline
        return set()
    if height == 9:
        return set([pos])

    result: set[tuple[int, int]] = set()

    up = (pos[0], pos[1] - 1)
    result = result.union(find_ends(grid, up, height))
    down = (pos[0], pos[1] + 1)
    result = result.union(find_ends(grid, down, height))
    left = (pos[0] - 1, pos[1])
    result = result.union(find_ends(grid, left, height))
    right = (pos[0] + 1, pos[1])
    result = result.union(find_ends(grid, right, height))
    return result
