import numpy as np
import pytest

from thermal import calculate_thermal_derivative, max_abs_error, simulate_temperature


def test_derivative_zero_at_steady_state():
    # I*(V-E)=2 W, cooling K*(T-Tair)=2 W, no evaporation
    assert calculate_thermal_derivative(1000, 1.0, 3.0, 1.0, 0.2, 35.0, 25.0, 0.0) == pytest.approx(0.0)


def test_simulation_matches_analytic_solution():
    C, I, V, E, K, Ta = 1000.0, 1.0, 3.0, 1.0, 0.2, 25.0
    t = np.linspace(0, 5000, 50)
    T = simulate_temperature(t, Ta, C, I, V, E, K, Ta, 0.0)
    T_ss = Ta + I * (V - E) / K
    analytic = T_ss + (Ta - T_ss) * np.exp(-K * t / C)
    assert max_abs_error(analytic, T) < 1e-4


def test_bad_inputs():
    with pytest.raises(ValueError):
        simulate_temperature([0], 25, 1000, 1, 3, 1, 0.2, 25, 0)
    with pytest.raises(ValueError):
        calculate_thermal_derivative(0, 1, 3, 1, 0.2, 30, 25, 0)
    with pytest.raises(ValueError):
        max_abs_error([1, 2], [1])
