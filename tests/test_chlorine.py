import pytest
from chlorine import calculate_expected_chlorine

def test_calculate_expected_chlorine():
    # Input values for the test
    x1 = 0.5
    Q = 1000
    F = 96485
    epsilon = 0.1
    M_Cl2 = 70.9
    V_L = 1.0
    
    # Manual calculation based on Faraday's law (as per the package formula):
    # 0.5 * (1000 / (2 * 96485)) * (1 - 0.1) * 70.9 * (1000 / 1.0) = 165.3365
    expected_value = 165.3365
    
    result = calculate_expected_chlorine(x1, Q, F, epsilon, M_Cl2, V_L)
    
    # Asserting that the code's output matches the manual calculation
    assert result == pytest.approx(expected_value, rel=1e-3)