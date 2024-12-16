import heapq
from typing import Literal
from utils.grid import Grid
from utils.load import load_as_line_characters

Direction = Literal["N", "E", "S", "W"]

START = "S"
END = "E"
WALL = "#"
EMPTY = "."

DIRECTION_VECTORS: dict[Direction, tuple[int, int]] = {
    "N": (0, -1),
    "E": (1, 0),
    "S": (0, 1),
    "W": (-1, 0),
}

START_DIRECTION: Direction = "E"
MOVE_COST = 1
TURN_COST = 1000


def solve(year: int, day: int, test: bool = False) -> None:
    puzzle_input = load_as_line_characters(year, day, test)

    grid = Grid(puzzle_input)
    end = grid.find_first(END)

    if end is None:
        raise ValueError("end not found")

    costs = cheapest_per_space(grid)

    cheapest = min(v for k, v in costs.items() if k[0] == end)

    print("Solution: ", cheapest)


def cheapest_per_space(
    grid: Grid[str],
) -> dict[tuple[tuple[int, int], Direction], int]:
    to_visit: list[tuple[int, tuple[int, int], Direction]] = []
    visited: dict[tuple[tuple[int, int], Direction], int] = {}

    start_pos = grid.find_first(START)

    if start_pos is None:
        return visited

    visited[(start_pos, START_DIRECTION)] = 0

    heapq.heapify(to_visit)
    heapq.heappush(to_visit, (0, start_pos, START_DIRECTION))

    while to_visit:
        cost, pos, direction = heapq.heappop(to_visit)

        if (pos, direction) in visited and visited[(pos, direction)] < cost:
            continue

        # try forward
        next_pos = get_next_pos(pos, direction)

        if is_valid_space(grid, next_pos):
            new_cost = cost + MOVE_COST
            if (next_pos, direction) not in visited or visited[
                (next_pos, direction)
            ] > new_cost:
                visited[(next_pos, direction)] = new_cost
                heapq.heappush(to_visit, (new_cost, next_pos, direction))

        for turn in get_90_degree_turns(direction):
            new_cost = cost + TURN_COST
            if (pos, turn) not in visited or visited[(pos, turn)] > new_cost:
                visited[(pos, turn)] = new_cost
                heapq.heappush(to_visit, (new_cost, pos, turn))

    return visited


def is_valid_space(grid: Grid[str], pos: tuple[int, int]) -> bool:
    value = grid.get(*pos)
    return value in {EMPTY, END}


def get_next_pos(position: tuple[int, int], direction: Direction) -> tuple[int, int]:
    vector = DIRECTION_VECTORS[direction]
    return (position[0] + vector[0], position[1] + vector[1])


def get_90_degree_turns(direction: Direction) -> list[Direction]:
    match direction:
        case "N":
            return ["E", "W"]
        case "E":
            return ["S", "N"]
        case "S":
            return ["W", "E"]
        case "W":
            return ["N", "S"]
