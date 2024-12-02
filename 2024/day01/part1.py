from utils.load import load_as_lines


def solve(year: int, day: int):
    # read input
    input = load_as_lines(year, day)
    # parse input
    left: list[int] = []
    right: list[int] = []
    for line in input:
        split = line.split()
        left.append(int(split[0]))
        right.append(int(split[1]))

    left.sort()
    right.sort()

    solution: int = 0
    for i, a in enumerate(left):
        b = right[i]
        if a > b:
            solution += a - b
        else:
            solution += b - a

    print(f"solution: {solution}")
