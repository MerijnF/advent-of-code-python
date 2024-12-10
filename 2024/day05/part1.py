from typing import Dict
import math
from utils.load import load_as_parts_of_lines


def solve(year: int, day: int, test: bool = False) -> None:
    # pylint: disable=W0632
    rules, page_sets = load_as_parts_of_lines(year, day, test)
    # pylint: enable=W0632
    rules_comes_after: Dict[int, list[int]] = {}
    for rule in rules:
        split = rule.split("|")
        a = int(split[0])
        b = int(split[1])
        # pylint: disable=C0201
        if a not in rules_comes_after.keys():
            rules_comes_after[a] = [b]
        else:
            rules_comes_after[a].append(b)
        # pylint: enable=C0201
    solution = 0
    for pages in page_sets:
        page_numbers = [int(number) for number in pages.split(",")]
        valid = True
        for i, number in enumerate(page_numbers):
            should_come_after_number = rules_comes_after.get(number)
            if should_come_after_number is None:
                continue
            for should_come_after in should_come_after_number:
                before = page_numbers[:i]
                if should_come_after in before:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            solution += page_numbers[math.floor(len(page_numbers) / 2)]

    print(f"solution: {solution}")
