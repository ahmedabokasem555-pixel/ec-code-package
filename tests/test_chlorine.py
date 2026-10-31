import pytest
from chlorine import calculate_expected_chlorine

def test_calculate_expected_chlorine():
    # قيم تجريبية بسيطة لاختبار الدالة
    x1 = 0.5
    Q = 1000
    F = 96485
    epsilon = 0.1
    M_Cl2 = 70.9
    V_L = 1.0
    
    result = calculate_expected_chlorine(x1, Q, F, epsilon, M_Cl2, V_L)
    
    # التأكد من أن النتيجة ليست فارغة وأنها رقم أكبر من صفر
    assert result is not None
    assert result > 0