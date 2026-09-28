"""
Imagine this file represent an executable or a binary file which you need to
execute. It could be an external software or a compiled C++ code you need use
trough command line or prompt or a compiled C++ code you need to execute.
Here it will be a simple function to print the sum of two numbers.
"""

import argparse

from advance_examples import fake_imported_file


def add_two_numbers(value1: float, value2: float):
    result = fake_imported_file.sum_numbers(value1, value2)
    print(result)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Add two numbers')
    parser.add_argument(
        'first_number',
        type=float,
    )
    parser.add_argument(
        'second_number',
        type=float,
    )

    args = parser.parse_args()

    add_two_numbers(args.first_number, args.second_number)
