"""
Suppose we want to add a functionality of randomly selecting 0 or 1 and returning
a string with 'Heads' or 'Tails', as if we were flipping a coin.
Here we have it implemented in three different ways. The first two ways give an
explicit mechanism of controlling the 'randomness' which makes it easier to test
and, in many cases, actually using the function within a more complex contest.
The consequences of these implementations are discussed in their respective tests.
"""
import numpy

from typing import Optional


def integer_to_coin_face(value: int):
    if value == 0:
        return 'Heads'
    elif value == 1:
        return 'Tails'
    else:
        raise ValueError(f'Unknown value to convert: {value}')


def flip_coin_from_generator(generator: Optional[numpy.random.Generator] = None):
    if generator is None:
        generator = numpy.random.default_rng()
    value = generator.integers(low=0, high=1, endpoint=True, size=None)
    return integer_to_coin_face(int(value))


def flip_coin_from_seed(seed: Optional[float] = None):
    """
    Simulate the flip of a coin

    Args:
        seed: seed for random generator. If None value is used (default), a
            'random' seed is used instead

    Returns:
        'Heads' or 'Tails' with a 50% change of either
    """
    generator = numpy.random.default_rng(seed)
    value = generator.integers(low=0, high=1, endpoint=True, size=None)
    return integer_to_coin_face(int(value))


def bad_flip_coin():
    value = numpy.random.randint(low=0, high=2, size=None)
    return integer_to_coin_face(int(value))
