from dataclasses import dataclass
import re
from utils.load import load_as_parts_of_lines

OFFSET = 10000000000000
PATTERN = r"X[+-=]?(\d+), Y[+-=]?(\d+)"


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_parts_of_lines(year, day, test)

    solution = 0

    for i, machine in enumerate(test_input):
        a = get_xy(machine[0])
        b = get_xy(machine[1])
        prize = get_xy(machine[2])
        prize = (prize[0] + OFFSET, prize[1] + OFFSET)

        print("Machine ", i)
        print("Button A: ", a[0], a[1])
        print("Button B: ", b[0], b[1])
        print("Prize: ", prize[0], prize[1])

        # math time -> linear algebra
        # given solution
        # 80*94 + 40*22 = 8400
        # 80*34 + 40*67 = 5400
        #
        # gives the following 2 formulas
        # a*ax + b*bx = px
        # a*ay + b*by = py
        #
        # matrix
        # | ax bx | a = | px |
        # | ay by | b = | py |
        #
        # cramer's rule to solve for a and b
        # a = det(Ma) / det(M)
        # b = det(Mb) / (det(M)
        #
        # det(M) = ax*by - ay*bx
        # det(Ma) = px*by - py*bx
        # det(Mb) = ax*py - px*ay
        #
        # a = (px*by - py*bx) / (ax*by - ay*bx)
        # b = (ax*py - px*ay) / (ax*by - ay*bx)

        ax = a[0]
        bx = b[0]
        ay = a[1]
        by = b[1]

        px = prize[0]
        py = prize[1]

        a_presses = (px * by - py * bx) / (ax * by - ay * bx)
        b_presses = (ax * py - px * ay) / (ax * by - ay * bx)

        print("a: ", a_presses)
        print("b: ", b_presses)

        if a_presses.is_integer() and b_presses.is_integer():
            solution += int(a_presses) * 3 + int(b_presses)

    print(f"solution: {solution}")


def get_xy(line: str) -> tuple[int, int]:
    match = re.search(PATTERN, line)
    if match is not None:
        x = int(match.group(1))
        y = int(match.group(2))
        return (x, y)
    return (0, 0)
