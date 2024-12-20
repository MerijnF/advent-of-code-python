from collections import Counter
import heapq
from pprint import pprint
from typing import Generator
from utils.grid import Grid
from utils.load import load_as_line_characters

START = "S"
END = "E"
WALL = "#"
EMPTY = "."

MAX_CHEAT_DIST = 20


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
            # cant start in wall
            continue
        # input("Press enter to continue")
        start_value = dist_from_start.get(x, y)
        for end_x, end_y, end_val in grid.iterate():
            if end_val not in [START, END, EMPTY]:
                # cant end up in wall
                # print("Wall: ", x, y, end_x, end_y)
                continue
            dist = abs(x - end_x) + abs(y - end_y)
            if dist > MAX_CHEAT_DIST:
                # too far
                # print("Too far: ", x, y, end_x, end_y, dist)
                continue

            end_value = dist_from_start.get(end_x, end_y)
            if start_value > end_value:
                # ended up closer to start
                # print("Ended up closer: ", x, y, end_x, end_y)
                continue
            save = end_value - (start_value + dist)
            if save < min_save:
                # print("Not enough saved: ", x, y, end_x, end_y)
                # not enough saved
                continue

            cheats[save] += 1
            solution += 1

    pprint(cheats)
    print("Solution: ", solution)


def possible_cheats(
    grid: Grid[str], pos: tuple[int, int]
) -> Generator[tuple[tuple[int, int], int]]:
    visited: set[tuple[int, int]] = set()
    to_visit: list[tuple[tuple[int, int], int]] = []
    heapq.heapify(to_visit)

    heapq.heappush(to_visit, (pos, 0))

    while to_visit:
        next_pos, dist = heapq.heappop(to_visit)
        if next_pos in visited:
            continue
        visited.add(next_pos)
        if grid.get(*next_pos) in [EMPTY, END]:
            print("Found: ", next_pos, dist)
            yield (next_pos, dist)

        next_dist = dist + 1
        if next_dist > MAX_CHEAT_DIST:
            continue
        neighbors = grid.get_neighbors(*next_pos)
        for neighbor in neighbors:
            heapq.heappush(to_visit, (neighbor, dist + 1))


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
