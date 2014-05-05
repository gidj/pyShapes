import math


class Point(object):
    """Abstract Point class that is the parent to both Polar and Cartesian
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


class Polar(Point):
    """Create a Point object given a radius 'r' and an angle 'theta'"""
    def __init__(self, r, theta):
        self._r = r
        self._theta = theta
    x = property(lambda self: self.r * math.cos(self.theta))
    y = property(lambda self: self.r * math.sin(self.theta))


class Cartesian(Point):
    """Create a Point object given x- and y-coordinates"""
    def __init__(self, x, y):
        self._x = x
        self._y = y
    r = property(lambda self: math.sqrt(self.x**2 + self.y**2))
    theta = property(lambda self: math.atan((1.0*self.x) / self.y))


class Line:
    def __init__(self, point, slope):
        pass

class Polygon:
    def __init__(self, *args):
        pass
