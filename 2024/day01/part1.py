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
    right.sort()

    solution: int = 0
    for i, a in enumerate(left):
        b = right[i]
        if a > b:
            solution += a - b
        else:
            solution += b - a

    print(f"solution: {solution}")
