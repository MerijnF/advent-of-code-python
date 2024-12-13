from dataclasses import dataclass, field
from utils.grid import Grid
from utils.load import load_as_line_characters

d_north = (0, -1)
d_east = (1, 0)
d_south = (0, 1)
d_west = (-1, 0)

directions = [d_north, d_east, d_south, d_west]


@dataclass
class Area:
    plant: str
    perimeter: int
    area: int
    positions: list[tuple[int, int]]

    northern_plots: set[tuple[int, int]] = field(default_factory=set)
    southern_plots: set[tuple[int, int]] = field(default_factory=set)
    eastern_plots: set[tuple[int, int]] = field(default_factory=set)
    western_plots: set[tuple[int, int]] = field(default_factory=set)


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_line_characters(year, day, test)
    plant_map = Grid(test_input)

    solution = 0

    for x, y, val in plant_map.iterate():
        if val != ".":
            plot = Area(val, 0, 0, [])
            fill_plot(plant_map, plot, x, y)

            edges = count_connected_edges(plot)
            print(plot.plant, plot.area, edges)

            solution += plot.area * edges

            for x, y in plot.positions:
                # print(f"({x}, {y})")
                plant_map.set(x, y, ".")

    print(solution)


def count_connected_edges(area: Area) -> int:
    edges = 0
    northen = count_connected_points(area.northern_plots)
    edges += northen
    southern = count_connected_points(area.southern_plots)
    edges += southern
    eastern = count_connected_points(area.eastern_plots)
    edges += eastern
    western = count_connected_points(area.western_plots)
    edges += western
    return edges


def count_connected_points(points: set[tuple[int, int]]) -> int:
    count = 0
    visited: set[tuple[int, int]] = set()

    def dfs(check: tuple[int, int]) -> None:
        if check in visited:
            return
        visited.add(check)
        for direction in directions:
            neighbor = (check[0] + direction[0], check[1] + direction[1])
            if neighbor in points:
                dfs(neighbor)

    for point in points:
        if point in visited:
            continue
        count += 1
        dfs(point)
    return count


def fill_plot(grid: Grid[str], plot: Area, x: int, y: int):

    def set_edge(direction: tuple[int, int]) -> None:
        if direction == d_north:
            plot.northern_plots.add((x, y))
        elif direction == d_east:
            plot.eastern_plots.add((x, y))
        elif direction == d_south:
            plot.southern_plots.add((x, y))
        elif direction == d_west:
            plot.western_plots.add((x, y))

    def part_of_plot(check: tuple[int, int], direction: tuple[int, int]) -> bool:
        if not grid.in_bounds(*check):
            plot.perimeter += 1
            set_edge(direction)
            return False
        if grid.get(*check) != plot.plant:
            plot.perimeter += 1
            set_edge(direction)
            return False

        return True

    if (x, y) in plot.positions:
        return
    if not grid.in_bounds(x, y):
        plot.perimeter += 1
        return

    if grid.get(x, y) != plot.plant:
        plot.perimeter += 1
        return

    plot.positions.append((x, y))
    plot.area += 1

    for d in directions:
        check = (x + d[0], y + d[1])
        if part_of_plot(check, d):
            fill_plot(grid, plot, *check)
