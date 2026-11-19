"""Faraday-based chlorine accounting.

Equations (see paper.md):
    n_Cl2 = x1 * Q / (2 F)                                   (Faraday, 2 e- per Cl2)
    mu    = x1 * Q/(2F) * (1 - eps) * M_Cl2 * 1000 / V_L     [mg/L as Cl2]
    eta_app = 2 F C_meas V_L / (1000 M_Cl2 Q) = x1 * (1 - eps)

DPD alone fixes only the product x1 * (1 - eps); separating x1 from the loss
fraction eps requires a prior on eps (see inference.py).
"""

FARADAY = 96485.33212  # C/mol
M_CL2 = 70.906  # g/mol


def _positive(name, value):
    if not value > 0:
        raise ValueError(f"{name} must be > 0, got {value!r}")


def calculate_expected_chlorine(x1, Q, F, epsilon, M_Cl2, V_L):
    """Expected free-chlorine concentration mu in mg/L as Cl2.

    Parameters
    ----------
    x1 : float
        Current efficiency of Cl2 formation, 0 <= x1 <= 1.
    Q : float
        Charge passed (C).
    F : float
        Faraday constant (C/mol).
    epsilon : float
        Fraction of formed chlorine lost before the DPD reading, 0 <= epsilon < 1.
    M_Cl2 : float
        Molar mass of Cl2 (g/mol).
    V_L : float
        Solution volume (litres).
    """
    _positive("Q", Q)
    _positive("F", F)
    _positive("M_Cl2", M_Cl2)
    _positive("V_L", V_L)
    if not 0 <= x1 <= 1:
        raise ValueError(f"x1 must be in [0, 1], got {x1!r}")
    if not 0 <= epsilon < 1:
        raise ValueError(f"epsilon must be in [0, 1), got {epsilon!r}")
    return x1 * (Q / (2 * F)) * (1 - epsilon) * M_Cl2 * (1000 / V_L)


def calculate_apparent_efficiency(C_meas, V_L, F, M_Cl2, Q):
    """Apparent efficiency eta_app = x1 * (1 - epsilon) from a DPD reading C_meas (mg/L).

    C_meas must already include any dilution factor.
    """
    if C_meas < 0:
        raise ValueError(f"C_meas must be >= 0, got {C_meas!r}")
    _positive("V_L", V_L)
    _positive("F", F)
    _positive("M_Cl2", M_Cl2)
    _positive("Q", Q)
    return (2 * F * C_meas * V_L) / (1000 * M_Cl2 * Q)