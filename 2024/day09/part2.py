import copy
from dataclasses import dataclass
from utils.load import load_as_characters


@dataclass
class DiskInfo:
    is_file: bool
    size: int
    id: int | None = None


def solve(year: int, day: int, test: bool = False):
    test_input = load_as_characters(year, day, test)

    disk: list[DiskInfo] = []

    next_id = 0
    file = True
    for char in test_input:
        size = int(char)
        if file:
            disk.append(DiskInfo(True, size, next_id))
            next_id += 1
        else:
            disk.append(DiskInfo(False, size))

        file = not file

    # print_disk(disk)

    for to_move in reversed(copy.deepcopy(disk)):
        if not to_move.is_file:
            continue

        new_disk = []
        moved = False
        passed = False
        for info in disk:
            if info.is_file:
                if to_move.id == info.id:
                    passed = True

                if info.id == to_move.id and moved:
                    new_disk.append(DiskInfo(False, to_move.size))
                else:
                    new_disk.append(info)
            else:
                if info.size >= to_move.size and not moved and not passed:
                    new_disk.append(to_move)
                    remaining_size = info.size - to_move.size
                    if remaining_size > 0:
                        new_disk.append(DiskInfo(False, remaining_size))
                    moved = True
                else:
                    new_disk.append(info)
        disk = new_disk

    # print_disk(disk)

    check_sum = 0
    disk_index = 0
    for info in disk:
        if info.is_file:
            for _ in range(info.size):
                if info.id is not None:
                    check_sum += disk_index * info.id
                disk_index += 1
        else:
            disk_index += info.size

    # print()
    print(f"solution: {check_sum}")


def print_disk(disk: list[DiskInfo]):
    for info in disk:
        for _ in range(info.size):
            if info.is_file:
                print(info.id, end="")
            else:
                print(".", end="")
    print()
