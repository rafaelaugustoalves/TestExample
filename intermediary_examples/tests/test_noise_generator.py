import numpy
import scipy

from intermediary_examples import noise_generator


def test_generate_noise(ndarrays_regression):
    generator = numpy.random.default_rng(seed=0)
    # In the python file where the function we are testing is defined, we
    # already visually inspected the histogram of the generated noise. It looks
    # like a normal distribution, so we may choose to just check repeatability,
    # that is, given the same seed we get the same distribution.
    values = noise_generator.create_noise(num_numbers=1000, generator=generator)

    # We will use pytest-regressions fixture (ndarrays_regression) to create the
    # 'expected file' which contains the generated float values and deal with
    # comparing it with what we got.
    result = {'distribution': values}
    ndarrays_regression.check(result)


def test_statistics_generate_noise():
    # Testing if the distribution is in fact a normal distribution can be 'tricky'.
    # Some ideas are to check the mean and standard deviation (std), but of course
    # it may not be good enough depending on the context.
    generator = numpy.random.default_rng(seed=0)
    values = noise_generator.create_noise(num_numbers=1000, generator=generator)

    obtained_mean = numpy.average(values)
    obtained_std = numpy.std(values)

    expected_mean = 0.0
    expected_std = 0.5

    assert numpy.isclose(obtained_mean, expected_mean, rtol=0, atol=0.05)
    assert numpy.isclose(obtained_std, expected_std, rtol=0, atol=0.05)


def test_fittness_generate_noise():
    values = noise_generator.create_noise(num_numbers=10000, generator=None)

    # Testing if the distribution is in fact a normal distribution can be 'tricky'.
    # One way of answering 'Does the generated values follow a gaussian distribution?'
    # is using the one-sample Kolmogorov-Smirnov test for goodness of fit.
    # Under alternative 'two-sided', if p-value is bellow 0.05 we have 95%
    # confidence that generated values do follow the distribution we are checking
    # against.
    # Since we know the 'loc' and 'scale' values, we can pass them in 'args'.
    # For details check the page bellow:
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ks_1samp.html
    res = scipy.stats.ks_1samp(
        values, scipy.stats.norm.cdf, args=(0.0, 0.5), alternative='two-sided')

    assert res.pvalue > 0.05

    # This is a good example of why we need to consider how hard it is to test
    # some aspects of our code. To actually check if we have a normal distribution
    # we had to: install one extra external library (scipy), learn which goodness
    # of fitness test would be useful for our case and how to interpret the result.
    # Is it worth here? Again, depends.
    # Are we worried the function has some unexpected behaviour which could lead
    # it to not generate a normal distribution? I would say no, because we are
    # using a well-known solution which is very straight forward to use.
    # Is our visual inspection of the result too unreliable? I would say no,
    # because a normal distribution is 'easy' to spot.
    # There are many other things we could consider to make the decision, the
    # point here is that sometimes we need to settle for the 'good enough' instead
    # of aiming for the 'best' solution.
