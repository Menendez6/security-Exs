import sys
import itertools
import hashlib
import time

import multiprocessing

##################
##### PART 1a ####
##################
charset = "abcdefghijklmnopqrstuvwxyz1234567890"

all_hashes = set([
    "7c58133ee543d78a9fce240ba7a273f37511bfe6835c04e3edf66f308e9bc6e5",
    "37a2b469df9fc4d31f35f26ddc1168fe03f2361e329d92f4f2ef04af09741fb9",
    "19dbaf86488ec08ba7a824b33571ce427e318d14fc84d3d764bd21ecb29c34ca",
    "06240d77c297bb8bd727d5538a9121039911467c8bb871a935c84a5cfe8291e4",
    "f5cd3218d18978d6e5ef95dd8c2088b7cde533c217cfef4850dd4b6fa0deef72",
    "dd9ad1f17965325e4e5de2656152e8a5fce92b1c175947b485833cde0c824d64",
    "845e7c74bc1b5532fe05a1e682b9781e273498af73f401a099d324fa99121c99",
    "a6fb7de5b5e11b29bc232c5b5cd3044ca4b70f2cf421dc02b5798a7f68fc0523",
    "1035f3e1491315d6eaf53f7e9fecf3b81e00139df2720ae361868c609815039c",
    "10dccbaff60f7c6c0217692ad978b52bf036caf81bfcd90bfc9c0552181da85a"])


def part_a_main():
    begin = time.time()
    for length in range(4, 7):
        for comb in itertools.product(charset, repeat=length):
            password = "".join(comb)
            h = hashlib.sha256(password.encode())
            digest = h.hexdigest()
            if digest in all_hashes:
                print("{} === {}".format(digest, password))
                all_hashes.remove(digest)
            else:
                print(password, end="\r")
    end = time.time()
    print("Time for naïve: {:.3f}".format(end-begin))


def block_func(combination):
    password = "".join(combination)
    h = hashlib.sha256(password.encode())
    digest = h.hexdigest()
    if digest in all_hashes:
        all_hashes.remove(digest)
        print("{} === {}".format(digest, password))
        return digest


def part_a_main_parallel():
    pool = multiprocessing.Pool(processes=16)
    total_matches = []
    for length in range(4, 7):
        combinations_iterator = itertools.product(charset, repeat=length)
        total_combinations = len(charset)**length
        for i, x in enumerate(pool.imap_unordered(block_func,
                                                  combinations_iterator,
                                                  100000)):
            if x is not None:
                total_matches.append(x)
            if i % 100 == 0:
                print("{:.3f}".format(100*i/total_combinations), end="\r")
    print(len(total_matches))


##################
##### PART 1b ####
##################

all_hashes_b = set([
    "2e41f7133fd134335f566736c03cc02621a03a4d21954c3bec6a1f2807e87b8a",
    "7987d2f5f930524a31e0716314c2710c89ae849b4e51a563be67c82344bcc8da",
    "076f8c265a856303ac6ae57539140e88a3cbce2a2197b872ba6894132ccf92fb",
    "b1ea522fd21e8fe242136488428b8604b83acea430d6fcd36159973f48b1102e",
    "326e90c0d2e7073d578976d120a4071f83ce6b7bc89c16ecb215d99b3d51a29b",
    "269398301262810bdf542150a2c1b81ffe0e1282856058a0e26bda91512cfdc4",
    "4fbee71939b9a46db36a3b0feb3d04668692fa020d30909c12b6e00c2d902c31",
    "55c5a78379afce32da9d633ffe6a7a58fa06f9bbe66ba82af61838be400d624e",
    "5106610b8ac6bc9da787a89bf577e888bce9c07e09e6caaf780d2288c3ec1f0c",
    "3992b888e772681224099302a5eeb6f8cf27530f7510f0cce1f26e79fdf8ea21"
])


def modif1(p: str):
    return p.title()


def modif2(p: str):
    return p.replace("e", "3")


def modif3(p: str):
    return p.replace("o", "0")


def modif4(p: str):
    return p.replace("i", "1")


def modif_and_hash(p):
    p = p.replace("\n", "")
    all_versions = set([p])
    for comb in all_modifs_combinations:
        p_temp = p
        for modificator in comb:
            p_temp = modificator(p_temp)
        all_versions.add(p_temp)
    for version in all_versions:
        hash = hashlib.sha256(version.encode()).hexdigest()
        if hash in all_hashes_b:
            print("{} === {} (from {})".format(hash, version, p))
            return p, hash


all_modifs_combinations = set()


def part_b_main():
    dictionaries = [
        ("500-worst-passwords.txt", "utf-8"),
        ("alypaa.txt", "utf-8"),
        ("cain.txt", "utf-8"),
        ("carders.cc.txt", "latin-1"),
        ("conficker.txt", "utf-8"),
        ("english.txt", "utf-8"),
        ("elitehacker.txt", "utf-8"),
        ("facebook-pastebay.txt", "utf-8"),
        ("facebook-phished.txt", "latin-1"),
        ("faithwriters.txt", "utf-8"),
        ("file-locations.txt", "utf-8"),
        ("fuzzing-strings.txt", "utf-8"),
        ("german.txt", "latin-1"),
        ("hak5.txt", "utf-8"),
        ("honeynet.txt", "latin-1"),
        ("hotmail.txt", "utf-8"),
        ("john.txt", "utf-8"),
        ("phpbb.txt", "latin-1"),
        ("phpmyadmin-locations.txt", "latin-1"),
        ("porno.txt", "latin-1"),
        ("porn-unknown.txt", "utf-8"),
        ("singles.org.txt", "utf-8"),
        ("tuscl.txt", "latin-1"),
        ("twitter-banned.txt", "utf-8"),
        ("us_cities.txt", "utf-8"),
        ("web-extensions.txt", "utf-8"),
        ("web-mutations.txt", "utf-8"),
        ("rockyou.txt", "latin1"),
        ("crackstation.txt", "latin-1")
    ]
    all_modifs = [modif1, modif2, modif3, modif4]
    for length in range(1, len(all_modifs)+1):
        for comb in itertools.permutations(all_modifs, length):
            all_modifs_combinations.add(comb)

    for fname, encoding in dictionaries:
        print("Opening file {}".format(fname))
        file = open("Dictionaries/{}".format(fname), encoding=encoding)
        pool = multiprocessing.Pool(8)
        results = []
        for r in pool.imap_unordered(modif_and_hash, file, 10000):
            if r is not None:
                results.append(r)
        file.close()


def salt_and_hash(p):
    salts = ["b9", "be", "bc", "72", "9f", "17", "94", "7f", "2e", "24"]
    p = p.replace("\n", "")
    for s in salts:
        salted = p+s
        hash = hashlib.sha256(salted.encode()).hexdigest()
        if hash in all_hashes_c:
            print("{} === {} (salt {})".format(hash, p, s))
            return p, hash


all_hashes_c = [
    "962642e330bd50792f647c1bf71895c5990be4ebf6b3ca60332befd732aed56c",
    "8eef79d547f7a6d6a79329be3c7035f8e377f9e629cd9756936ec233969a45a3",
    "e71067887d50ce854545afdd75d10fa80b841b98bb13272cf4be7ef0619c7dab",
    "889a22781ef9b72b7689d9982bb3e22d31b6d7cc04db7571178a4496dc5ee128",
    "6a16f9c6d9542a55c1560c65f25540672db6b6e121a6ba91ee5745dabdc4f208",
    "2317603823a03507c8d7b2970229ee267d22192b8bb8760bb5fcef2cf4c09edf",
    "c6c51f8a7319a7d0985babe1b6e4f5c329403d082e05e83d7b9d0bf55876ecdc",
    "c01304fc36655dd37b5aa8ca96d34382ed9248b87650fffcd6ec70c9342bf451",
    "cff39d9be689f0fc7725a43c3bdc7f5be012c840b9db9b547e6e3c454a076fc8",
    "662ab7be194cee762494c6d725f29ef6321519035bfb15817e84342829728891"
]


def part_c_main():
    dictionaries = [
        ("500-worst-passwords.txt", "utf-8"),
        ("alypaa.txt", "utf-8"),
        ("cain.txt", "utf-8"),
        ("carders.cc.txt", "latin-1"),
        ("conficker.txt", "utf-8"),
        ("english.txt", "utf-8"),
        ("elitehacker.txt", "utf-8"),
        ("facebook-pastebay.txt", "utf-8"),
        ("facebook-phished.txt", "latin-1"),
        ("faithwriters.txt", "utf-8"),
        ("file-locations.txt", "utf-8"),
        ("fuzzing-strings.txt", "utf-8"),
        ("german.txt", "latin-1"),
        ("hak5.txt", "utf-8"),
        ("honeynet.txt", "latin-1"),
        ("hotmail.txt", "utf-8"),
        ("john.txt", "utf-8"),
        ("phpbb.txt", "latin-1"),
        ("phpmyadmin-locations.txt", "latin-1"),
        ("porno.txt", "latin-1"),
        ("porn-unknown.txt", "utf-8"),
        ("singles.org.txt", "utf-8"),
        ("tuscl.txt", "latin-1"),
        ("twitter-banned.txt", "utf-8"),
        ("us_cities.txt", "utf-8"),
        ("web-extensions.txt", "utf-8"),
        ("web-mutations.txt", "utf-8"),
        ("rockyou.txt", "latin1"),
        ("crackstation.txt", "latin-1")
    ]
    for fname, encoding in dictionaries:
        print("Opening file {}".format(fname))
        file = open("Dictionaries/{}".format(fname), encoding=encoding)
        pool = multiprocessing.Pool(8)
        results = []
        for r in pool.imap_unordered(salt_and_hash, file, 10000):
            if r is not None:
                results.append(r)
        file.close()


if __name__ == "__main__":
    # part_a_main() # SLOW!
    part_a_main_parallel()
    part_b_main()
    part_c_main()
