import base64
user = "A"
msg = "N"
user_ascii = ord(user)
msg_ascii = ord(msg)
print(user_ascii)
pw_ascii=user_ascii^msg_ascii
pw_char = str(pw_ascii)
print(pw_char)
print(base64.b64encode(pw_char.encode()).decode())
