"""This file generates random passwords and their hashes.

Matches  the requirements of HW3.EX2. Writes them to two files.
"""
import hashlib
import random
import string

SIZE_PWD = 8
NUMBER_PASSWORDS = 10000
charset = string.ascii_lowercase + string.digits

random.seed(42)
hashes = []
matches = []
for _ in range(NUMBER_PASSWORDS):
    pwd = "".join(random.choice(charset) for _ in range(SIZE_PWD))
    h = hashlib.sha256(pwd.encode())
    hashes.append(h.hexdigest() + "\n")
    matches.append("{},{}\n".format(pwd, h.hexdigest()))

with open("dump_hashes.txt", "w") as f:
    f.writelines(hashes)

with open("dump_matches.txt", "w") as f:
    f.writelines(matches)
