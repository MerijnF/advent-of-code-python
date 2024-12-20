from functools import cache
from utils.load import load_as_parts_of_lines


def solve(year: int, day: int, test: bool = False) -> None:
    puzzle_input = load_as_parts_of_lines(year, day, test)
    towels = [towel.strip() for towel in puzzle_input[0][0].split(",")]
    print(towels)

    combos = puzzle_input[1]
    solution = 0

    @cache
    def possible(remaining: str) -> bool:
        for towel in towels:
            if remaining.startswith(towel):
                new_remaining = remaining[len(towel) :]
                # print(f"matching {towel} for {remaining}, stripped to {new_remaining}")
                if new_remaining == "":
                    return True
                if possible(new_remaining):
                    return True
        return False

    for combo in combos:
        if possible(combo):
            print(combo, "possible")
            solution += 1

    print(f"solution: {solution}")
