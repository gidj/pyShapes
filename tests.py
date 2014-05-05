import unittest
from math import pi
from shapes import Cartesian, Polar, Line, Polygon

class PolarPointsTestCases(unittest.TestCase):
    """Basic tests on Point objects"""
    def setUp(self):
        self.polar1 = Polar(5, 0)
        self.polar2 = Polar(10, pi)
        self.polar3 = Polar(10, -pi)
        self.polar4 = Polar(5, pi/2)
        self.polar5 = Polar(5, -pi/2)

    def test_polar_pair_from_polar_pair(self):
        self.assertEqual(self.polar1.polar_pair(), (5, 0))

    def test_cartesian_pair_from_polar_pair(self):
        self.assertEqual(self.polar2.cartesian_pair()[0], -10)
        self.assertAlmostEqual(self.polar2.cartesian_pair()[1], 0, delta=0.00001)

    def test_polar_opposite_pi_angles_are_the_same(self):
        self.assertEqual(self.polar2.x, self.polar3.x)
        self.assertAlmostEqual(self.polar2.y, self.polar3.y, delta=0.00001)

    def test_polar_opposite_half_pis_are_opposites(self):
        self.assertAlmostEqual(self.polar4.x, self.polar5.x)
        self.assertAlmostEqual(self.polar4.y, -self.polar5.y)

class CartesianPointsTestCases(unittest.TestCase):
    def setUp(self):
        self.cart1 = Cartesian(0, 0)
        self.cart2 = Cartesian(1, 2)
        self.cart3 = Cartesian(-1, -1)
        self.cart4 = Cartesian(2, -4)
        self.cart5 = Cartesian(-3, 2)
    

class LinesTestCases(unittest.TestCase):
    """Test cases with onself.ly lines"""
    def setUp(self):
        pt1 = Cartesian(0, 0)
        pt2 = Cartesian(1, 1)
        pass
    

class CirclesTestCases(unittest.TestCase):
    """Test cases with only circles"""
    def setUp(self):
        pass


class PolygonTestCases(unittest.TestCase):
    """Test cases with only polygons"""
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
