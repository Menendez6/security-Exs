import random

def is_prime(n, k=128):
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, r, n)
        
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            
            if x != n - 1:
                return False
    
    return True

def generate_prime(bits):
    while True:
        p = random.randrange(2**(bits-1), 2**bits)
        if is_prime(p):
            return p


