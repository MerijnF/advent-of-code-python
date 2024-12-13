from dataclasses import dataclass
import re
from utils.load import load_as_parts_of_lines

MAX_PRESSES = 100
PATTERN = r"X[+-=]?(\d+), Y[+-=]?(\d+)"


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_parts_of_lines(year, day, test)

    solution = 0

    for i, machine in enumerate(test_input):
        a = get_xy(machine[0])
        b = get_xy(machine[1])
        prize = get_xy(machine[2])
        position = (0, 0)

        print("Machine ", i)
        print("Button A: ", a[0], a[1])
        print("Button B: ", b[0], b[1])
        print("Prize: ", prize[0], prize[1])

        if (MAX_PRESSES * a[0] + MAX_PRESSES * b[0]) < prize[0] and (
            MAX_PRESSES * a[1] + MAX_PRESSES * b[1]
        ) < prize[1]:
            # quickly determine estimated impossible
            print("impossible")
            continue

        cheapest = move_to_prize(position, [Move(a, 3), Move(b, 1)], [0, 0], prize)
        print("cheapest ", cheapest)
        if cheapest != -1:
            solution += cheapest

    print(f"solution: {solution}")


@dataclass
class Move:
    direction: tuple[int, int]
    cost: int


def move_to_prize(
    position: tuple[int, int],
    moves: list[Move],
    counts: list[int],
    prize: tuple[int, int],
    current_cost: int = 0,
) -> int:

    results = []
    for i, move in enumerate(moves):
        if counts[i] > MAX_PRESSES:
            results.append(-1)
            continue
        new_pos = (position[0] + move.direction[0], position[1] + move.direction[1])
        cost = current_cost + move.cost
        # print("testing", new_pos, "for", cost, "tokens")
        if new_pos == prize:
            print("found prize")
            results.append(cost)
        elif new_pos[0] > prize[0] or new_pos[1] > prize[1]:
            # print("moved too far")
            results.append(-1)
        else:
            # print("moving")
            new_counts = counts.copy()
            new_counts[i] = new_counts[i] + 1
            results.append(
                move_to_prize(new_pos, moves[i:], new_counts[i:], prize, cost)
            )
    return min((x for x in results if x != -1), default=-1)


def get_xy(line: str) -> tuple[int, int]:
    match = re.search(PATTERN, line)
    if match is not None:
        x = int(match.group(1))
        y = int(match.group(2))
        return (x, y)
    return (0, 0)
