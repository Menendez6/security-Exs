import random
import math
import utils

# Generates a RSA keypair
def generate_keypair():
    e = 65537
    while True:
        p = utils.generate_prime(1024)
        q = utils.generate_prime(1024)
        phi = (p - 1) * (q - 1)
        if math.gcd(e, phi) == 1:
            break
        
    n = p * q
    d = pow(e, -1, phi)

    assert (e * d) % phi == 1
    
    return ((n, e), (n, d))

"""
The challenger of the IND-CPA game.
You are not supposed to modify this class, nor to access its private members.
"""
class Challenger:
    def __init__(self):
        pk = generate_keypair()[0]
        self._b = random.randint(0, 1)
        self.pk = pk
    
    """
    Given two messages m0 and m1, return the encryption of m0 if b = 0, or the encryption of m1 if b = 1.
    """
    def lor(self, m0, m1):
        n, e = self.pk
        return pow(m1 if self._b else m0, e, n)

    """
    Once you are convinced, use this to submit your answer.
    """
    def submit(self, b):
        if b == self._b:
            print('Correct!')
        else:
            print('Nah!')
            exit(-1)
    

if __name__ == '__main__':
    challenger = Challenger()
    # Write your code here
    challenger.submit(0 if challenger.lor(0, 1) == 0 else 1)
