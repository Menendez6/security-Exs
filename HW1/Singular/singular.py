import ec
import random

a = 1729
b = 19904280025191531747281460031843416517381455437060637272956641558324120258138
curve = ec.Curve(ec.p, a, b)
G = ec.Point(curve, 420, 23803119964091633611047049209350032552964054893083423945742997504857389289134)

"""
The game that you will be playing against.
The challenger will generate a random public key pk = sk * G.
Your task is to recover sk.
Of course, you could access it directly, but that would defeat the point...
"""
class Challenger:
    def __init__(self):
        self._sk = random.randint(0, 2**128)
        self.pk = G.scale(self._sk)

    def get_pk(self):
        return self.pk

    def submit(self, sk):
        if sk == self._sk:
            print('Correct!')
        else:
            print('Nah!')
            exit(-1)
 
if __name__ == '__main__':
    challenger = Challenger()
    # Your code here
