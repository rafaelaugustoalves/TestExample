import os

import pytest
import numpy

from intermediary_examples import coin_flipper


def test_repeatability_flip_coin_from_seed():
    # Since the function we are testing allows controlling the 'randomness', we 
    # know which result to expect, and we can repeat the test any number of times
    # without risking failing the test
    for attempt in range(0, 100):
        coin_face = coin_flipper.flip_coin_from_seed(seed=0)
        assert coin_face == 'Tails'

    for attempt in range(0, 100):
        coin_face = coin_flipper.flip_coin_from_seed(seed=1)
        assert coin_face == 'Heads'


def test_repeatability_flip_coin_from_generator():
    # The function being tested may look 'clunkier', but this structure may be
    # useful in cases where a single generator is used in multiple different
    # parts of longer code.
    # In any case, what matters for our testing is that we can explicitly control
    # 'randomness' just as the previous implementation
    for attempt in range(0, 100):
        generator = numpy.random.default_rng(seed=0)
        coin_face = coin_flipper.flip_coin_from_generator(generator)
        assert coin_face == 'Tails'

    for attempt in range(0, 100):
        generator = numpy.random.default_rng(seed=1)
        coin_face = coin_flipper.flip_coin_from_generator(generator)
        assert coin_face == 'Heads'


def test_repeatability_bad_flip_coin():
    # This function does not give us a direct way of controlling the 'randomness'.
    # This means it will eventually fail unless we find an external way of
    # controlling it
    for attempt in range(0, 100):
        # The line bellow is our 'external' way of controlling the 'randomness'.
        # It may look fine, but consider the following:
        #   * What happens if we were testing a combination of random functions?
        #   * What happens if the generator changes within the function we are
        #     testing?
        # Here it 'looks fine' because it's a single line function, using a
        # well-known library to perform a 'trivial' task. We are almost never
        # working within all these conditions
        numpy.random.seed(1)
        coin_face = coin_flipper.bad_flip_coin()
        assert coin_face == 'Tails'

    for attempt in range(0, 100):
        numpy.random.seed(0)
        coin_face = coin_flipper.bad_flip_coin()
        assert coin_face == 'Heads'


@pytest.mark.parametrize(
    'seed, expected',
    [
        (0, 'Tails'),
        (1, 'Heads'),
        (19801, 'Tails'),
        (15865214, 'Heads'),
    ],
)
def test_seeds_flip_coin_from_seed(seed, expected):
    # This test is redundant, since we already have another test to check out
    # different seeds. It is implemented here just to show a different way doing
    # such test
    coin_face = coin_flipper.flip_coin_from_seed(seed=seed)
    assert coin_face == expected


def test_distribution_flip_coin_from_seed():
    # We know what distribution of 'Heads' and 'Tails' we should get, so it is
    # important that we check if we are  indeed getting such distribution
    tails_counter = 0
    num_flips = 500
    for attempt in range(0, num_flips):
        # We know from the documentation that if we use the 'default' value for
        # the seed, a random seed will be used. We could also generate our on
        # random seed in case the function didn't already offer us a way to do
        # it.
        face = coin_flipper.flip_coin_from_seed()
        if face == 'Tails':
            tails_counter += 1

    tails_frequency = tails_counter / num_flips
    expected_odds = 0.5

    # In this case, although the odds are 50% after an infinite number of coin
    # flips, there may be a noticeable fluctuation for a finite number of flips.
    # Our test should accommodate for that, otherwise it will eventually fail
    # just by coincidence.
    # Two ways of 'solving' this issue are: making a more 'flexible'
    # comparison (code line bellow) or increasing the number of flips (test
    # function bellow).

    # Note: having 'atol=0.1, rtol=0' means we are allowing a frequency between
    # 0.4 and 0.6
    assert numpy.isclose(tails_frequency, expected_odds, atol=0.1, rtol=0)


def test_tighter_distribution_flip_coin_from_seed():
    tails_counter = 0
    num_flips = 10000
    for attempt in range(0, num_flips):
        # We know from the documentation that if we use the 'default' value for
        # the seed, a random seed will be used. We could also generate our on
        # random seed in case the function didn't already offer us a way to do
        # it.
        face = coin_flipper.flip_coin_from_seed()
        if face == 'Tails':
            tails_counter += 1

    tails_frequency = tails_counter / num_flips

    expected_odds = 0.5

    # Note: having 'atol=0.01, rtol=0' means we are allowing a frequency between
    # 0.49 and 0.51
    assert numpy.isclose(tails_frequency, expected_odds, atol=0.01, rtol=0)

    # Now, is this a good idea to check the probability distribution like this?
    # Maybe. It depends on what you are planning to do, what 'issues' or
    # unexpected behaviours you expect, and how hard it is to test (unfortunately!).
    # Checking if we are getting a 50% odds is simple enough here because this is
    # a uniform distribution, we know the odds of each possible outcome and the
    # random result is quick to generate. Now suppose each coin flip took 1 minute
    # to do, would it be worth waiting ~8 hours just to see if odds are what we
    # expected? Or if we were 'simulating' something with a uniform distribution,
    # checking a single value may not even make sense.
    # From this we can quickly see that different cases will require different
    # strategies. Maybe we can check if the average of the distribution is what
    # we expect; or we can generate many times once from a single starting seed,
    # visually inspect if it has the 'shape' we expect and then just test
    # repeatability.


# @pytest.mark.parametrize(
#     'numbers, expected',
#     [
#         pytest.param([1, 2, 3], 6, id='sum_positive_integers'),
#         pytest.param([-1, -2, -3], -6, id='sum_negative_integers'),
#         pytest.param([0.5, 1.2, -2.5], -0.8, id='sum_floats'),
#     ],
# )
# def test_many_sums(numbers, expected):
#     # You can use pytest.mark.parametrize (need to import pyest) to simulate
#     # changing input parameters and doing multiple functions calls. This is
#     # great when you need to do the same test with different parameters.
#     # See: https://docs.pytest.org/en/stable/example/parametrize.html
#     # This will appear in pytest report as multiple tests.
#     sum_value = example_functions.sum_numbers(numbers)
#     # We should use equality here because these number may be "float"
#     assert numpy.isclose(sum_value, expected)

