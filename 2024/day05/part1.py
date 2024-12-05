from utils.load import load_as_parts_of_lines
from typing import Dict
import math


def solve(year: int, day: int, test: bool = False):
    rules, page_sets = load_as_parts_of_lines(year, day, test)
    rules_comes_after: Dict[int, list[int]] = {}
    for rule in rules:
        split = rule.split("|")
        a = int(split[0])
        b = int(split[1])
        if a not in rules_comes_after.keys():
            rules_comes_after[a] = [b]
        else:
            rules_comes_after[a].append(b)

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
