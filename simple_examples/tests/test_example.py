import os

import pytest
import numpy

from simple_examples import example_functions


def test_sum():
    # Test setup. Here you should do the things you need to run the code you
    # want to test, like creating input files.
    numbers = [1, 2, 3]

    # Test execution. Here you would run the code you want to test and capture
    # its output for verification. If the code generates a file and/or does not
    # return a result, you need to have some way of getting the file content for
    # verification.
    sum_value = example_functions.sum_numbers(numbers)

    # Test assertion. Here you should verify if obtained "result" matches what
    # you expect. Note that the "result" does not needto be a "number".For example,
    # if the code is meant to change some data in a file, the "result" is that
    # the file was indeed changed AND that it changed to the correct thing.
    expected_value = 6
    # We can use equality here because it's an integer
    assert sum_value == expected_value

    # Test tear-down. Here you should "return everything to the way it was before
    # the test". For example, if you created a file, here you should delete it.
    # Thankfully, pytest and pytest-regressions will deal with this by themselves
    # under 99% of the cases.
    # This example test has nothing to "undo", so we don't have a tear-down step.


@pytest.mark.parametrize(
    'numbers, expected',
    [
        pytest.param([1, 2, 3], 6, id='sum_positive_integers'),
        pytest.param([-1, -2, -3], -6, id='sum_negative_integers'),
        pytest.param([0.5, 1.2, -2.5], -0.8, id='sum_floats'),
    ],
)
def test_many_sums(numbers, expected):
    # You can use pytest.mark.parametrize (need to import pyest) to simulate
    # changing input parameters and doing multiple functions calls. This is
    # great when you need to do the same test with different parameters.
    # See: https://docs.pytest.org/en/stable/example/parametrize.html
    # This will appear in pytest report as multiple tests.
    sum_value = example_functions.sum_numbers(numbers)
    # We should use equality here because these number may be "float"
    assert numpy.isclose(sum_value, expected)


def test_create_file(tmp_path):
    # "tmp_path" is a pytest fixture. It deals with creating a temporary directory,
    # which the system OS or pytest will deal with deleting. This is very useful
    # to avoid having to write the "tear-down" step of the test ourselves.

    # Setup
    filename = os.path.join(tmp_path, 'test_file.txt')

    # Execution
    value = 3
    example_functions.create_file(filename, value)

    # Verification 1. Check if the file was created
    assert os.path.isfile(filename)

    # Get file content for second verification
    with open(filename, 'r') as file:
        value_written = file.read()

    # Verification 2. Check if written value is correct
    assert int(value_written) == value

    # pytest will deal with tear-down, so we don't need to delete created
    # file afterward


def test_create_fancy_file(tmp_path, file_regression):
    # We will use pytest-regressions fixture (file_regression) to create the
    # "expected file" and deal with comparing it with what we got.
    filename = os.path.join(tmp_path, 'test_file.txt')
    example_functions.create_fancy_file(filename, 3)

    # Verification 1. Check if the file was created
    assert os.path.isfile(filename)

    # Verification 2. Check the full file content
    with open(filename, 'r') as file:
        content = file.read()
    file_regression.check(content)
