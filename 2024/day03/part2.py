from utils.load import load_as_string
import re


def solve(year: int, day: int):
    input = load_as_string(year, day)
    found = re.findall(r"(mul)\(([0-9]+),([0-9]+)\)|(do)\(\)|(don't)\(\)", input)

    solution: int = 0

    enabled = True
    for f in found:
        if f[0] == "mul":
            a, b = f[1], f[2]
            if enabled:
                solution += int(a) * int(b)
        elif f[3] == "do":
            enabled = True
        elif f[4] == "don't":
            enabled = False

    print(f"solution: {solution}")
