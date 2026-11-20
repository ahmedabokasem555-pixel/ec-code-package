"""Synthetic-data utilities and a calibration (coverage) study.

EVERYTHING produced here is SIMULATED. It tests whether the inference behaves as designed when the
truth is known. It is not experimental validation and must never be presented as measured DPD data.
"""

import warnings

import numpy as np

from chlorine import calculate_expected_chlorine
from inference import run_inference

FARADAY = 96485.33212
M_CL2 = 70.906


def simulate_dpd(x1, eps, Q, V_L, sigma, rng, F=FARADAY, M_Cl2=M_CL2):
    """One synthetic DPD reading (mg/L): true mu plus Gaussian noise (clipped at 0)."""
    mu = calculate_expected_chlorine(x1, Q, F, eps, M_Cl2, V_L)
    return float(max(mu + rng.normal(0.0, sigma), 0.0))


def coverage_study(n_rep=200, true_eps_params=(1.2, 4.9), prior_params=(1.2, 4.9), sigma=0.1,
                   Q=1000.0, V_L=1.0, grid_n=800, eps_max=0.6, seed=0):
    """Repeatedly simulate a run with known (x1, eps), infer, and record coverage of the 95% interval.

    x1 ~ Uniform(0.02, 0.30); eps ~ Beta(true_eps_params) truncated to (0.001, eps_max).
    prior_params is the prior ASSUMED by the inference; a mismatch with true_eps_params tests robustness.
    Returns a dict with coverage, mean interval width, and median absolute error of the posterior median.
    """
    rng = np.random.default_rng(seed)
    xg = np.linspace(1e-4, 0.35, grid_n)
    eg = np.linspace(0.001, eps_max, grid_n)
    hit, width, err = [], [], []
    for _ in range(n_rep):
        x1 = rng.uniform(0.02, 0.30)
        while True:
            eps = rng.beta(*true_eps_params)
            if 0.001 < eps < eps_max:
                break
        C = simulate_dpd(x1, eps, Q, V_L, sigma, rng)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            _, med, lo, hi, _ = run_inference(C, V_L, FARADAY, M_CL2, Q, xg, eg,
                                              prior_params=prior_params, sigma=sigma)
        hit.append(lo <= x1 <= hi)
        width.append(hi - lo)
        err.append(abs(med - x1))
    return {"n_rep": n_rep, "coverage": float(np.mean(hit)), "mean_width": float(np.mean(width)),
            "median_abs_error": float(np.median(err))}
