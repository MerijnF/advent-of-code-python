from collections import Counter


def solve(year: int, day: int):
    # read input
    with open(f"input/{year}/day{day:02}/input.txt", "r") as input_file:
        input: list[str] = input_file.readlines()
    # parse input
    left: list[int] = []
    right: list[int] = []
    for line in input:
        split = line.split()
        left.append(int(split[0]))
        right.append(int(split[1]))

    left.sort()
    counted = Counter(right)

    solution: int = 0
    for i, a in enumerate(left):
        if a in counted:
            solution += a * counted[a]

    print(f"solution: {solution}")
