import secrets
import math
import utils
from functools import reduce


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
    
    return ((n, e), d)

"""
The challenger of this game.
You are not supposed to modify this class, nor to access its private members.
"""
class Challenger:
    def __init__(self):
        pk, d = generate_keypair()
        n, e = pk
        self.n = n
        self.e = e
        self.__secret = secrets.randbelow(n)
        self.__d = d
        # Encryption of the secret under RSA
        self.ciphertext = pow(self.__secret, e, n)
    
    """
    Given a message, returns its decryption.
    """
    def decrypt(self, m):
        m = m % self.n
        if m == self.ciphertext:
            return 'Nice try...'
        return pow(m, self.__d, self.n)

    """
    Once you are convinced, use this to submit your answer.
    """
    def submit(self, secret):
        if secret == self.__secret:
            print('Correct!')
        else:
            print('Nah!')
            exit(-1)
    



if __name__ == '__main__':
    challenger = Challenger()
    # Write your code here
    #Dividimos m en dos mensajes, uno de valor 1 y el otro lo sacamos
    print(challenger.n)
    print(1.5**challenger.e)

          



