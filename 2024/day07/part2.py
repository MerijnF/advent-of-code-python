from utils.load import load_as_split_lines


def solve(year: int, day: int, test: bool = False):
    test_input = load_as_split_lines(year, day, test)

    solution = 0
    for line in test_input:
        result = int(line[0][:-1])
        values = [int(x) for x in line[1:]]

        if operate_to(result, values):
            solution += result

    print(f"solution: {solution}")


def operate_to(result: int, values: list[int]) -> bool:
    a = values[0]
    b = values[1]

    sum_result = a + b
    mul_result = a * b
    concat_result = int(str(a) + str(b))

    if len(values) == 2:
        return (
            (sum_result == result)
            or (mul_result == result)
            or (concat_result == result)
        )

    sum_found = operate_to(result, [sum_result] + values[2:])
    mul_found = operate_to(result, [mul_result] + values[2:])
    concat_found = operate_to(result, [concat_result] + values[2:])

    return sum_found or mul_found or concat_found
