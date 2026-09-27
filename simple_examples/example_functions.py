from typing import List


def sum_numbers(numbers: List[float]) -> float:
    return sum(numbers)


def create_file(filename: str, value: int) -> None:
    with open(filename, 'w+') as file:
        file.write(str(value))


def create_fancy_file(filename: str, value: int) -> None:
    with open(filename, 'w+') as file:
        file.write(f'This is a harder ({value}) file content to verify')
