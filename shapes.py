from math import sqrt, atan


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def r(self):
        """ Returns the value of the radius extending from the origin (0, 0)
        to the point """
        return sqrt(self.x**2 + self.y**2)

    def theta(self):
        """ Returns theta, the polar coordinate angle of the point,
        in radians """
        return atan((1.0*self.x) / self.y) # 1.0 to ensure integers are floting

    def cartesian_pair(self):
        """ Returns the x, y coordinates as a tuple """
        return (self.x, self.y)

    def polar_pair(self):
        """ Returns the r, theta polar coordinates as a tuple """
        return (self.r(), self.theta())
