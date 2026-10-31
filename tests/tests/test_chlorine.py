import pytest
from ec_code.chlorine import calculate_chlorine_decay # تأكد من تغيير هذا المسار حسب اسم دالتك الفعلي

def test_chlorine_decay_basic():
    # اختبار بسيط للتأكد من أن الدالة تعمل ولا تعطي خطأ
    result = calculate_chlorine_decay(initial=1.0, time=1.0)
    assert result is not None
    assert result > 0