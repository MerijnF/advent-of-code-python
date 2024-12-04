from utils.load import load_as_lines
from itertools import pairwise


def difference(a: int, b: int):
    return abs(a - b)


def solve(year, day, test=False):
    input = load_as_lines(year, day, test)
    solution: int = 0
    for line in input:
        split = list(map(int, line.split()))
        if is_valid_dampened(split):
            solution += 1
            # print("true", split)
        else:
            print("false", split)

    print(f"solution: {solution}")


def is_valid_dampened(report: list[int]) -> bool:
    if is_valid(report):
        return True
    for index_to_remove in range(len(report)):
        new_report = report.copy()
        new_report.pop(index_to_remove)
        # print("dampened", new_report)
        if is_valid(new_report):
            return True
    return False


def is_valid(report) -> bool:
    asc: bool = None
    for a, b in pairwise(report):
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
