import unittest
from ec_code.chlorine import calculate_expected_chlorine

class TestChlorineModel(unittest.TestCase):
    def test_faraday_law(self):
        # Test with x1=1, Q=2F, epsilon=0, M_Cl2=70.9, V_L=1
        result = calculate_expected_chlorine(1.0, 2*96485.33, 96485.33, 0.0, 70.9, 1.0)
        self.assertAlmostEqual(result, 70900.0, places=1)

    def test_loss_fraction(self):
        # Test with 50% loss
        result = calculate_expected_chlorine(1.0, 2*96485.33, 96485.33, 0.5, 70.9, 1.0)
        self.assertAlmostEqual(result, 35450.0, places=1)

if __name__ == '__main__':
    unittest.main()