# thermal.py
def calculate_thermal_derivative(C_tot, I, V, E_tn, K_dry, T, T_air, Q_evap):
    joule_heat = I * (V - E_tn)
    newton_cooling = K_dry * (T - T_air)
    return (joule_heat - newton_cooling - Q_evap) / C_tot
