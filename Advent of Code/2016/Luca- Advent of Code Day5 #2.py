import hashlib

#0000043e8f3f991deb83a48397ae1e7e

ID = "ugkcyxxp"
code = [0, 0, 0, 0, 0, 0, 0, 0]
temp = ""
number = 0
positionsFilled = []

print("This will take like 3 minutes. You have been warned!")

while len(positionsFilled) != 8:
    temp = hashlib.md5()
    temp.update((str(ID)+str(number)).encode('utf-8'))
    temp = str(temp.hexdigest())
    if temp[:5] == "00000":
        if temp[5].isalpha() == False:
            #print("false")
            if str(temp[5]) not in positionsFilled:
                if int(temp[5]) <= 7:
                    #print("False")
                    positionsFilled.append("{}".format(temp[5]))
                    code[int(temp[5])] = ("{}".format(temp[6]))
                    #print(temp)
                    #print(code)
                    #print(positionsFilled)
                    #print(number)

    number += 1

print("Your code is...")
print("".join(code))

    

