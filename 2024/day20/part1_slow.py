from utils.grid import Grid, GridPathfinder
from utils.load import load_as_line_characters

START = "S"
END = "E"
WALL = "#"
EMPTY = "."


def solve(year: int, day: int, test: bool = False) -> None:
    puzzle_input = load_as_line_characters(year, day, test)

    min_save = 50 if test else 100
    grid = Grid(puzzle_input)
    pathfinder = GridPathfinder(grid, lambda x: x in [EMPTY, START, END])
    pathfinder.find_start("S")
    pathfinder.find_end("E")

    baseline = pathfinder.find_shortest_dist()
    if baseline is None:
        raise ValueError("No path found")
    print("Baseline: ", baseline)
    cheats: dict[int, list[tuple[int, int]]] = {}
    solution = 0
    for x, y in grid.find(WALL):

        if grid.on_edge(x, y):
            continue

        neighbors = grid.get_neighbor_values(x, y)

        if len([x for x in neighbors if x in [EMPTY, START, END]]) >= 2:
            new_grid = grid.deepcopy()
            new_grid.set(x, y, EMPTY)
            new_pathfinder = GridPathfinder(
                new_grid,
                lambda x: x in [EMPTY, START, END],
                pathfinder.start,
                pathfinder.end,
            )
            dist = new_pathfinder.find_shortest_dist()
            if dist is None:
                continue
            saving = baseline - dist
            if saving not in cheats:
                cheats[saving] = []
            cheats[saving].append((x, y))
            if saving >= min_save:
                solution += 1

    for k, v in sorted(cheats.items()):
        print(k, len(v))
    print("Solution: ", solution)
