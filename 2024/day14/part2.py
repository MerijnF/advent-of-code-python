from collections import Counter
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

    tree = False
    count = 0
    while not tree:
        move_bots(bots, width, height)
        count += 1
        if not has_overlap(bots):
            grid = bots_to_grid(bots, width, height)
            grid.print()
            is_tree = input("tree? (y/n):")
            if is_tree == "y":
                tree = True

    print(f"solution: {count}")


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


def has_overlap(bots: list[Bot]) -> bool:
    counts = Counter([bot.pos for bot in bots])

    for count in counts.values():
        if count > 1:
            return True

    return False


def bots_to_grid(bots: list[Bot], width: int, height: int):
    grid = Grid([["." for _ in range(width)] for _ in range(height)])

    for bot in bots:
        grid.set(bot.pos[0], bot.pos[1], "#")

    return grid
