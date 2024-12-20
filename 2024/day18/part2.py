from utils.grid import Grid, GridPathfinder
from utils.load import load_as_split_lines_as_integers


def solve(year: int, day: int, test: bool = False) -> None:
    bytes_to_drop = 12 if test else 1024
    width = 7 if test else 71
    height = 7 if test else 71

    grid = Grid([["." for _ in range(width)] for _ in range(height)])

    puzzle_input = load_as_split_lines_as_integers(year, day, test, ",")

    for i in range(bytes_to_drop):
        x, y = puzzle_input[i][0], puzzle_input[i][1]
        grid.set(x, y, "#")

    pathfinder = GridPathfinder(
        grid,
        lambda x: x == ".",
        (0, 0),
        (width - 1, height - 1),
    )

    for i in range(bytes_to_drop, len(puzzle_input)):
        x, y = puzzle_input[i][0], puzzle_input[i][1]
        grid.set(x, y, "#")

        dist = pathfinder.find_shortest_dist()
        if dist is None:

            print("Solution: ", x, y)
            break
