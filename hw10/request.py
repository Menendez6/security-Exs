import requests
import time
import string

def post(token):
    before = time.time()
    resp = requests.post("http://0.0.0.0:8080/hw10/ex1",
                         json = {"token": token})
    after = time.time()

    time_diff = after-before
    #print("Token {}, request took {:.3f}"
    #      .format(token, time_diff)) # useful for debugging
    print("response is {}".format(resp.text))  # often useless
    return time_diff

TOKEN_LENGTH = 12

charset = string.digits + string.ascii_lowercase

for start_char in charset:
    token = 'b4351d395d2f'
    tdiff = post(token)
    print("Token {}, request took {:.3f}"
          .format(token, tdiff))