import secrets
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
        self._secret = secrets.randbelow(n)
        self._d = d
        # Encryption of the secret under RSA
        self.ciphertext = pow(self._secret, e, n)
    
    """
    Given a message, returns its decryption.
    """
    def decrypt(self, m):
        m = m % self.n
        if m == self.ciphertext:
            return 'Nice try...'
        return pow(m, self._d, self.n)

    """
    Once you are convinced, use this to submit your answer.
    """
    def submit(self, secret):
        if secret == self._secret:
            print('Correct!')
        else:
            print('Nah!')
            exit(-1)
    

if __name__ == '__main__':
    challenger = Challenger()
    # Write your code here
    new = (challenger.ciphertext * pow(2, challenger.e, challenger.n)) % challenger.n
    dec = challenger.decrypt(new)
    challenger.submit((dec * pow(2, -1, challenger.n)) % challenger.n)

