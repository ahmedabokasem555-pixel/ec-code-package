# inference.py
import numpy as np
from scipy.stats import beta

def run_inference(C_meas, V_L, F, M_Cl2, Q, x1_grid, epsilon_grid, prior_params=(1.2, 4.9)):
    X1, Eps = np.meshgrid(x1_grid, epsilon_grid, indexing="ij")
    mu = X1 * (Q / (2 * F)) * (1 - Eps) * M_Cl2 * (1000 / V_L)
    likelihood = np.exp(-0.5 * ((C_meas - mu) / 0.01) ** 2)
    a, b = prior_params
    prior_eps = beta.pdf(Eps, a, b)
    posterior = likelihood * prior_eps
    posterior /= np.sum(posterior)
    marginal_x1 = np.sum(posterior, axis=1)
    marginal_eps = np.sum(posterior, axis=0)
    cdf_x1 = np.cumsum(marginal_x1)
    median_x1 = x1_grid[np.searchsorted(cdf_x1, 0.5)]
    lower_ci = x1_grid[np.searchsorted(cdf_x1, 0.025)]
    upper_ci = x1_grid[np.searchsorted(cdf_x1, 0.975)]
    return marginal_x1, median_x1, lower_ci, upper_ci, marginal_eps
