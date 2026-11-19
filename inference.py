"""Grid-based inference of the current efficiency x1 given a prior on the loss fraction eps.

Likelihood: C_meas ~ Normal(mu(x1, eps), sigma);  prior: eps ~ Beta(a, b); flat prior on x1.
The reported interval is CONDITIONAL on this model and prior. It is not a validated
coverage statement. DPD fixes only x1*(1-eps), so the x1 interval is driven largely by the prior.
"""

import warnings

import numpy as np
from scipy.stats import beta

DEFAULT_SIGMA = 0.01  # mg/L, measurement standard deviation (an assumption; change it to your own)


def run_inference(C_meas, V_L, F, M_Cl2, Q, x1_grid, epsilon_grid,
                  prior_params=(1.2, 4.9), sigma=DEFAULT_SIGMA):
    """Return (marginal_x1, median_x1, lower_ci, upper_ci, marginal_eps).

    The grids must be strictly increasing; epsilon_grid within [0, 1). The grid must resolve the
    likelihood ridge (spacing small relative to sigma): a RuntimeWarning is issued if it does not,
    because coarse grids give wrong intervals. Check convergence by refining both grids.
    """
    x1_grid = np.asarray(x1_grid, dtype=float)
    epsilon_grid = np.asarray(epsilon_grid, dtype=float)
    for name, g in (("x1_grid", x1_grid), ("epsilon_grid", epsilon_grid)):
        if g.ndim != 1 or len(g) < 2 or np.any(np.diff(g) <= 0):
            raise ValueError(f"{name} must be a strictly increasing 1-D array with >= 2 points")
    if epsilon_grid[0] < 0 or epsilon_grid[-1] >= 1:
        raise ValueError("epsilon_grid must lie in [0, 1)")
    if not sigma > 0:
        raise ValueError("sigma must be > 0")
    if C_meas < 0 or min(V_L, F, M_Cl2, Q) <= 0:
        raise ValueError("C_meas must be >= 0 and V_L, F, M_Cl2, Q must be > 0")

    X1, Eps = np.meshgrid(x1_grid, epsilon_grid, indexing="ij")
    mu = X1 * (Q / (2 * F)) * (1 - Eps) * M_Cl2 * (1000 / V_L)
    z = (C_meas - mu) / sigma
    a, b = prior_params
    with np.errstate(divide="ignore"):
        log_post = -0.5 * z ** 2 + beta.logpdf(Eps, a, b)

    if np.min(np.abs(z)) > 5:
        raise ValueError(
            "No grid cell lies within 5 sigma of C_meas: the measurement is incompatible with the "
            "grids/prior, or the grids are far too coarse.")
    post = np.exp(log_post - np.nanmax(log_post[np.isfinite(log_post)]))
    post = np.where(np.isfinite(post), post, 0.0)
    post /= post.sum()

    # Resolution check: the ridge x1*(1-eps) = const must be sampled finely across its width (sigma).
    # Use the posterior mode cell; require the finer axis to change mu by <= 3 sigma per grid step.
    i, j = np.unravel_index(np.argmax(post), post.shape)
    k = (Q / (2 * F)) * M_Cl2 * (1000 / V_L)
    step_x = k * (1 - epsilon_grid[j]) * np.max(np.diff(x1_grid))
    step_e = k * x1_grid[i] * np.max(np.diff(epsilon_grid))
    if min(step_x, step_e) > 3 * sigma:
        warnings.warn(
            "Grids are too coarse to resolve the likelihood ridge (mu changes by "
            f"{min(step_x, step_e):.3g} mg/L per grid step vs sigma = {sigma:g}). Intervals are "
            "unreliable; refine the grids until the result stops changing.",
            RuntimeWarning, stacklevel=2)

    marginal_x1 = post.sum(axis=1)
    marginal_eps = post.sum(axis=0)
    cdf = np.cumsum(marginal_x1)
    last = len(x1_grid) - 1

    def q(p):
        return float(x1_grid[min(int(np.searchsorted(cdf, p)), last)])

    return marginal_x1, q(0.5), q(0.025), q(0.975), marginal_eps


def prior_only_interval(eta_app, prior_params=(1.2, 4.9), level=0.95):
    """x1 interval implied by the prior on eps alone: x1 = eta_app / (1 - eps).

    Returns (lower, median, upper). Compare with run_inference to see how much the data add.
    """
    a, b = prior_params
    lo = (1 - level) / 2
    e = beta.ppf([lo, 0.5, 1 - lo], a, b)
    x = eta_app / (1 - e)
    return float(x[0]), float(x[1]), float(x[2])
