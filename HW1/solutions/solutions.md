# Exercise 1a
Two attacks, first one can note that textbook RSA always encrypts 0 to 0 and 1 to 1. This directly leads to an attack on IND-CPA. Even more generally, any encryption scheme that is deterministic (like textbook RSA or ECB) cannot be IND-CPA.
# Exercise 1b
An adversary can ask for a decryption of $2^e \cdot c$, which would correctly decrypt to $2 \cdot \mathsf{sk}$. This is because RSA is multiplicatively homomorphic.

# Exercise 2
We had to lower the entropy of the nonce since our underlying EC implementation was very inefficient. The attack aims to find a colliding pair of nonces, and extract the private key from those. Of course, this leads to the question of how to detect when a pair of nonces collide. The solution is to attempt to extract, and verify the recovered key against the public key. 

# Optional Exercises
We have decided not to release solutions for the optional exercises. Those were deliberately at an higher difficulty level, and we might be using them for future challenges or CTFs. If you are interested, come talk to me (Giacomo).
