from utils.load import load_as_characters


def solve(year: int, day: int, test: bool = False):
    input = load_as_characters(year, day, test)

    disk = []

    id = 0
    file = True
    for char in input:
        number = int(char)
        for i in range(number):
            if file:
                disk.append(id)
            else:
                disk.append(-1)
        if file:
            id += 1

        file = not file

    formatted_disk = []
    reversed_pointer = len(disk) - 1
    for disk_pointer in range(len(disk)):
        if disk[disk_pointer] != -1:
            formatted_disk.append(disk[disk_pointer])
        else:
            found = disk[reversed_pointer]
            while found == -1:
                reversed_pointer -= 1
                found = disk[reversed_pointer]
            formatted_disk.append(found)
            reversed_pointer -= 1
        if disk_pointer > reversed_pointer - 1:
            break

    check_sum = 0
    for x, i in enumerate(formatted_disk):
        if x != -1:
            check_sum += x * i
    print(f"solution: {check_sum}")
