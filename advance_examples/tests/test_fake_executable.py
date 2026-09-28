import subprocess
import pathlib
import platform
import os


import pytest
import numpy


@pytest.mark.parametrize(
    'val1, val2, expected',
    [
        pytest.param(2, 5, 7, id='sum_positive_integers'),
        pytest.param(-1, -3, -4, id='sum_negative_integers'),
        pytest.param(-0.5, 1.2, 0.7, id='sum_floats'),
    ],
)
def test_fake_executable(val1, val2, expected):
    # This time we will deal with testing some sort of executable file external
    # to Python. Our 'problem case' is: we have an .py file which needs to be
    # executed through a command line during a Python test so we can verify that
    # it works properly.
    # This is more complicated than previous examples because now we need to deal
    # with how the executable even runs in the host machine our python code is
    # running. Of course, we should avoid such situation when possible.
    # One solution is to create python bindings to operate the external code as
    # if we were still inside Python. However, creating python binds is its
    # own challenge and out of scope for now.
    # Here, the solution will be to use Python's 'subprocess' library to run the
    # code through the machine terminal and capture the output.

    # Let's look at some strategies to actually do this.
    #
    # First idea is to create a bash (.sh Linux or .bat Windows) or sbatch (Slurm)
    # file and write in its content: the typical 'conda activate <env>' to activate
    # the correct python environment, and the command 'python <executable> <params>'.
    # Then we would need to just use Python's subprocess to execute that bash file.
    #
    # Second idea is to find the path for the python executable related to the
    # conda environment we want to use and call
    # '<conda_path>/python.exe <executable> <params>'.
    #
    # Here, we will do the second idea.

    # See inside the function bellow for why we need this
    pythonpath_command = get_pythonpath_command()

    # Get the command to run the .py file with its arguments using the python
    # executable of the conda environment we need.
    python_executable = get_python_executable()
    run_command = f'{python_executable} fake_executable.py {val1} {val2}'

    # Get the path where the .py file we want to run is
    executable_path = get_executable_path()


    # Build the full command line to set the 'PYTHONPATH' and execute the .py file.
    # It is important to note that some IDE's, like pycharm, will modify the
    # PYTHONPATH on our behalf and setting it here would be redundant.
    # However, this will not be usual case when someone runs pytest from outside
    # the IDE (like running pytest in the command line or inside a bash file).
    command_line = f'{pythonpath_command} && {run_command}'

    # Run the command using the machine's terminal using as working directory
    # the place where the .py file is
    info = subprocess.run(
        command_line, capture_output=True, shell=True, cwd=executable_path)

    # Get the print (result from the .py we ran) and decode it from bytes to a
    # regular string. Then we can just convert it to float.
    # A more usual situation is when the code we executed creates a file containing
    # the output. In this case, we would read that file and get the result
    # from it.
    result = info.stdout.decode("utf-8")
    result = float(result)

    assert numpy.isclose(result, expected)


# Note: The following free functions would normally be placed before all test
# functions, they are placed here just to make the explanation easier to follow.

def get_python_executable():
    # Here we can already see some of the problems of testing non-python code like
    # this. Since we need the path to the correct python, we need to deal with
    # which platform we are working on, and we need to assume that pytest is
    # running form the environment we want.
    # As we remove assumptions, the code gets more and more complicated.
    system_name = platform.system()
    if 'linux' in system_name.lower():
        return os.path.join(os.environ['CONDA_PREFIX'], 'bin', 'python')
    else:
        return os.path.join(os.environ['CONDA_PREFIX'], 'python.exe')


def get_pythonpath_command():
    # We also may need to worry about pointing the imports to the correct path of
    # the project, which is done via the 'PYTHONPATH' variable. Otherwise, we may
    # break the imports of the python code we are attempting to run.
    # This also creates an additional problem: how do we know the root of this
    # project?
    root_path = get_root_path()
    system_name = platform.system()
    if 'linux' in system_name.lower():
        return f'PYTHONPATH=\"{root_path}\":$PYTHONPATH'
    else:
        return f'set \"PYTHONPATH={root_path};%PYTHONPATH%\"'


def get_root_path() -> pathlib.Path:
    # One way to get the path to this project 'root' is by taking advantage of the
    # location of this particular .py file 'test_face_executable.py'.
    # This can be risky, however, because at some point the project structure
    # may change, which would require this function to change too.
    root_path = pathlib.Path(__file__).parents[2].resolve()
    return root_path


def get_executable_path():
    # Same idea as 'get_root_path', but to get the path to the python file we
    # want to run through the command line.
    root_path = pathlib.Path(__file__).parents[1].resolve()
    return os.path.join(root_path)
