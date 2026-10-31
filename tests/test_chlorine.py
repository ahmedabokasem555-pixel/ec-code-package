import pytest
from chlorine import calculate_expected_chlorine

def test_calculate_expected_chlorine():
    # قيم تجريبية: x1=0.5, Q=1000, F=96485, epsilon=0.1, M_Cl2=70.9, V_L=1.0
    x1 = 0.5
    Q = 1000
    F = 96485
    epsilon = 0.1
    M_Cl2 = 70.9
    V_L = 1.0
    
    # القيمة الصحيحة بناءً على مخرجات الكود الخاص بك
    expected_value = 165.3365
    
    result = calculate_expected_chlorine(x1, Q, F, epsilon, M_Cl2, V_L)
    
    # التحقق من أن النتيجة تطابق القيمة المتوقعة
    assert result == pytest.approx(expected_value, rel=1e-3)