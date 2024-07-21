import base64
import hashlib
import hmac

sk = 'ABCDEFGHIJKLMNOP'
sk_bytes = base64.b32decode(sk)
d = 6
counter = 0
hmac_sha1 = hmac.new(sk_bytes, str(counter).encode(), hashlib.sha1)





