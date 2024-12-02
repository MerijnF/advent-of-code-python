from utils.load import load_as_lines
from itertools import pairwise


def difference(a: int, b: int):
    return abs(a - b)


def solve(year, day):
    input = load_as_lines(year, day)
    solution: int = 0
    for line in input:
        split = map(int, line.split())
        if is_valid(split):
            solution += 1

    print(f"solution: {solution}")


def is_valid(split) -> bool:
    asc: bool = None
    for a, b in pairwise(split):
        step_asc: bool = None
        if a > b:
            step_asc = False
        else:
            step_asc = True

        if asc is None:
            asc = step_asc

        if step_asc != asc:
            return False

        dif = difference(a, b)
        if dif > 3 or dif < 1:
            return False
    return True
