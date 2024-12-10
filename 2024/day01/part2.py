from collections import Counter

from utils.load import load_as_lines


def solve(year: int, day: int, test: bool = False) -> None:
    # read input
    test_input = load_as_lines(year, day, test)
    # parse input
    left: list[int] = []
    right: list[int] = []
    for line in test_input:
        split = line.split()
        left.append(int(split[0]))
        right.append(int(split[1]))

    left.sort()
    counted = Counter(right)

    solution: int = 0
    for _, a in enumerate(left):
        if a in counted:
            solution += a * counted[a]

    print(f"solution: {solution}")
