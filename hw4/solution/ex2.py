import math
import hashlib
import string
import sys
import pickle as pkl


SIZE_PASSWORDS = 8
NUM_ROWS = 10000000
NUM_REDUCTIONS = 1000


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


def build(filename):
    """Build a rainbow table, and write to to `filename`.

    Args:
        filename (str): Filename where to dump the table.
    """
    end_to_start_matching = dict()

    for row_num in range(NUM_ROWS):
        init_plaintext = reduction(hex(row_num), 0)
        plaintext = init_plaintext
        # compute all iterations for the row
        for i in range(NUM_REDUCTIONS):
            h = hashing(plaintext)
            plaintext = reduction(h, i)
        # finally, only store the matching start-end
        end_to_start_matching[plaintext] = init_plaintext

    # dump table
    with open(filename, "wb") as f:
        pkl.dump(end_to_start_matching, f)


def crack_hash(target_hash, table_filename):
    """Look for the target_hash in the rainbow table.

    Read the rainbow table with the provided filename; Then, look for the hash
    in each column. If the end plaintext matches, look for the hash
    in the row, by calling `find_preimage`.

    Args:
        target_hash (str): Hash we are looking for
        filename (str): Filename (relative or absolute) of the rainbow table.
    """
    print("Loading rainbow table")
    with open(table_filename, "rb") as f:
        end_to_start_matching = pkl.load(f)

    for i in range(NUM_REDUCTIONS-1, -1, -1):
        h = target_hash
        for j in range(i, NUM_REDUCTIONS):
            plaintext = reduction(h, j)
            h = hashing(plaintext)
        if plaintext in end_to_start_matching:
            preimage = find_preimage(target_hash,
                                     end_to_start_matching[plaintext])
            if preimage is not None:
                print("Found reverse hash of {}: {}"
                      .format(target_hash, preimage))


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
        all_m.append(N*(1-math.exp(-all_m[-1]/N)))

    prod = 1.0
    for mi in all_m:
        prod = prod*(1-mi/N)
    print("{}%".format(100*(1-prod)))


if __name__ == "__main__":
    """Ease the use of the program.

    When calling, you have 3 possible arguments:
        * build <filename>, will build the table and dump it to <filename>
        * crack <target_hash> <filename> will try to crack a the target_hash
            using the rainbow table stored at <filename>
        * success <num_rows> <num_cols>, will compute the theoretical success
            rate for these numbers of cols/rows.
    """
    if len(sys.argv) not in [3, 4]:
        # not correct number of arguments (crude check)
        raise Exception("Usage: '{pname} build <filename> or "
                        "'{pname} crack <target_hash> <table_filename>")
    if sys.argv[1].lower() == "build":
        # Build the table
        build(sys.argv[2])
    elif sys.argv[1].lower() == "crack":
        # crack a list of hashes
        target_hash = sys.argv[2]
        table_filename = sys.argv[3]
        crack_hash(target_hash, table_filename)
    elif sys.argv[1].lower() == "success":
        # compute success rate
        success_rate(int(sys.argv[2]), int(sys.argv[3]))
    else:
        raise Exception("Usage: '{pname} build <filename> or "
                        "'{pname} crack <target_hash> <table_filename>")
