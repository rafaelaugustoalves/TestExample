Basic Explanations


When running pytest, it will:
1) Look for directories starting with "test_"
2) Inside matching directories, it will look for ".py" files starting with "test_"
    * Matching files are also commonly referred to as "collected files"
3) Within files matching the name convention (step 2), it will look for functions whose name starts with "test_".
    * Matching functions are also commonly referred to as "collected functions" or "collected tests"
4) Pytest will them execute all collected tests (step 3):
    * If an error is raised during the function execution, it will mark the test as failed. Otherwise, it will mark it
        as passed.


Important:
* Due to behaviour described in step 4, you must write the function so that it will raise an error (python's
    Exception object) when you want the test to fail. It's not magic, you NEED to write the code so that it WILL fail
    when things do not behave as you want them to.
* Normally, we raise "AssertionError" to indicate that the behaviour is wrong, as a way to distinguish from
    unexpected errors. Usually, the person writing the test will call "assertion" to verify True/False statement, where
    True means everything is "ok".
* Pytest-regression (from ESSS) is a great tool to simplify writing, managing and running tests verification and its
    files. See: https://pytest-regressions.readthedocs.io/en/latest/overview.html


Recommended reading order:
1) example_functions.py
2) tests/test_example.py

Read all docstrings, comments and code from top to bottom. They have been organized
to facilitate reading in that order and may not make sense if you skip parts of it.
