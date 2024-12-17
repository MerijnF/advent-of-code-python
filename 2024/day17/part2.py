from dataclasses import dataclass
from math import trunc
import re
from utils.load import load_as_lines

REGISTER_PATTERN = r"Register [ABC]: (\d+)"


@dataclass
class State:
    a: int
    b: int
    c: int
    program: list[int]
    pointer: int = 0


def solve(year: int, day: int, test: bool = False) -> None:
    test_input = load_as_lines(year, day, test)

    program = [int(x) for x in test_input[4].replace("Program: ", "").split(",")]

    matches = recursive_try_a(0, program)
    print(matches)


def recursive_try_a(prev_a: int, program: list[int], matching: int = 1) -> list[int]:
    expected = program[-matching:]
    print(f"matching: {matching}, expected: {expected}")
    matches = try_for_a(prev_a, program, expected)
    if expected == program:
        return matches
    found: list[int] = []
    for match in matches:
        found = found + recursive_try_a(match * 8, program, matching + 1)
    return found


def try_for_a(prev_a: int, program: list[int], expected_end: list[int]):
    matches: list[int] = []
    for d_a in range(0, 8):
        a = prev_a + d_a
        state = State(a, 0, 0, program)
        output = run(state)
        print(a, output)
        if output == expected_end:
            matches.append(a)

    return matches


def run(state: State) -> list[int]:
    halt = False
    out: list[int] = []
    # print(state)
    while not halt:
        instruction = state.program[state.pointer]
        operand = state.program[state.pointer + 1]
        # print(instruction, operand)

        match instruction:
            case 0:  # adv
                op_value = get_combo_operand_value(state, operand)
                state.a = trunc(state.a / (pow(2, op_value)))
                state.pointer += 2
            case 1:  # bxl
                state.b = state.b ^ operand
                state.pointer += 2
            case 2:  # bst
                op_value = get_combo_operand_value(state, operand)
                state.b = op_value % 8
                state.pointer += 2
            case 3:  # jnz
                if state.a != 0:
                    state.pointer = operand
                else:
                    state.pointer += 2
            case 4:  # bxc
                state.b = state.b ^ state.c
                state.pointer += 2
            case 5:  # out
                op_value = get_combo_operand_value(state, operand)
                out.append(op_value % 8)
                # print(out)
                state.pointer += 2
            case 6:  # bdv
                op_value = get_combo_operand_value(state, operand)
                state.b = trunc(state.a / (pow(2, op_value)))
                state.pointer += 2
            case 7:  # cdv
                op_value = get_combo_operand_value(state, operand)
                state.c = trunc(state.a / (pow(2, op_value)))
                state.pointer += 2
        # print(state)
        if state.pointer >= len(state.program):
            halt = True
    return out


def get_combo_operand_value(state: State, operand: int) -> int:
    match operand:
        case 0:
            return 0
        case 1:
            return 1
        case 2:
            return 2
        case 3:
            return 3
        case 4:
            return state.a
        case 5:
            return state.b
        case 6:
            return state.c
        case 7:
            raise ValueError("invalid use of reserved operand: 7")

    raise ValueError(f"invalid operand: {operand}")


def read_register_from_input(line) -> int:
    match = re.match(REGISTER_PATTERN, line)
    if match is None:
        raise ValueError(f"invalid input: {line}")
    value = match.group(1)
    if value is None:
        raise ValueError(f"invalid input: {line}")

    return int(value)
