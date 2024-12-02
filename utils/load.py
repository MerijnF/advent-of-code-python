def load_as_lines(year: int, day: int, test: bool = False) -> list[str]:
    prefix = ""
    if test:
        prefix = "test-"
    with open(f"input/{year}/day{day:02}/{prefix}input.txt", "r") as input_file:
        return input_file.readlines()
