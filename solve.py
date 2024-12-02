from importlib import import_module
from datetime import datetime
import argparse


def solve(year: int, day: int, part: int):
    module = import_module(f"{year}.day{day:02}.part{part}")
    module.solve(year, day)
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("day")
    parser.add_argument("part")
    parser.add_argument("-y", "--year")

    args = parser.parse_args()

    if args.year != None:
        year = int(args.year)
    else:
        year = datetime.now().year

    day = int(args.day)
    part = int(args.part)

    solve(year, day, part)
