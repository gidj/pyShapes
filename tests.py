import unittest
from shapes import Point

class PointsTestCases(unittest.TestCase):
    """Basic tests on Point objects"""
    pass


class LinesTestCases(unittest.TestCase):
    """Test cases with only lines"""
    def setUp(self):
        pt1 = Point(0, 0)
        pt2 = Point(1, 1)
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
