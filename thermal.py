"""Single lumped thermal balance used as a diagnostic consistency check.

    C_tot dT/dt = I (V - E_tn) - K_dry (T - T_air) - Q_evap

It does not determine x1; it only checks that a simple energy balance can
reproduce the measured temperature trace.
"""

import numpy as np
from scipy.integrate import solve_ivp


def calculate_thermal_derivative(C_tot, I, V, E_tn, K_dry, T, T_air, Q_evap):
    """dT/dt (K/s) for constant I, V. Units: C_tot J/K, I A, V and E_tn V, K_dry W/K, Q_evap W."""
    if not C_tot > 0:
        raise ValueError("C_tot must be > 0")
    joule_heat = I * (V - E_tn)
    newton_cooling = K_dry * (T - T_air)
    return (joule_heat - newton_cooling - Q_evap) / C_tot


def simulate_temperature(t, T0, C_tot, I, V, E_tn, K_dry, T_air, Q_evap):
    """Integrate the balance at the times t (s, increasing). Returns temperatures at t."""
    t = np.asarray(t, dtype=float)
    if t.ndim != 1 or len(t) < 2 or np.any(np.diff(t) <= 0):
        raise ValueError("t must be a strictly increasing 1-D array with >= 2 points")
    sol = solve_ivp(
        lambda _t, y: [calculate_thermal_derivative(C_tot, I, V, E_tn, K_dry, y[0], T_air, Q_evap)],
        (t[0], t[-1]), [T0], t_eval=t, rtol=1e-8, atol=1e-10,
    )
    if not sol.success:
        raise RuntimeError(sol.message)
    return sol.y[0]


def max_abs_error(T_measured, T_model):
    """Maximum absolute temperature error (diagnostic)."""
    a = np.asarray(T_measured, dtype=float)
    b = np.asarray(T_model, dtype=float)
    if a.shape != b.shape:
        raise ValueError("shape mismatch")
    return float(np.max(np.abs(a - b)))
