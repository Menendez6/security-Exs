import string
import hashlib
import time
import itertools


lower_case = string.ascii_lowercase
digits = string.digits
charset = lower_case+digits
start_time = time.perf_counter()
passwords = []

for comb in itertools.product(charset, repeat=8):
    password = "".join(comb)
    h = hashlib.sha256(password.encode())
    digest = h.hexdigest()
    if digest in all_hashes:
        print("{} === {}".format(digest, password))
        all_hashes.remove(digest)
    else:
        print(password, end="\r")

