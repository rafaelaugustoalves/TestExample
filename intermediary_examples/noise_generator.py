import numpy
import matplotlib.pyplot as plt

from typing import Optional


def create_noise(
    num_numbers: int = 1,
    generator: Optional[numpy.random.Generator] = None,
) -> numpy.typing.NDArray:
    if generator is None:
        generator = numpy.random.default_rng()
    values = generator.normal(loc=0.0, scale=0.5, size=num_numbers)
    return values


if __name__ == "__main__":
    # # Following up the discussion at the enf of the coin flip example, on how to
    # # 'test' a function which returns a normal distribution. We can verify it
    # # 'visually' as the bases to avoid a more formal test. Of course, this comes
    # # with its own obvious risks. A proper statistical analysis is advised, when
    # # possible.
    # example_generator = numpy.random.default_rng(seed=0)
    # noise_values = create_noise(num_numbers=1000, generator=example_generator)
    # print(noise_values)
    #
    # figure, axes = plt.subplots(1, 2, sharey=True, tight_layout=True)
    # counts, bins = numpy.histogram(noise_values, bins=20)
    # axes[0].stairs(counts, bins, fill=True)
    # axes[0].set_xlim(xmin=-2, xmax=2)
    # plt.show()

    import scipy
    generator = numpy.random.default_rng(seed=None)
    values = create_noise(num_numbers=10000, generator=generator)

    # values = scipy.stats.norm.rvs(loc=0.0, scale=0.5, size=1000, )

    expected_distribution = scipy.stats.norm  # normal distribution

    # res = scipy.stats.goodness_of_fit(
    #     expected_distribution,
    #     values,
    #     known_params={'loc': 0.0, 'scale': 0.5},
    #     # statistic='ks',
    #     # random_state=rng
    # )

    res = scipy.stats.ks_1samp(values, scipy.stats.norm.cdf, args=(0.0, 0.5), alternative='two-sided')

    print("Statistic:", res.statistic)
    print("P-value:", res.pvalue)

