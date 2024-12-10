from typing import Dict
from itertools import permutations
from utils.grid import Grid
from utils.load import load_as_line_characters


def solve(year: int, day: int, test: bool = False):
    test_input = load_as_line_characters(year, day, test)
    nodes = Grid(test_input)

    frequencies: Dict[str, list[tuple[int, int]]] = {}

    for _, _, val in nodes.iterate():
        if val != "." and val not in frequencies:
            frequencies[val] = nodes.find(val)

    anti_nodes = Grid([["." for _ in range(nodes.width)] for _ in range(nodes.height)])

    for _, value in frequencies.items():
        for xy_a, xy_b in permutations(value, 2):
            a_x, a_y = xy_a
            b_x, b_y = xy_b

            dist_x = abs(a_x - b_x)
            dist_y = abs(a_y - b_y)

            anti_x = a_x
            anti_y = a_y

            if a_x > b_x:
                anti_x = a_x + dist_x
            elif a_x < b_x:
                anti_x = a_x - dist_x

            if a_y > b_y:
                anti_y = a_y + dist_y
            elif a_y < b_y:
                anti_y = a_y - dist_y

            if anti_nodes.in_bounds(anti_x, anti_y):
                anti_nodes.set(anti_x, anti_y, "#")

    anti_nodes.print()
    print("solution:", len(anti_nodes.find("#")))
