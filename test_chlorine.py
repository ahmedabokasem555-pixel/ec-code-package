import pytest

from chlorine import calculate_apparent_efficiency, calculate_expected_chlorine

F, M = 96485, 70.9


def test_calculate_expected_chlorine():
    # 0.5 * (1000 / 192970) * 0.9 * 70.9 * 1000 = 165.33658 mg/L
    assert calculate_expected_chlorine(0.5, 1000, F, 0.1, M, 1.0) == pytest.approx(165.33658, rel=1e-4)


def test_reduces_to_faraday_when_no_loss():
    mu = calculate_expected_chlorine(1.0, 2 * F, F, 0.0, M, 1.0)  # 1 mol Cl2 in 1 L
    assert mu == pytest.approx(M * 1000)


def test_apparent_efficiency_is_x1_times_one_minus_eps():
    x1, eps, Q, V = 0.3, 0.25, 500.0, 0.5
    C = calculate_expected_chlorine(x1, Q, F, eps, M, V)
    assert calculate_apparent_efficiency(C, V, F, M, Q) == pytest.approx(x1 * (1 - eps))


@pytest.mark.parametrize("kwargs", [
    dict(x1=1.5, Q=1, F=F, epsilon=0.1, M_Cl2=M, V_L=1),
    dict(x1=0.5, Q=1, F=F, epsilon=1.0, M_Cl2=M, V_L=1),
    dict(x1=0.5, Q=-1, F=F, epsilon=0.1, M_Cl2=M, V_L=1),
    dict(x1=0.5, Q=1, F=F, epsilon=0.1, M_Cl2=M, V_L=0),
])
def test_invalid_inputs_raise(kwargs):
    with pytest.raises(ValueError):
        calculate_expected_chlorine(**kwargs)
