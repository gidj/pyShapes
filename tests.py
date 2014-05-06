import unittest
from math import pi
from shapes import Cartesian, Polar, Line, LineByPoints, LineBySlope, LineSegment
from shapes import Circle, Polygon
from shapes import line_line_intersect, line_line_intersection, line_linesegment_intersect, \
        line_circle_intersect, line_polygon_intersect, circle_circle_intersect, \
        circle_linesegment_intersect, circle_polygon_intersect, \
        linesegment_linesegment_intersect, linesegment_polygon_intersect, \
        polygon_polygon_intersect


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
        self.cart2 = Cartesian(1, 0)
        self.cart3 = Cartesian(0, 10)
        self.cart4 = Cartesian(-2, 0)
        self.cart5 = Cartesian(-3, 2)

    def test_origin_cartesian_converts_to_theta_zero(self):
        self.assertEqual(self.cart1.theta, 0)

    def test_negative_x_and_zero_y_is_pi(self):
        self.assertAlmostEqual(self.cart4.theta, pi)

    def test_number_on_the_positive_y_axis_is_half_pi(self):
        self.assertAlmostEqual(self.cart3.theta, pi/2)


class LinesTestCases(unittest.TestCase):
    """Test cases with only lines"""
    def setUp(self):
        self.pt1 = Cartesian(0, 0)
        self.pt2 = Cartesian(1, 1)
        self.pt3 = Cartesian(1, 2)
        self.pt4 = Cartesian(0, 2)
        self.pt5 = Cartesian(1, -1)

    def test_y_given_x_of_5_with_slope_of_1(self):
        l = LineByPoints(self.pt1, self.pt2)
        self.assertEqual(l.y_given_x(5), 5)

    def test_x_given_y_of_5_with_slope_of_1(self):
        l = LineByPoints(self.pt1, self.pt2)
        self.assertEqual(l.x_given_y(5), 5)

    def test_slope_is_one(self):
        l = LineByPoints(self.pt1, self.pt2)
        self.assertEqual(l.slope, 1)

    def test_verticle_line_slope_is_inf(self):
        l = LineByPoints(self.pt2, self.pt3)
        self.assertEqual(l.slope, float('inf'))

    def test_horizontal_line_slope_is_zero(self):
        l = LineByPoints(self.pt3, self.pt4)
        self.assertEqual(l.slope, 0)

    def test_negative_slope(self):
        l = LineByPoints(self.pt1, self.pt5)
        self.assertEqual(l.slope, -1)


class CirclesTestCases(unittest.TestCase):
    """Test cases with only circles"""
    def setUp(self):
        self.p = Cartesian(0, 0)
        self.p1 = Cartesian(1, 1)
        self.p2 = Cartesian(10, 20)
        self.circ = Circle(self.p, 5)
        self.circ1 = Circle(self.p1, 1)
        self.circ2 = Circle(self.p2, 1)

    def test_perimeter(self):
        self.assertAlmostEqual(self.circ1.perimeter(), 2*pi)

    def test_edge_of_circle_in_circle(self):
        test_point = Cartesian(5, 0)
        self.assertTrue(self.circ.point_in_circle(test_point))

    def test_point_outside_of_circle(self):
        test_point = Cartesian(10, 10)
        self.assertFalse(self.circ.point_in_circle(test_point))

    def test_two_intersecting_circles_intersect(self):
        self.assertTrue(self.circ.intersect(self.circ1))
        # Make sure it's reflexive
        self.assertTrue(self.circ1.intersect(self.circ))

    def test_two_nonintersecting_circles_not_intersect(self):
        self.assertFalse(self.circ.intersect(self.circ2))
        # make sure it's relfexive
        self.assertFalse(self.circ2.intersect(self.circ))


class LineSegmentTests(unittest.TestCase):
    def setUp(self):
        self.seg1 = LineSegment(Cartesian(-2, -1), Cartesian(1, 2))
        self.seg2 = LineSegment(Cartesian(0, 0), Cartesian(3, -3))
        self.vert = LineSegment(Cartesian(-1, 1), Cartesian(-1, 4))
        self.horiz = LineSegment(Cartesian(0, 0), Cartesian(6, 0))

    def test_segments_that_arent_parallel_but_dont_intersect(self):
        self.assertFalse(linesegment_linesegment_intersect(
            self.seg1, self.seg2))

    def test_vertical_segment_not_intersecting(self):
        self.assertFalse(linesegment_linesegment_intersect(
            self.seg1, self.vert))

    def test_horizontal_segment_not_intersecting(self):
        self.assertFalse(linesegment_linesegment_intersect(
            self.seg1, self.horiz))

class PolygonTestCases(unittest.TestCase):
    """Test cases with only polygons"""
    def setUp(self):
        self.p1 = Cartesian(1, 0)
        self.p2 = Cartesian(1, 2)
        self.p3 = Cartesian(3, 2)
        self.p4 = Cartesian(3, 0)
        self.poly1 = Polygon(self.p1,
                        self.p2,
                        self.p3,
                        self.p4)

        self.p5 = Cartesian(1, 3)
        self.p6 = Cartesian(2, 4)
        self.p7 = Cartesian(4, 2)
        self.p8 = Cartesian(3, 1)
        self.poly2 = Polygon(self.p5,
                        self.p6,
                        self.p7,
                        self.p8)

        self.p9 = Cartesian(-1, 1)
        self.p10 = Cartesian(2, 1)
        self.p11 = Cartesian(2, -1)
        self.p12 = Cartesian(-1, -1)
        self.poly3 = Polygon(self.p9,
                        self.p10,
                        self.p11,
                        self.p12)

    def test_poly1_poly2_intersect(self):
        self.assertTrue(self.poly1.intersect(self.poly2))
        self.assertTrue(self.poly2.intersect(self.poly1))
        
    def test_poly1_poly3_intersect(self):
        self.assertTrue(self.poly1.intersect(self.poly3))
        self.assertTrue(self.poly3.intersect(self.poly1))

    def test_poly2_poly3_dont_intersect(self):
        self.assertFalse(self.poly2.intersect(self.poly3))
        self.assertFalse(self.poly3.intersect(self.poly2))


class DifferentObjectsTests(unittest.TestCase):
    def setUp(self):
        self.p = Cartesian(0, 0)
        self.p1 = Cartesian(1, 1)
        self.p2 = Cartesian(10, 20)
        self.circ = Circle(self.p, 5)
        self.circ1 = Circle(self.p1, 1)
        self.circ2 = Circle(self.p2, 1)

        self.p5 = Cartesian(1, 3)
        self.p6 = Cartesian(2, 4)
        self.p7 = Cartesian(4, 2)
        self.p8 = Cartesian(3, 1)
        self.poly2 = Polygon(self.p5,
                        self.p6,
                        self.p7,
                        self.p8)
        self.p9 = Cartesian(-1, 1)
        self.p10 = Cartesian(2, 1)
        self.p11 = Cartesian(2, -1)
        self.p12 = Cartesian(-1, -1)
        self.poly3 = Polygon(self.p9,
                        self.p10,
                        self.p11,
                        self.p12)

    def test_circle_overlapping_polygon_intersect(self):
        self.assertTrue(self.poly2.intersect(self.circ1))
        self.assertTrue(self.circ1.intersect(self.poly2))

    def test_circle_not_overlapping_polygon_dont_intersect(self):
        self.assertFalse(self.poly2.intersect(self.circ2))
        self.assertFalse(self.circ2.intersect(self.poly2))


if __name__ == '__main__':
    unittest.main()
