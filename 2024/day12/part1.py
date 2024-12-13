from dataclasses import dataclass
from utils.grid import Grid
from utils.load import load_as_line_characters


@dataclass
class Plot:
    plant: str
    perimeter: int
    area: int
    positions: list[tuple[int, int]]


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_line_characters(year, day, test)
    plant_map = Grid(test_input)
    plots: list[Plot] = []

    for x, y, val in plant_map.iterate():
        if val != ".":
            plot = Plot(val, 0, 0, [])
            fill_plot(plant_map, plot, x, y)
            print(plot.plant, plot.perimeter, plot.area)
            plots.append(plot)

            for x, y in plot.positions:
                plant_map.set(x, y, ".")

    solution = 0
    for plot in plots:
        solution += plot.area * plot.perimeter

    print(solution)


def fill_plot(grid: Grid[str], plot: Plot, x: int, y: int):
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

    right = (x + 1, y)
    left = (x - 1, y)
    up = (x, y - 1)
    down = (x, y + 1)

    fill_plot(grid, plot, *right)
    fill_plot(grid, plot, *left)
    fill_plot(grid, plot, *up)
    fill_plot(grid, plot, *down)
