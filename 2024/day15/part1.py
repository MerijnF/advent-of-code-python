from typing import Literal, Dict, cast
from utils.grid import Grid
from utils.load import load_as_parts_of_line_characters

BOT = "@"
CRATE = "O"
WALL = "#"
EMPTY = "."

Direction = Literal["<", ">", "^", "v"]
DIRECTIONS_MAP: Dict[Direction, tuple[int, int]] = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def solve(year: int, day: int, test: bool = False) -> None:
    puzzle_input = load_as_parts_of_line_characters(year, day, test)

    grid = Grid(puzzle_input[0])
    bot = grid.find_first(BOT)

    if bot is None:
        raise ValueError("bot not found")

    for row in puzzle_input[1]:
        for instruction in row:
            _, bot = try_move(grid, bot, cast(Direction, instruction))

    grid.print()

    solution = 0

    for x, y in grid.find(CRATE):
        solution += x + (y * 100)

    print(f"solution: {solution}")


def try_move(
    grid: Grid, bot: tuple[int, int], direction: Direction
) -> tuple[bool, tuple[int, int]]:
    next_pos = get_next_position(bot, direction)
    next_value = grid.get(*next_pos)
    if next_value == WALL:
        return False, bot
    if next_value == BOT:
        return False, bot
    if next_value == CRATE:
        moved_crate = try_move_crate(grid, next_pos, direction)
        if moved_crate:
            grid.set(*next_pos, BOT)
            grid.set(*bot, EMPTY)
            return True, next_pos
        return False, bot
    if next_value == EMPTY:
        grid.set(*next_pos, BOT)
        grid.set(*bot, EMPTY)
        return True, next_pos
    return False, bot


def try_move_crate(grid: Grid, crate: tuple[int, int], direction: Direction) -> bool:
    next_pos = get_next_position(crate, direction)
    next_value = grid.get(*next_pos)
    if next_value == WALL:
        return False
    if next_value == BOT:
        return False
    if next_value == CRATE:
        moved_crate = try_move_crate(grid, next_pos, direction)
        if moved_crate:
            grid.set(*next_pos, CRATE)
            grid.set(*crate, EMPTY)
            return True
        return False
    if next_value == EMPTY:
        grid.set(*next_pos, CRATE)
        grid.set(*crate, EMPTY)
        return True
    return False


def get_next_position(
    position: tuple[int, int], direction: Direction
) -> tuple[int, int]:
    direction_vector = DIRECTIONS_MAP[direction]
    return (position[0] + direction_vector[0], position[1] + direction_vector[1])
