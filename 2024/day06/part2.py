from typing import Literal
from utils.grid import Grid, GridStepper
from utils.load import load_as_line_characters


def solve(year: int, day: int, test: bool = False):
    input = load_as_line_characters(year, day, test)

    grid = Grid(input)
    grid_stepper = GridStepper(grid)

    grid_stepper.find_start("^")

    start_x = grid_stepper.x
    start_y = grid_stepper.y

    grid_stepper.direction = "U"

    def on_collision(
        x, y, prev_x, prev_y, direction
    ) -> tuple[int, int, Literal["U", "D", "L", "R"]]:
        new_direction = None
        match direction:
            case "U":
                new_direction = "R"
            case "D":
                new_direction = "L"
            case "L":
                new_direction = "U"
            case "R":
                new_direction = "D"
        return (prev_x, prev_y, new_direction)

    grid_stepper.on_collision = on_collision
    grid_stepper.fill_collision_mask(lambda x: x != "#")

    grid_stepper.step_until(["OUT-OF-BOUNDS"])

    solution = 0
    for x, y in grid_stepper.visited():
        if x == start_x and y == start_y:
            continue
        new_grid = grid.deepCopy()
        new_grid.set(x, y, "#")

        new_grid_stepper = GridStepper(new_grid, (start_x, start_y))
        new_grid_stepper.direction = "U"

        new_grid_stepper.on_collision = on_collision
        new_grid_stepper.fill_collision_mask(lambda x: x != "#")

        result = new_grid_stepper.step_until(["OUT-OF-BOUNDS", "LOOP"])
        if result == "LOOP":
            solution += 1

    print(f"solution: {solution}")
