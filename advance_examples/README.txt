Recommended reading order:
1) fake_executable_file.py
2) fake_imported_file.py
3) tests/test_fake_executable.py

Read all docstrings, comments and code from top to bottom. They have been organized
to facilitate reading in that order and may not make sense if you skip parts of it.


Additional Information for Executable Example

In order to compile this example, it is recommended to use cmake to generate
the makefile (Linux) or Visual Studio project (Windows).
In both cases, it's recommended to run cmake in a terminal with the conda environment
active, otherwise it may fail to find Pybind11.

Build location of Executable Example C++ code should be in
'executable_example/c_code/build' or 'executable_example/c_code/build/Release'.
Windows users normally use Visual Studio to compile, in that case you may run
'cmake -B build && cmake --build build --config Release' inside
'executable_example/c_code' to get it setup.
