import warnings

import numpy as np
import pytest

from chlorine import calculate_apparent_efficiency, calculate_expected_chlorine
from inference import prior_only_interval, run_inference

F, M, V, Q = 96485.33212, 70.906, 1.0, 1000.0


def _case(x1=0.05, eps=0.2):
    return calculate_expected_chlorine(x1, Q, F, eps, M, V)


def test_posterior_is_normalised_and_brackets_truth():
    C = _case()
    xg = np.linspace(1e-4, 0.35, 1000)
    eg = np.linspace(0.001, 0.6, 1000)
    mx, med, lo, hi, me = run_inference(C, V, F, M, Q, xg, eg)
    assert mx.sum() == pytest.approx(1.0) and me.sum() == pytest.approx(1.0)
    assert lo <= med <= hi
    assert lo <= 0.05 <= hi


def test_converges_with_grid_refinement():
    C = _case()
    res = []
    for n in (1000, 2000):
        xg = np.linspace(1e-4, 0.35, n)
        eg = np.linspace(0.001, 0.6, n)
        res.append(run_inference(C, V, F, M, Q, xg, eg)[1:4])
    assert np.allclose(res[0], res[1], atol=2e-3)


def test_coarse_grid_warns():
    C = _case()
    xg = np.linspace(1e-4, 0.35, 50)
    eg = np.linspace(0.001, 0.6, 50)
    with pytest.warns(RuntimeWarning):
        run_inference(C, V, F, M, Q, xg, eg)


def test_conditional_interval_not_narrower_than_prior_only_here():
    """DPD fixes only x1*(1-eps): the x1 interval is essentially prior-driven."""
    C = _case()
    eta = calculate_apparent_efficiency(C, V, F, M, Q)
    xg = np.linspace(1e-4, 0.35, 2000)
    eg = np.linspace(0.001, 0.6, 2000)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        _, _, lo, hi, _ = run_inference(C, V, F, M, Q, xg, eg)
    plo, _, phi = prior_only_interval(eta)
    assert (hi - lo) > 0.8 * (phi - plo)


def test_incompatible_measurement_raises():
    xg = np.linspace(1e-4, 0.05, 200)
    eg = np.linspace(0.001, 0.6, 200)
    with pytest.raises(ValueError):
        run_inference(1e6, V, F, M, Q, xg, eg)


def test_bad_grids_raise():
    with pytest.raises(ValueError):
        run_inference(1.0, V, F, M, Q, [0.2, 0.1], [0.1, 0.2])
    with pytest.raises(ValueError):
        run_inference(1.0, V, F, M, Q, [0.1, 0.2], [0.1, 1.2])


def test_prior_only_interval_ordering():
    lo, med, hi = prior_only_interval(0.04)
    assert 0.04 < lo < med < hi
