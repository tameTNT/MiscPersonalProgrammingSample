input = ["UULLULLUULLLURDLDUURRDRRLDURDULLRURDUDULLLUULURURLRDRRRRULDRUULLLLUUDURDULDRRDRUDLRRLDLUDLDDRURURUURRRDDDLLRUDURDULUULLRRULLRULDUDRDRLDLURURUDDUDLURUDUDURLURURRURLUDDRURRDLUURLLRURRDUDLULULUDULDLLRRRDLRDLDUDRDDDRRUURRRRRUURRDRRDLURDRRURDLLUULULLRURDLDDDRRLLRRUURULURUUDDLRRUDDRURUUDLRLRDLRURRRDULLDLRUDDUULRDULURUURDULUDLLRRLDDLRDLRUDRLDDRLRRRDURDULLRRRDRRLUURURDRRDRRLDLUDURURLDUURDRUDRDDRLDRRLDLURURULLUURUDUUDLRLL", 
"LLLULLULDDULRLLURLLLRUUDDLRUULRLULLDLLRRDRLRLRLLDRUUURULDRDDLUDLLDUDULLLRLULLLRULDRDRUDLLRLRLLUDULRRRLDRUULDDULLDULULLUDUDLDRDURDLDLLDUDRRRDLUURRUURULLURLDURLRRLLDDUUULDRLUUDUDLURLULUDURRDRLLDDDDDRRULLRLDULULDDRUURRDLUDDDUDURDDRDRULULLLLUURDURUUUULUDLRURRULRDDRURURLLRLUUDUUURDLLDDLUDRLLLUDLLLLULRLURDRRRDUUDLLDLDDDURRDDRURUURDDRURRLDDDURDLLUURUUULRLUURRUDRLLDLURDUDRLULDLRLULULUDDLRDUDRUDLUULUULDURDRRRRLRULLUDRDDRDLDUDRDRRLDLLLLUDDLRULDLLDDUULDDRRULRRUURUDRDURLLLDDUUDRUUDLULLDR", 
"UDUUULLDDDDLUDLDULRLRDLULLDDRULDURRLURRUDLRRUDURRDUDRRRUULRLLRLUDLDRRDUURDDRDRDUUUDUDLDLLRRLUURLUUUDDDUURLULURRLURRRDRDURURUDRLRUURUDRUDDDRDRDLDRDURDLDRRDUUDLLURLDDURRRLULDRDRLLRLLLRURLDURDRLDRUURRLDLDRLDDDRLDLRLDURURLLLLDDRDUDLRULULLRDDLLUDRDRRLUUULDRLDURURDUDURLLDRRDUULDUUDLLDDRUUULRRULDDUDRDRLRULUUDUURULLDLLURLRRLDDDLLDRRDDRLDDLURRUDURULUDLLLDUDDLDLDLRUDUDRDUDDLDDLDULURDDUDRRUUURLDUURULLRLULUURLLLLDUUDURUUDUULULDRULRLRDULDLLURDLRUUUDDURLLLLDUDRLUUDUDRRURURRDRDDRULDLRLURDLLRRDRUUUURLDRURDUUDLDURUDDLRDDDDURRLRLUDRRDDURDDRLDDLLRR", 
"ULDRUDURUDULLUDUDURLDLLRRULRRULRUDLULLLDRULLDURUULDDURDUUDLRDRUDUDDLDRDLUULRRDLRUULULUUUDUUDDRDRLLULLRRDLRRLUDRLULLUUUUURRDURLLRURRULLLRLURRULRDUURRLDDRRDRLULDDRRDRLULLRDLRRURUDURULRLUDRUDLUDDDUDUDDUDLLRDLLDRURULUDRLRRULRDDDDDRLDLRRLUUDLUURRDURRDLDLDUDRLULLULRLDRDUDLRULLULLRLDDRURLLLRLDDDLLLRURDDDLLUDLDLRLUULLLRULDRRDUDLRRDDULRLLDUURLLLLLDRULDRLLLUURDURRULURLDDLRRUDULUURRLULRDRDDLULULRRURLDLRRRUDURURDURDULURULLRLDD", 
"DURLRRRDRULDLULUDULUURURRLULUDLURURDDURULLRRUUDLRURLDLRUDULDLLRRULLLLRRLRUULDLDLLRDUDLLRLULRLLUUULULRDLDLRRURLUDDRRLUUDDRRUDDRRURLRRULLDDULLLURRULUDLRRRURRULRLLLRULLRRURDRLURULLDULRLLLULLRLRLLLDRRRRDDDDDDULUUDUDULRURDRUDRLUULURDURLURRDRRRRDRRLLLLUDLRRDURURLLULUDDLRLRLRRUURLLURLDUULLRRDURRULRULURLLLRLUURRULLLURDDDRURDUDDULLRULUUUDDRURUUDUURURRDRURDUDRLLRRULURUDLDURLDLRRRRLLUURRLULDDDUUUURUULDLDRLDUDULDRRULDRDULURRUURDU"]

keypadNumber = 5
row = 3
time = 0

#Keypad Layout
#  1
# 234
#56789
# ABC
#  D

def negativeCheck(action):
    global keypadNumber
    global row
    
    if action == "U":
        if row == 1:
            return
        elif row == 2:
            if keypadNumber != 3:
                return
            else:
                keypadNumber -= 2
                row -= 1
        elif row == 3:
            if keypadNumber == 5:
                return
            elif keypadNumber == 9:
                return
            else:
                keypadNumber -= 4
                row -= 1
        elif row == 4:
                keypadNumber -= 4
                row -= 1
        if row == 5:
            keypadNumber -= 2
            row -= 1
            
    elif action == "D":
        if row == 1:
            keypadNumber += 2
            row += 1
        elif row == 2:
            keypadNumber += 4
            row += 1
        elif row == 3:
            if keypadNumber == 5:
                return
            elif keypadNumber == 9:
                return
            else:
                keypadNumber += 4
                row += 1
        elif row == 4:
            if keypadNumber != 11:
                return
            else:
                keypadNumber += 2
                row += 1
        if row == 5:
            return
        
    elif action == "L":
        if row == 1:
            return
        elif row == 2:
            if keypadNumber - 1 <= 1:
                return
            else:
                keypadNumber -= 1
        elif row == 3:
            if keypadNumber - 1 <= 4:
                return
            else:
                keypadNumber -= 1
        elif row == 4:
            if keypadNumber - 1 <= 9:
                return
            else:
                keypadNumber -= 1
        elif row == 5:
            return
        
    elif action == "R":
        if row == 1:
            return
        elif row == 2:
            if keypadNumber + 1 >= 5:
                return
            else:
                keypadNumber += 1
        elif row == 3:
            if keypadNumber + 1 >= 10:
                return
            else:
                keypadNumber += 1
        elif row == 4:
            if keypadNumber + 1 >= 13:
                return
            else:
                keypadNumber += 1
        elif row == 5:
            return
        

for w in input:
    for i in range(len(w)):
        if w[i:i + 1] == "U":
            negativeCheck("U")
        elif w[i:i + 1] == "D":
            negativeCheck("D")
        elif w[i:i + 1] == "L":
            negativeCheck("L")
        elif w[i:i + 1] == "R":
            negativeCheck("R")
        #print(keypadNumber)
        
    if keypadNumber == 10:
        print("Keypad Number {} is... A".format(time))
    elif keypadNumber == 11:
        print("Keypad Number {} is... B".format(time))
    elif keypadNumber == 12:
        print("Keypad Number {} is... C".format(time))
    elif keypadNumber == 13:
        print("Keypad Number {} is... D".format(time))
    else:
        print("Keypad Number {} is... ".format(time) + str(keypadNumber))

    time += 1
    
            

        
