from utils.load import load_as_parts_of_lines
from functools import cmp_to_key
from typing import Dict
import math


def solve(year: int, day: int, test: bool = False):
    rules, page_sets = load_as_parts_of_lines(year, day, test)
    rules_comes_after: Dict[int, list[int]] = {}
    rules_comes_before: Dict[int, list[int]] = {}
    for rule in rules:
        split = rule.split("|")
        a = int(split[0])
        b = int(split[1])
        if a not in rules_comes_after.keys():
            rules_comes_after[a] = [b]
        else:
            rules_comes_after[a].append(b)

        if b not in rules_comes_before.keys():
            rules_comes_before[b] = [a]
        else:
            rules_comes_before[b].append(a)

    solution = 0
    for pages in page_sets:
        page_numbers = [int(number) for number in pages.split(",")]
        if not are_pages_valid(page_numbers, rules_comes_after):
            sorted_page = sorted(
                page_numbers,
                key=cmp_to_key(
                    lambda a, b: compare(a, b, rules_comes_after, rules_comes_before)
                ),
            )

            solution += sorted_page[math.floor(len(page_numbers) / 2)]

    print(f"solution: {solution}")


def compare(
    a: int,
    b: int,
    rules_comes_after: Dict[int, list[int]],
    rules_comes_before: Dict[int, list[int]],
):
    numbers_that_should_come_after = rules_comes_after.get(b)
    numbers_that_should_come_before = rules_comes_before.get(b)
    comp = 0
    if numbers_that_should_come_after is not None:
        if a in numbers_that_should_come_after:
            comp = 1
    if numbers_that_should_come_before is not None:
        if a in numbers_that_should_come_before:
            comp = -1
    return comp


def are_pages_valid(page_numbers: list[int], rules_comes_after: Dict[int, list[int]]):
    valid = True
    for i, number in enumerate(page_numbers):
        numbers_that_should_come_after = rules_comes_after.get(number)
        if numbers_that_should_come_after is None:
            continue
        for should_come_after in numbers_that_should_come_after:
            before = page_numbers[:i]
            if should_come_after in before:
                valid = False
                break
        if not valid:
            break
    return valid
