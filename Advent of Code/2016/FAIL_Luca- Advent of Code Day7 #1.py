import collections

IPS = ["abba[mnop]qrst",
"abcd[bddb]xyyx",
"aaaa[qwer]tyui",
"ioxxoj[asdfgh]zxcvbn"]

supportCount = 0
insideBracket = False
done = False
bB = ""
wB = ""

for w in IPS:
    print(w)
    bB = str(((((w.split("["))[1]).split("]"))[0]))
    wB = str(((w.split("["))[0]) + ((w.split("]"))[1]))
    #print(bB)
    #print(wB)
    
    for i in range(len(w) - 4):
        
        for i in range(len(bB) - 3):
            if str(str(bB[i + 1]) + str(bB[i])) == str(str(bB[i + 2]) + str(bB[i + 3])):
                if not (str(bB[i + 1]) == str(bB[i])):
                    print("inside double")
                    done = True
                    
        if done == False:
            if str(str(wB[i + 1]) + str(wB[i])) == str(str(wB[i + 2]) + str(wB[i + 3])):
                if str(wB[i + 1]) != str(wB[i]):
                    print("match")
                    supportCount += 1
                    done = True

        if done == True:
            break


    done = False

print(supportCount)

                        
                    

        

                
    
