import math

class Point(object):
    """Base Point class that is the parent to both Polar and Cartesian
    representations of points"""
    x = property(lambda self: self._x)
    y = property(lambda self: self._y)
    r = property(lambda self: self._r)
    theta = property(lambda self: self._theta)

    def __unicode__(self): 
        return "x={0}, y={1}, r={2}, theta={3}".format(self.x, self.y, self.r, self.theta)

    def __str__(self):
        return self.__unicode__()

    def cartesian_pair(self):
        """ Returns the x, y coordinates as a tuple """
        return (self.x, self.y)

    def polar_pair(self):
        """ Returns the r, theta polar coordinates as a tuple """
        return (self.r, self.theta)

    def distance_to_point(self, point):
        """ Returns the absolute distance from this point to a given point """
        return math.sqrt((self.x - point.x)**2 + (self.y - point.y)**2)


class Polar(Point):
    """Create a Point object given a radius 'r' and an angle 'theta'"""
    def __init__(self, r, theta):
        self._r = r
        self._theta = theta
    x = property(lambda self: self.r * math.cos(self.theta))
    y = property(lambda self: self.r * math.sin(self.theta))


class Cartesian(Point):
    """Create a Point object given x- and y-coordinates. """
    def __init__(self, x, y):
        self._x = x
        self._y = y
    r = property(lambda self: math.sqrt(self.x**2 + self.y**2))
    theta = property(lambda self: math.atan2(self.y, self.x))


class Line(object):
    """Base Line class that is the parent of LineByPoints and LineBySlope
    classes that are derived from it. All lines can be represented by a slope
    and a point."""
    x = property(lambda self: self._x)
    y = property(lambda self: self._y)
    slope = property(lambda self: self._slope)
    y_intercept = property(lambda self: self.y_given_x(0))

    def intersect(self, obj):
        """ Check which instance the object is, and dispatch the appropriate 
        intersection test method """
        if isinstance(obj, LineSegment):
            return line_linesegment_intersect(self, obj)
        elif isinstance(obj, Line):
            return line_line_intersect(self, obj)
        elif isinstance(obj, Circle):
            return line_circle_intersect(self, obj)
        elif isinstance(obj, Polygon):
            return line_polygon_intersect(self, obj)

    def is_vertical(self):
        return self.slope == float('inf')

    def x_given_y(self, y):
        """ Given a y value, return the associated value for x"""
        if self.slope == float('inf'):
            return self.x
        else:
            return ((y - self.y) / self.slope) + self.x

    def y_given_x(self, x):
        """ Given a x value, return the associated value for y. Returns
        the internal value of y for a vertical line"""
        if self.slope == float('inf'):
            return self.y
        else:
            return (self.slope * (x - self.x)) + self.y

class LineByPoints(Line):
    def __init__(self, point1, point2):
        # In the case of a vertical line
        if point1.x == point2.x:
            self._slope = float('inf')
            self._x = point1.x
            self._y = point1.y
        else:
            self._slope = (1.0 * (point2.y-point1.y)) / (point2.x-point1.x)
            self._x = point1.x
            self._y = point1.y


class LineBySlope(Line):
    """ Create a Line object when given a Point object and a slope"""
    def __init__(self, point, slope):
        self._x = point.x
        self._y = point.y
        self._slope = slope


class LineSegment(Line):
    """ Define a LineSegment object that will make checking if polygons
    intersect much easier."""
    def __init__(self, point1, point2):
        # In the case of a vertical line
        if point1.x == point2.x:
            self._slope = float('inf')
            self._x = point1.x
            self._y = point1.y
        else:
            self._slope = (1.0 * (point2.y-point1.y)) / (point2.x-point1.x)
            self._x = point1.x
            self._y = point1.y
        self._endpoint1 = point1
        self._endpoint2 = point2

    endpoint1 = property(lambda self: self._endpoint1)
    endpoint2 = property(lambda self: self._endpoint2)

    def intersect(self, obj):
        """ Check which instance the object is, and dispatch the appropriate 
        intersection test method """
        if isinstance(obj, LineSegment):
            return linesegment_linesegment_intersect(self, obj)
        elif isinstance(obj, Line):
            return line_linesegment_intersect(obj, self)
        elif isinstance(obj, Circle):
            return circle_linesegment_intersect(obj, self)
        elif isinstance(obj, Polygon):
            return linesegment_polygon_intersect(self, obj)

    def length(self):
        return self.endpoint1.distance_to_point(self.endpoint2)

    def point_between_endpoints(self, point):
        """Returns true if the provided point can be found between the x- and
        y- ranges of the LineSegment's endpoints. This is NOT a test for
        whether a given point is actually on the segment. Due to floating point
        equality testing that is problematic"""
        return point.x >= min(self.endpoint1.x, self.endpoint2.x) and \
               point.x <= max(self.endpoint1.x, self.endpoint2.x) and \
               point.y >= min(self.endpoint1.y, self.endpoint2.y) and \
               point.y <= max(self.endpoint1.y, self.endpoint2.y)


class Polygon(object):
    vertices = []
    def __init__(self, *args):
        for point in args:
            self.vertices.append(point)

    def edges(self):
        edges = []
        if len(self.vertices) < 2:
            return edges
        else:
            p0 = self.vertices[-1]
            for vertex in self.vertices:
               edges.append(LineSegment(p0, vertex))
               p0 = vertex
            return edges

    def intersect(self, obj):
        """ Check which instance the object is, and dispatch the appropriate 
        intersection test method """
        if isinstance(obj, LineSegment):
            return linesegment_polygon_intersect(obj, self)
        elif isinstance(obj, Line):
            return line_polygon_intersect(self, obj)
        elif isinstance(obj, Circle):
            return circle_polygon_intersect(obj, self)
        elif isinstance(obj, Polygon):
            return polygon_polygon_intersect(self, obj)

    def perimeter(self):
        if len(self.vertices) < 2:
            return 0
        else:
            perimeter = 0
            for edge in self.edges():
                perimeter += edge.length
            return perimeter


class Circle(object):
    """ Circle objects are represented by a center Point object and a radius
    scalar. """
    def __init__(self, center, radius):
        self._center = center
        self._radius = radius

    center = property(lambda self: self._center)
    x = property(lambda self: self.center.x)
    y = property(lambda self: self.center.y)
    radius = property(lambda self: self._radius)

    def intersect(self, obj):
        """ Check which instance the object is, and dispatch the appropriate 
        intersection test method """
        if isinstance(obj, LineSegment):
            return circle_linesegment_intersect(self, obj)
        elif isinstance(obj, Line):
            return line_circle_intersect(obj, self)
        elif isinstance(obj, Circle):
            return circle_circle_intersect(self, obj)
        elif isinstance(obj, Polygon):
            return circle_polygon_intersect(self, obj)

    def perimeter(self):
        """ returns the perimeter of the circle """
        return 2 * math.pi * self.radius

    def point_in_circle(self, point):
        """ returns true if the given Point object lies on or within the 
        perimeter of the Circle object """
        return point.distance_to_point(self.center) <= self.radius



def line_line_intersection(line1, line2):
    """ Returns the point where two lines intersect. If there is no point of 
    intersection, returns None"""
    if line1.slope == line2.slope:
        return None
    elif line1.slope == float('inf'):
        x = line1.x
        y = line2.y_given_x(x)
        return Cartesian(x, y)
    elif line2.slope == float('inf'):
        x = line2.x
        y = line2.y_given_x(x)
        return Cartesian(x, y)
    else:
        a = line1.slope
        b = line2.slope
        c = line1.y_intercept
        d = line2.y_intercept

        x = (d-c)/(a-b)
        y = a*((d-c)/(a-b)) + c
        return Cartesian(x, y)
         
def line_line_intersect(line1, line2):
    """ Returns whether two lines intersect. Since the Line class extends 
    infinitely in both directions, this is as simple as seeing if their slopes
    are equal and returning False if equal, True if otherwise """
    if line1.slope == line2.slope:
        return False
    else:
        return True

def line_linesegment_intersect(line, segment):
    """Here we first determine if two LINES will intersect; if so, we calculate
    the intersection point. Then, we check to see if that point is between the
    endponts of the line segment. If so, True; if not, False."""
    if line_line_intersection(line, segment):
        return segment.point_between_endpoints(line_line_intersection(line,segment))

def line_circle_intersect(line, circle):
    """ Taken from Wolfram mathworld: http://mathworld.wolfram.com/Circle-LineIntersection.html
    This is a straightforward test for whether a line will, at some point, 
    intersect a circle."""
    # for vertical lines: create a point on the line that has a y-coordiate the
    # same as the circle's center. Then test to see if that line is in the circle.
    if line.slope == float('inf'):
        test_point = Cartesian(line.x, circle.y)
        return circle.point_in_circle(test_point)
    else:
        new_x = line.x + 1
        new_y = line.y_given_x(new_x)
        dx = line.x - new_x
        dy = line.y - new_y
        dr = math.sqrt(dx**2 + dy**2)
        D = new_x*line.y - line.x*new_y
        discriminant = circle.radius**2 * dr**2 - D**2

        return discriminant >= 0

def line_polygon_intersect(line, polygon):
    """ Tests each edge of the Polygon recursively to see if it intersects 
    with a given line. """
    for edge in polygon.edges():
        if line_linesegment_intersect(line, edge):
            return True
    return False

def circle_circle_intersect(circle1, circle2):
    """ Returns whether two circles intersect. This is accomplished by seeing
    if the distance between their centers is less than or equal to the sum of
    their radii. If so, then they must intersect."""
    return (circle1.center.distance_to_point(circle2.center) <=
            circle1.radius + circle2.radius)

def circle_linesegment_intersect(circle, segment):
    """ Returns true if a LineSegment intersects Circle"""
    #To determine if a LineSegment intersects a Circle, we first determine
    #the line perpendicular to the given LineSegment that runs through the
    #center of the circle. With this line we find the intersection

    slope = -1 / segment.slope
    perpendicular_line = LineBySlope(circle.center, slope)

    # Now we find the intersection between segment and perpendiculary line;
    # this point will give us the nearest point of the line that segment is
    # part of to circle.

    lines_intersect = line_line_intersection(segment, perpendicular_line)

    # This point is the closest point to the circle on the line that contains 
    # the segment. If the point is on or in the circle, then that means the
    # segment may intersect the circle

    if circle.point_in_circle(lines_intersect):
        # The case where it is outside the circle
        return False
    else:
        # We check two things: is the point in the segment range? If it is,
        # we are finished and return True. We also check whether either endpoint
        # of the segment is in the circle. If so, True; if neither, False.
        return segment.point_between_endpoints(lines_intersect) or \
                circle.point_in_circle(segment.endpoint1) or \
                circle.point_in_circle(segment.endpoint2)

def circle_polygon_intersect(circle, polygon):
    """ This method returns whether a line segment intersects with a circle.
    """
    for edge in polygon.edges():
        if circle_linesegment_intersect(circle, edge):
            return True
    return False

def linesegment_linesegment_intersect(segment1, segment2):
    """ This is just a slightly special case of line and linesegment
    intersection. The test is the same."""
    return line_linesegment_intersect(segment1, segment2)

def linesegment_polygon_intersect(segment, polygon):
    """ Tests to see if each edge of a Polygon intersects with the given line
    segment. If any one edge does, return True. If none do, return False."""
    for edge in polygon.edges():
        if linesegment_linesegment_intersect(edge, segment):
            return True
    return False

def polygon_polygon_intersect(polygon1, polygon2):
    """Polygon - Polygon intersection is reduced to recursive segment - segment
    tests. This is true because if one polygon intersects another, at least one
    of its edges must intersect at least one of the other polygon's segments."""
    for edge1 in polygon1.edges():
        for edge2 in polygon2.edges():
            if linesegment_linesegment_intersect(edge1, edge2):
                return True
    return False

