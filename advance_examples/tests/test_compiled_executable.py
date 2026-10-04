import subprocess
import pathlib
import platform
import os


import pytest
import numpy

# Remember to compile the C++ code and its python bind before trying to run this
# file tests! Check README.txt for instructions.

# Bellow is an add-hoc solution to accommodate Visual Studio default build path.
# This is NOT a good solution for dealing with Python imports
try:
    from advance_examples.executable_example.c_code.build import examplepybind
except (ModuleNotFoundError, ImportError):
    from advance_examples.executable_example.c_code.build.Release import examplepybind


@pytest.mark.parametrize(
    'val1, val2, expected',
    [
        pytest.param(2, 5, 7, id='sum_positive_integers'),
        pytest.param(-1, -3, -4, id='sum_negative_integers'),
        pytest.param(-0.5, 1.2, 0.7, id='sum_floats'),
    ],
)
def test_binary_executable(val1, val2, expected):
    # This time we are using a proper executable file so we can just "call" the
    # executable file in the command line
    executable_filename = get_executable_filename()
    command_line = f'{executable_filename} {val1} {val2}'

    # Run the command using the machine's terminal using as working directory
    # the place where the .py file is
    info = subprocess.run(
        command_line, capture_output=True, shell=True)

    # As in the previous example, the executable will output (print) the result
    # in the "terminal"
    result = info.stdout.decode("utf-8")
    result = float(result)

    assert numpy.isclose(result, expected)


def get_root_path() -> pathlib.Path:
    # This function is repeated here just to make the example easier to follow.
    # In a real situation, this function should be placed in a separate file so
    # all tests can use it.
    # In a real case, AVOID DUPLICATING CODE
    root_path = pathlib.Path(__file__).parents[2].resolve()
    return root_path


def get_executable_filename() -> str:
    # Getting the correct path for the binary files is tricky because we are not
    # using any of the "guard rails" one would set up to make its location known
    # beforehand. For this reason, we need to fumble around for it
    root_path = get_root_path()
    c_code_path = os.path.join(
        root_path, 'advance_examples', 'executable_example', 'c_code')
    system_name = platform.system()

    tried_locations = []
    if 'linux' in system_name.lower():
        executable_path = os.path.join(c_code_path, 'build')
        tried_locations.append(executable_path)
    else:
        executable_path = None
        for vs_dir in ['Release', 'Debug', 'MinSizeRel', 'RelWithDebInfo']:
            possible_dir = os.path.join(c_code_path, 'build', vs_dir)
            tried_locations.append(possible_dir)

            if os.path.isdir(possible_dir):
                executable_path = possible_dir
                break

    if executable_path is None or not os.path.isdir(executable_path):
        raise FileNotFoundError(
            f'Unable to find executable path is default locations: {tried_locations}')

    filename = os.path.join(executable_path, 'SumNumbers.exe')
    return filename


@pytest.mark.parametrize(
    'val1, val2, expected',
    [
        pytest.param(2, 5, 7, id='sum_positive_integers'),
        pytest.param(-1, -3, -4, id='sum_negative_integers'),
        pytest.param(-0.5, 1.2, 0.7, id='sum_floats'),
    ],
)
def test_python_bind(val1, val2, expected):
    # This time we have a python bind for the C++ code, so testing goes the
    # same as a regular python code. Of course, we still had all the extra work
    # to create the python bind in the first place and get it compiled

    result = examplepybind.add_two_numbers(val1, val2)

    assert numpy.isclose(result, expected)
