import hashlib
text = b"123456"
m = hashlib.new("sha256")
m.update(text)

print(m.hexdigest())

with open("rockyou.txt","r", encoding="ISO-8859-1") as file:
    lista = file.read().splitlines()
    for element in lista:
        m = hashlib.new("sha256")
        m.update(element.encode("utf-8"))
        if m.hexdigest() == "0cb7cbe18b18ee7872ebb9fe873436c71fdc820520418248166c2f584077ed72":
            print(element)
            break

#Solution = babycakes