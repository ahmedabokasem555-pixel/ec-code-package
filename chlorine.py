# chlorine.py
def calculate_expected_chlorine(x1, Q, F, epsilon, M_Cl2, V_L):
    return x1 * (Q / (2 * F)) * (1 - epsilon) * M_Cl2 * (1000 / V_L)

def calculate_apparent_efficiency(C_meas, V_L, F, M_Cl2, Q):
    return (2 * F * C_meas * V_L) / (1000 * M_Cl2 * Q)
