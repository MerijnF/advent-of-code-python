from utils.load import load_as_string
import re


def solve(year: int, day: int):
    input = load_as_string(year, day)
    found = re.findall(r"mul\(([0-9]+),([0-9]+)\)", input)
    solution: int = 0

    for f in found:
        a, b = f
        solution += int(a) * int(b)

    print(f"solution: {solution}")
