import math
import hashlib
import string
import sys
import pickle as pkl
import multiprocessing
from typing import Dict  # for type hinting

SIZE_PASSWORDS = 8
NUM_ROWS = 10000000
NUM_REDUCTIONS = 1000
NUM_THREADS = 7


end_to_start_matching: Dict[str, str] = dict()


def hashing(plaintext: str):
    """Hashes a plaintext string with SHA256."""
    return hashlib.sha256(plaintext.encode()).hexdigest()


def reduction(h: str, i: int):
    """Reduce a hash to the set of considered passwords.

    Takes the hash, and reads it as an integer (in base 16).
    Then, converts that big integer to a representation
    (char by char) in base N (with N = size of charset).
    Create different reductions functions by adding an integer
    (notably, the "column number" of the function).

    Args:
        h (str) : hash to reduce (in hex representation)

    Returns:
        str : a reduction (in passwords set) of the hash
    """
    corresp_int = int(h, 16) + i
    chars = string.ascii_lowercase + string.digits
    chars_len = len(chars)
    pwd = ""
    while len(pwd) < SIZE_PASSWORDS:
        pwd = pwd + chars[corresp_int % chars_len]
        corresp_int = corresp_int // chars_len
    return pwd


def compute_row(row_num: int):
    """Compute one row of a rainbow table.

    Starts from the reduction of the row number, and then computes
    all hashes and reductions, and yields the first and last plaintexts.

    Args:
        row_num (int): Number of the row; must be unique.

    Returns:
        tuple: Tuple of the start and end of the row.
    """
    if row_num % 10 == 0:
        print(row_num, end="\r")
    init_plaintext = reduction(hex(row_num), 0)
    plaintext = init_plaintext
    for i in range(NUM_REDUCTIONS):
        h = hashing(plaintext)
        plaintext = reduction(h, i)
    return (init_plaintext, plaintext)


def build(filename):
    """Build a rainbow table, and write to to `filename`.

    Args:
        filename (str): Filename where to dump the table.
    """
    pool = multiprocessing.Pool(processes=NUM_THREADS)
    pool_res = pool.imap_unordered(compute_row, range(NUM_ROWS), 1000)

    start_end_matching = dict()
    for start, end in pool_res:
        start_end_matching[end] = start

    # dump table
    with open(filename, "wb") as f:
        pkl.dump(start_end_matching, f)


def crack_hash(target_hash):
    """Crack one hash.

    Function to be passed to a worker for a parallelized implementation
    of the cracking of multiple hashes.

    Args:
        target_hash (str): target hash

    Returns:
        tuple: A tuple (hash, preimage) if cracked, or None if not cracked.
    """
    global end_to_start_matching
    for i in range(NUM_REDUCTIONS-1, -1, -1):
        h = target_hash
        for j in range(i, NUM_REDUCTIONS):
            plaintext = reduction(h, j)
            h = hashing(plaintext)
        if plaintext in end_to_start_matching:
            unhash = find_preimage(target_hash,
                                   end_to_start_matching[plaintext])
            if unhash is not None:
                # print("\tFound reverse hash: {}".format(unhash))
                return target_hash, unhash


def crack_file(hashes_filename, table_filename):
    """Look for the target_hash in the rainbow table.

    Read the rainbow table with the provided filename; Then, look for the hash
    in each column. If the end plaintext matches, look for the hash
    in the row, by calling `find_preimage`.

    Args:
        target_hash (str): Hash we are looking for
        filename (str): Filename (relative or absolute) of the rainbow table.
    """
    print("Loading rainbow table")
    global end_to_start_matching
    with open(table_filename, "rb") as f:
        end_to_start_matching = pkl.load(f)
    print("Loading hashes")
    with open(hashes_filename, "r") as f:
        all_hashes = [r.strip() for r in f.readlines()]
    print("Hacking initiated!")
    pool = multiprocessing.Pool(processes=NUM_THREADS)
    pool_res = pool.imap_unordered(crack_hash, all_hashes)
    cracked = total = 0
    for r in pool_res:
        if r is not None:
            cracked += 1
            print("{} ({}/{}, {}% success rate)".format(r, cracked, total, 100*cracked/total))
        total += 1


def find_preimage(target_hash: str, start_text: str):
    """Look for `target_hash` in row starting by `start_text`.

    Args:
        target_hash (str): The hash we are looking for
        start_text (str): The beginning/root of the row

    Returns:
        str/None: the preimage of the hash, or None if not found.
    """
    # print("Looking for preimage of '{}', in chain starting with {}"
    #       .format(target_hash, start_text))
    plaintext = start_text
    for i in range(NUM_REDUCTIONS):
        h = hashing(plaintext)
        if h == target_hash:
            return plaintext
        plaintext = reduction(h, i)
    # print("Chain did not match\n")
    return None


def success_rate(m: int, t: int):
    """Compute success rate of a given table.

    Args:
        m (int): number of rows
        t (int): number of columns
    """
    N = 36**8  # change for different passwords space
    all_m = [float(m)]
    for _ in range(t):
        all_m.append(N*(1-math.exp(all_m[-1]/N)))

    prod = 1.0
    for mi in all_m:
        prod = prod*(1-mi/N)
    print(1-prod)


if __name__ == "__main__":
    if len(sys.argv) not in [3, 4]:
        raise ValueError("Usage: '{pname} build <filename> or "
                         "'{pname} crack <hashes_filename> <table_filename>")
    if sys.argv[1].lower() == "build":
        build(sys.argv[2])
    elif sys.argv[1].lower() == "crack":
        target_hash = sys.argv[2]
        table_filename = sys.argv[3]
        crack_file(target_hash, table_filename)
    elif sys.argv[1].lower() == "success":
        success_rate(int(sys.argv[2]), int(sys.argv[3]))
    else:
        raise ValueError("Usage: '{pname} build <filename> or "
                         "'{pname} crack <hashes_filename> <table_filename>")
