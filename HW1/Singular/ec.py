# This does not really matter, but for completeness it is nice.

class Curve:
    def __init__(self, p: int, a: int, b: int) -> None:
        self.p = p
        self.a = a
        self.b = b

    def is_on_curve(self, x: int, y: int) -> bool:
        return (y**2 - x**3 - self.a*x - self.b) % self.p == 0

class Point:
    def __init__(self, curve: Curve, x: int|None, y: int|None) -> None:
        self.curve = curve
        if x == None or y == None: 
            self.is_infinity = True
            return
        
        assert(curve.is_on_curve(x, y))
        self.is_infinity = False
        self.x = x
        self.y = y
        pass

    def __eq__(self, other) -> bool:
        if self.is_infinity:
            return other.is_infinity
        return 0 == self.x - other.x % self.curve.p and 0 == self.y - other.y % self.curve.p

    def __add__(self, other): 
        if self.is_infinity:
            return other

        if other == -self:
            return Point(self.curve, None, None)

        lam = 0
        if self != other:
            lam = ((other.y - self.y) * pow(other.x - self.x, -1, self.curve.p)) % self.curve.p
        else:
            lam = ((3 * self.x**2 + self.curve.a) * pow(2 * self.y, -1, self.curve.p)) % self.curve.p

        x = (lam**2 - self.x - other.x) % self.curve.p
        y = (lam * (self.x - x) - self.y) % self.curve.p

        return Point(self.curve, x, y)

    def __neg__(self):
        if self.is_infinity:
            return self
        return Point(self.curve, self.x, -self.y % self.curve.p)

    def __sub__(self, other):
        return self + -other

    def scale(self, pw: int):
        if self.is_infinity:
            return self
        if pw == 0:
            return Point(self.curve, None, None)
        if pw == 1:
            return self
        if pw < 0:
            return -self.scale(-pw)
        if pw % 2 == 0:
            return (self + self).scale(pw // 2)
        return self + self.scale(pw - 1)

    def serialize(self) -> bytes:
        if self.is_infinity:
            return b'1' + (0).to_bytes(32, 'big') + (1).to_bytes(32, 'big')
        return b'0' + self.x.to_bytes(32, 'big') + self.y.to_bytes(32, 'big')


p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
