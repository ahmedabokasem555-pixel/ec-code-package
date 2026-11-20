import numpy as np

from simulate import coverage_study, simulate_dpd


def test_simulate_is_reproducible_and_nonnegative():
    a = simulate_dpd(0.1, 0.2, 1000.0, 1.0, 0.1, np.random.default_rng(1))
    b = simulate_dpd(0.1, 0.2, 1000.0, 1.0, 0.1, np.random.default_rng(1))
    assert a == b and a >= 0


def test_coverage_calibrated_when_prior_correct():
    r = coverage_study(n_rep=60, grid_n=500, seed=3)
    assert 0.85 <= r["coverage"] <= 1.0
