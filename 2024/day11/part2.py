from utils.load import load_as_split_string_of_integers
from functools import cache


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_split_string_of_integers(year, day, test)

    solution = 0
    for stone in test_input:
        solution += stones_after_blinks(stone, 75)

    print(f"solution: {solution}")


@cache
def stones_after_blinks(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1
    if stone == 0:
        return stones_after_blinks(1, blinks - 1)
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        count = 0
        left = int(stone_str[: len(stone_str) // 2])
        count += stones_after_blinks(left, blinks - 1)
        right = int(stone_str[len(stone_str) // 2 :])
        count += stones_after_blinks(right, blinks - 1)
        return count
    return stones_after_blinks(stone * 2024, blinks - 1)
