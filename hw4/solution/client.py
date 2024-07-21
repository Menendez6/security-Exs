import websockets
import asyncio
import os
import hashlib
EMAIL = "your.email@epfl.ch"
PASSWORD = "correct horse battery staple"
N = int("EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C256576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376435B9FC61D2FC0EB06E3", 16)
g = 2
NUMBER_LENGTH = 32


def itob(x):
    """Transform an int to a binary hex.

    Args:
        x (int): Integer to transform

    Returns:
        binary string: Binary encoding of the hex representation
    """
    return format(x, "x").encode()


async def srp():
    uri = "ws://127.0.0.1:5000"
    async with websockets.connect(uri) as websocket:
        await websocket.send(EMAIL.encode())

        salt_hex = await websocket.recv()
        salt_int = int(salt_hex, 16)
        salt_bin = itob(salt_int)
        # alternatively: salt_bin = salt_hex.encode()
        print("[Client] received salt: " + str(salt_int))

        a = int.from_bytes(os.urandom(NUMBER_LENGTH), "big")
        A = pow(g, a, N)
        A_hex = itob(A)
        print("[Client] A_hex : {}".format(A_hex))
        await websocket.send(A_hex)

        B_hex = await websocket.recv()
        B = int(B_hex, 16)
        print("[Client] B : {}".format(B))

        h = hashlib.sha256()
        h.update(itob(A))
        h.update(itob(B))

        u = int(h.hexdigest(), 16)
        print("[Client] u : {}".format(u))

        inner = hashlib.sha256()
        inner.update(EMAIL.encode())
        inner.update(b":")
        inner.update(PASSWORD.encode())
        print('[Client] H(U || ":" || PASSWORD): {}'.format(inner.hexdigest()))

        outer = hashlib.sha256()
        outer.update(salt_bin)
        outer.update(inner.hexdigest().encode())
        print('[Client] H(salt || H(U || ":" || PASSWORD)): {}'.format(
            outer.hexdigest()))

        x = int(outer.hexdigest(), 16)
        print("[Client] x : {}".format(x))

        S = pow(B - pow(g, x, N), (a + u * x), N)
        print("[Client] Secret : " + str(S))

        # h is the same as above, the first 3 lines here are redundant
        h = hashlib.sha256()
        h.update(itob(A))
        h.update(itob(B))
        h.update(itob(S))

        await websocket.send(h.hexdigest().encode())

        resp = await websocket.recv()
        print("Response: {}".format(resp))

asyncio.get_event_loop().run_until_complete(srp())
