from dataclasses import dataclass
import re
from utils.grid import Grid
from utils.load import load_as_lines

PATTERN = r"p=([-\d]+),([-\d]+) v=([-\d]+),([-\d]+)"


@dataclass
class Bot:
    pos: tuple[int, int]
    vel: tuple[int, int]


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_lines(year, day, test)

    width = 11 if test else 101
    height = 7 if test else 103

    bots: list[Bot] = []

    for line in test_input:
        match = re.match(PATTERN, line)
        if match is None:
            print(f"no match for: {line}")
            continue

        bots.append(
            Bot(
                (int(match.group(1)), int(match.group(2))),
                (int(match.group(3)), int(match.group(4))),
            )
        )

    for _ in range(100):
        move_bots(bots, width, height)

    up_right = 0
    up_left = 0
    down_right = 0
    down_left = 0

    grid = bots_to_grid(bots, width, height)
    grid.print()

    half_width = (width - 1) / 2
    half_height = (height - 1) / 2

    print(f"half_width: {half_width}, half_height: {half_height}")

    for bot in bots:

        if bot.pos[0] > half_width and bot.pos[1] < half_height:
            up_right += 1
        if bot.pos[0] < half_width and bot.pos[1] < half_height:
            up_left += 1
        if bot.pos[0] > half_width and bot.pos[1] > half_height:
            down_right += 1
        if bot.pos[0] < half_width and bot.pos[1] > half_height:
            down_left += 1

    solution = up_right * up_left * down_right * down_left

    print(f"solution: {solution}")


def move_bots(bots: list[Bot], width: int, height: int) -> None:
    for bot in bots:
        bot.pos = (bot.pos[0] + bot.vel[0], bot.pos[1] + bot.vel[1])
        while bot.pos[0] > width - 1:
            bot.pos = (bot.pos[0] - width, bot.pos[1])
        while bot.pos[0] < 0:
            bot.pos = (bot.pos[0] + width, bot.pos[1])
        while bot.pos[1] > height - 1:
            bot.pos = (bot.pos[0], bot.pos[1] - height)
        while bot.pos[1] < 0:
            bot.pos = (bot.pos[0], bot.pos[1] + height)


def bots_to_grid(bots: list[Bot], width: int, height: int):
    grid = Grid([[0 for _ in range(width)] for _ in range(height)])

    for bot in bots:
        count = grid.get(*bot.pos)
        count += 1
        grid.set(bot.pos[0], bot.pos[1], count)

    return grid
