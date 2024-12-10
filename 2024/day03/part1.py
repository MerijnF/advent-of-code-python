import re
from utils.load import load_as_string


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_string(year, day, test)
    found = re.findall(r"mul\(([0-9]+),([0-9]+)\)", test_input)
    solution: int = 0

    for f in found:
        a, b = f
        solution += int(a) * int(b)

    print(f"solution: {solution}")
