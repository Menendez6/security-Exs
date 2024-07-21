import ec
import secrets
import hashlib
import secrets

# We are using a smaller entropy than usual to make the game easier
# My EC library was slower than what it should have been...
entropy = 16

# Generates a Schnorr keypair
def keygen():
    sk = secrets.randbelow(ec.n)
    pk = ec.G.scale(sk)
    return pk, sk

# Given a secret key and a message, returns a signature
def sign(sk, m: bytes):
    r = secrets.randbelow(2**entropy)
    R = ec.G.scale(r) 
    c = int.from_bytes(hashlib.sha256(R.serialize() + m).digest(), 'big') % ec.n
    s = (r - sk * c) % ec.n
    return (s, c)

# Verifies a given signature
def verify(pk, m: bytes, sig):
    s, c = sig
    R = ec.G.scale(s) + pk.scale(c)
    c_prime = int.from_bytes(hashlib.sha256(R.serialize() + m).digest(), 'big') % ec.n
    return c == c_prime

"""
This is the security game you will be playing against.
You are not supposed to access the private key directly (as that defeats the purpose of the game).
You will have access to the public key, and to a signature oracle (given a message, it will return a signature).
Your task is to recover the secret key of the scheme.
"""
class Game:
    def __init__(self) -> None:
        pk, sk = keygen()
        self.pk = pk
        self._sk = sk

    """
    Signature oracle
    """
    def get_signature(self, m: bytes):
        return sign(self._sk, m)

    """
    Checks whether the given secret key is the correct one
    """
    def submit(self, sk):
        return self._sk == sk
    

if __name__ == '__main__':
    game = Game()

    # Your code here
    sk = None

    def attack():
        m0 = b'hi'
        m1 = b'there'
        
        sig_m0 = []
        sig_m1 = []
        print('Signature generation')
        for _ in range(2**(entropy//2)):
            sig_m0.append(game.get_signature(m0))
            sig_m1.append(game.get_signature(m1))
        
        print('Start recovery')
        for sig0 in sig_m0:
            for sig1 in sig_m1:
                s0, c0 = sig0
                s1, c1 = sig1
                guessed_sk = (s0 - s1) * pow(c1 - c0, -1, ec.n) % ec.n
                if game.pk == ec.G.scale(guessed_sk):
                    return guessed_sk
        return None


    while sk is None:
        sk = attack()

    assert(game.submit(sk)) # If this assert passes, you won the game!
