from typing import Literal, Dict, cast
from utils.grid import Grid
from utils.load import load_as_parts_of_line_characters

BOT = "@"
CRATE = "O"
CRATE_LEFT = "["
CRATE_RIGHT = "]"
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

    converted_grid: list[list[str]] = []

    for row in puzzle_input[0]:
        new_row: list[str] = []
        for char in row:
            if char == CRATE:
                new_row.append(CRATE_LEFT)
                new_row.append(CRATE_RIGHT)
            elif char == WALL:
                new_row.append(WALL)
                new_row.append(WALL)
            elif char == EMPTY:
                new_row.append(EMPTY)
                new_row.append(EMPTY)
            elif char == BOT:
                new_row.append(BOT)
                new_row.append(EMPTY)
        converted_grid.append(new_row)
    grid = Grid(converted_grid)

    bot = grid.find_first(BOT)

    if bot is None:
        raise ValueError("bot not found")

    for row in puzzle_input[1]:
        for instruction in row:
            _, bot = try_move(grid, bot, cast(Direction, instruction))

    grid.print()

    solution = 0

    for x, y in grid.find(CRATE_LEFT):
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
    if next_value in {CRATE_LEFT, CRATE_RIGHT}:
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

    if direction in {"<", ">"}:
        return try_move_crate_horizontal(grid, crate, direction)
    else:
        return try_move_crate_vertical(grid, crate, direction)


def try_move_crate_horizontal(
    grid: Grid, crate: tuple[int, int], direction: Direction
) -> bool:
    left, right = get_crate_positions(grid, crate)

    if direction == "<":
        next_pos = get_next_position(left, direction)
    else:
        next_pos = get_next_position(right, direction)
    next_value = grid.get(*next_pos)

    if next_value == WALL:
        return False

    if next_value == BOT:
        return False

    if next_value == EMPTY:
        if direction == "<":
            grid.set(*next_pos, CRATE_LEFT)
            grid.set(*left, CRATE_RIGHT)
            grid.set(*right, EMPTY)
        else:
            grid.set(*next_pos, CRATE_RIGHT)
            grid.set(*right, CRATE_LEFT)
            grid.set(*left, EMPTY)
        return True

    if next_value in (CRATE_LEFT, CRATE_RIGHT):
        moved_crate = try_move_crate(grid, next_pos, direction)
        if moved_crate:
            if direction == "<":
                grid.set(*next_pos, CRATE_LEFT)
                grid.set(*left, CRATE_RIGHT)
                grid.set(*right, EMPTY)
            else:
                grid.set(*next_pos, CRATE_RIGHT)
                grid.set(*right, CRATE_LEFT)
                grid.set(*left, EMPTY)
            return True
        return False
    return False


def try_move_crate_vertical(
    grid: Grid, crate: tuple[int, int], direction: Direction
) -> bool:
    can_move = can_move_crate_vertical(grid, crate, direction)
    if can_move:
        left, right = get_crate_positions(grid, crate)
        next_pos_left = get_next_position(left, direction)
        next_value_left = grid.get(*next_pos_left)
        if next_value_left in {CRATE_LEFT, CRATE_RIGHT}:
            try_move_crate_vertical(grid, next_pos_left, direction)

        next_pos_right = get_next_position(right, direction)
        next_value_left = grid.get(*next_pos_right)
        if next_value_left in {CRATE_LEFT, CRATE_RIGHT}:
            try_move_crate_vertical(grid, next_pos_right, direction)

        grid.set(*next_pos_left, CRATE_LEFT)
        grid.set(*left, EMPTY)

        grid.set(*next_pos_right, CRATE_RIGHT)
        grid.set(*right, EMPTY)

        return True
    else:
        return False


def can_move_crate_vertical(
    grid: Grid, crate: tuple[int, int], direction: Direction
) -> bool:
    left, right = get_crate_positions(grid, crate)
    can_left_move = False

    next_pos_left = get_next_position(left, direction)
    next_value_left = grid.get(*next_pos_left)
    if next_value_left == EMPTY:
        can_left_move = True
    if next_value_left in {CRATE_LEFT, CRATE_RIGHT}:
        can_left_move = can_move_crate_vertical(grid, next_pos_left, direction)

    can_right_move = False

    next_pos_right = get_next_position(right, direction)
    next_value_right = grid.get(*next_pos_right)
    if next_value_right == EMPTY:
        can_right_move = True
    if next_value_right in {CRATE_LEFT, CRATE_RIGHT}:
        can_right_move = can_move_crate_vertical(grid, next_pos_right, direction)

    return can_left_move and can_right_move


def get_crate_positions(
    grid: Grid, crate: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    crate_part = grid.get(*crate)

    if crate_part == CRATE_LEFT:
        left_pos = crate
        right_pos = (crate[0] + 1, crate[1])
    else:
        left_pos = (crate[0] - 1, crate[1])
        right_pos = crate

    return left_pos, right_pos


def get_next_position(
    position: tuple[int, int], direction: Direction
) -> tuple[int, int]:
    direction_vector = DIRECTIONS_MAP[direction]
    return (position[0] + direction_vector[0], position[1] + direction_vector[1])
