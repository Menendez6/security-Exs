import ec
import secrets
import hashlib
import secrets

# Generates a Schnorr keypair
def keygen():
    sk = secrets.randbelow(ec.n)
    pk = ec.G.scale(sk)
    return pk, sk

# Given a secret key and a message, returns a signature
def sign(sk, m: bytes):
    r = secrets.randbelow(2**32)
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
    #Lo interesante aquí es qeu la c es un hash y se puede demostrar que con una probabilidad muy alta
    #hay dos elementos que tienen el mismo hash
    #PODEMOS OBTENER LA KEY SI LA NONCE ES LA MISMA, ES DECIR LA r tiene que ser LA MISMA
    #find the colision:
    lista_c = []
    for i in range(2**16):
        m = b"mensaje"
        s,c = game.get_signature(m)
        if c in lista_c:
            print("Colisión")
        else:
            lista_c.append(c)

    #assert(game.submit(sk)) # If this assert passes, you won the game!
