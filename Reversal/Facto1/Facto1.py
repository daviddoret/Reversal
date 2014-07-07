__author__ = 'dmd'

from mpmath import *
mp.dps = 50

# By default, mpmath uses Python integers internally. If gmpy version 1.03 or later is installed on your system, mpmath will automatically detect it and transparently use gmpy integers intead. This makes mpmath much faster, especially at high precision (approximately above 100 digits).
# import mpmath.libmp


class Factor():

    def __init__(self, product):
        self.product = product
        self.root = sqrt(x=product)
        self.ab_points_with_index_a = {}
        self.xy_point_with_index_x = {}
        self.origin = Point(ab_x=0, ab_y=0, xy_x=0, xy_y=0)
        p1 = Point(ab_x=1, ab_y=product)
        self.add_point(p1)

    def __repr__(self):
        output = ""
        for item in self.ab_points_with_index_a:
            output = "{0}\n{1}".format(output, str(item))
        return output

    def add_point(self, point):
        self.ab_points_with_index_a[point.ab_x] = point
        self.xy_point_with_index_x[point.xy_x] = point


class Point():

    def __init__(self, ab_x, ab_y, xy_x=None, xy_y=None):
        self.ab_x = None
        self.ab_y = None
        self.xy_x = None
        self.xy_y = None
        if(ab_x is not None and ab_y is not None):
            self.ab_x = ab_x
            self.ab_y = ab_y
            self.infer_xys()

    def __repr__(self):
        return "p(ab.x:{0},ab.y:{1},xy.x:{2},xy.y:{3})".format(self.ab_x,self.ab_y,self.xy_x,self.xy_y)

    def get_inverse(self):
        return Point(ab_x=self.ab_y, ab_y=self.ab_x)

    def infer_xys(self):
        self.xy_x = sqrt( \
            power(x=self.ab_x, y=2) + power(x=self.ab_y,y=2) - power(x=(self.ab_x + self.ab_y), y=2) / 2)


def test_1():
    product = mpf(146)
    f = Factor(product=product)
    print(f)

test_1()
