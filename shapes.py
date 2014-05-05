import math

class Point(object):
    """Base Point class that is the parent to both Polar and Cartesian
    representations of points"""
    x = property(lambda self: self._x)
    y = property(lambda self: self._y)
    r = property(lambda self: self._r)
    theta =  property(lambda self: self._theta)
    
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

    def intersect(self, obj):
        """ Check which instance the object is, and dispatch the appropriate 
        intersection test method """
        if isinstance(obj, Line):
            return line_line_intersect(self, obj)

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


class LineSegment(object):
    """ Define a LineSegment object that will make checking if polygons
    intersect much easier."""
    def __init__(self, point1, point2):
        self._endpoint1 = point1
        self._endpoint2 = point2

    endpoint1 = property(lambda self: self._endpoint1)
    endpoint2 = property(lambda self: self._endpoint2)

    def length(self):
        return self.endpoint1.distance_to_point(self.endpoint2)

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

    def perimeter(self):
        """ returns the perimeter of the circle """
        return 2 * math.pi * self.radius

    def point_in_circle(self, point):
        """ returns true if the given Point object lies on or within the 
        perimeter of the Circle object """
        return point.distance_to_point(self.center) <= self.radius



def line_line_intersect(line1, line2):
    pass

def line_linesegment_intersect(line, segment):
    pass

def line_circle_intersect(line, circle):
    pass

def line_polygon_intersect(line, polygon):
    pass

def circle_circle_intersect(circle1, circle2):
    pass

def circle_linesegment_intersect(circle, segment):
    pass

def circle_polygon_intersect(circle, polygon):
    pass

def linesegment_linesegment_intersect(segment1, segment2):
    pass

def linesegment_polygon_intersect(segment, polygon):
    pass

def polygon_polygon_segment1(polygon1, polygon2):
    pass


