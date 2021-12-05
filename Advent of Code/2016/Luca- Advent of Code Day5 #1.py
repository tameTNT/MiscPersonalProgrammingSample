import hashlib

ID = "ugkcyxxp"
code = []
temp = ""
number = 0

print("This will take over a minute. You have been warned!")

while len(code) != 8:
    temp = hashlib.md5()
    temp.update((str(ID)+str(number)).encode('utf-8'))
    temp = str(temp.hexdigest())
    if temp[:5] == "00000":
        code.append(temp[5])
        #print(code)
    number += 1

print("Your code is...")
print("".join(code))

    

