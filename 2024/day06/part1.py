from typing import Literal
from utils.grid import Grid, GridStepper
from utils.load import load_as_line_characters


def solve(year: int, day: int, test: bool = False):
    test_input = load_as_line_characters(year, day, test)

    grid = Grid(test_input)
    grid_stepper = GridStepper(grid)

    grid_stepper.find_start("^")
    grid_stepper.direction = "U"

    def on_collision(
        _x, _y, prev_x: int, prev_y: int, direction: Literal["U", "D", "L", "R"]
    ) -> tuple[int, int, Literal["U", "D", "L", "R"]]:
        new_direction: Literal["U", "D", "L", "R"] = "U"
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
    print(f"solution: {len(list(grid_stepper.visited()))}")
