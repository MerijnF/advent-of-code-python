from collections import Counter
from utils.grid import Grid, GridPathfinder
from utils.load import load_as_line_characters

START = "S"
END = "E"
WALL = "#"
EMPTY = "."

CHEAT_STEPS = [(-2, 0), (2, 0), (0, -2), (0, 2)]


def solve(year: int, day: int, test: bool = False) -> None:
    puzzle_input = load_as_line_characters(year, day, test)

    min_save = 50 if test else 100
    grid = Grid(puzzle_input)
    dist_from_start = Grid(
        [[-1 for _ in range(grid.width)] for _ in range(grid.height)]
    )

    pos = grid.find_first(START)
    if pos is None:
        raise ValueError("start not found")

    dist = 0
    dist_from_start.set(*pos, dist)
    dist += 1
    prev_pos = None

    value = grid.get(*pos)

    while value != END:
        next_pos = find_next_pos(grid, pos, prev_pos)
        dist_from_start.set(*next_pos, dist)
        dist += 1
        prev_pos = pos
        pos = next_pos
        value = grid.get(*pos)

    grid.print()
    dist_from_start.print(5)

    cheats: Counter[int] = Counter()

    solution = 0
    for x, y, val in grid.iterate():
        if val not in [START, END, EMPTY]:
            continue
        start_dist = dist_from_start.get(x, y)
        for dx, dy in CHEAT_STEPS:
            end_pos = (x + dx, y + dy)
            if grid.in_bounds(*end_pos) and grid.get(*end_pos) in (EMPTY, END):
                end_dist = dist_from_start.get(*end_pos)
                if start_dist < end_dist:
                    saving = end_dist - (start_dist + 2)
                    if saving == 0:
                        continue
                    cheats[saving] += 1
                    if saving >= min_save:
                        solution += 1
    print(cheats)
    print("Solution: ", solution)


def find_next_pos(
    grid: Grid, pos: tuple[int, int], prev_pos: tuple[int, int] | None
) -> tuple[int, int]:
    neighbors = grid.get_neighbors(*pos)
    for neighbor in neighbors:
        if neighbor == prev_pos:
            continue
        if grid.get(*neighbor) in [EMPTY, END]:
            return neighbor
    return (-1, -1)
