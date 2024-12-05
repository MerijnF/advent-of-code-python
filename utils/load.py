def load_as_lines(year: int, day: int, test: bool = False) -> list[str]:
    prefix = get_test_prefix(test)
    with open(f"input/{year}/day{day:02}/{prefix}input.txt", "r") as input_file:
        return [line.strip() for line in input_file.readlines()]


def load_as_string(year: int, day: int, test: bool = False) -> str:
    prefix = get_test_prefix(test)
    with open(f"input/{year}/day{day:02}/{prefix}input.txt", "r") as input_file:
        return input_file.read()


def load_as_split_lines(year: int, day: int, test: bool = False) -> list[list[str]]:
    prefix = get_test_prefix(test)
    with open(f"input/{year}/day{day:02}/{prefix}input.txt", "r") as input_file:
        return [line.strip().split() for line in input_file.readlines()]


def load_as_line_characters(year: int, day: int, test: bool = False) -> list[list[chr]]:
    prefix = get_test_prefix(test)
    with open(f"input/{year}/day{day:02}/{prefix}input.txt", "r") as input_file:
        return [list(line.strip()) for line in input_file.readlines()]


def load_as_parts_of_lines(
    year: int, day: int, test: bool = False, delimiter: str = "\n"
) -> list[list[str]]:
    prefix = get_test_prefix(test)
    with open(f"input/{year}/day{day:02}/{prefix}input.txt", "r") as input_file:
        result = [[]]
        index = 0
        for line in input_file.readlines():
            if line == delimiter:
                index += 1
                result.append([])
            else:
                result[index].append(line.strip())
        return result


def get_test_prefix(test):
    prefix = ""
    if test:
        prefix = "test-"
    return prefix
