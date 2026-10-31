import pytest
from chlorine import calculate_expected_chlorine

def test_calculate_expected_chlorine():
    # Inputs with their physical meanings:
    x1 = 0.5          # Current efficiency (dimensionless, 50%)
    Q = 1000          # Charge passed (Coulombs)
    F = 96485         # Faraday's constant (C/mol)
    epsilon = 0.1     # Loss fraction (dimensionless, 10% loss)
    M_Cl2 = 70.9      # Molar mass of Cl2 (g/mol)
    V_L = 1.0         # Volume of solution (Liters)
    
    # Manual calculation based on Faraday's law:
    # Mass of Cl2 (mg) = x1 * (Q / (2 * F)) * (1 - epsilon) * M_Cl2 * (1000 / V_L)
    # Calculation: 0.5 * (1000 / 192970) * 0.9 * 70.9 * 1000 = 165.33658 mg/L
    expected_value = 165.33658
    
    result = calculate_expected_chlorine(x1, Q, F, epsilon, M_Cl2, V_L)
    
    # Verify the code's output matches the manual calculation (relative tolerance 1e-4)
    assert result == pytest.approx(expected_value, rel=1e-4)