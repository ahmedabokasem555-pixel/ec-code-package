import pytest
from chlorine import calculate_chlorine_decay

def test_chlorine_decay_basic():
    # اختبار بسيط للتأكد من أن الدالة تعمل
    result = calculate_chlorine_decay(initial=1.0, time=1.0)
    assert result is not None
    assert result > 0