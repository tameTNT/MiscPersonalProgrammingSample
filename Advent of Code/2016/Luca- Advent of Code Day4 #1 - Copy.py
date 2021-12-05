import collections
import operator

codes = list(open("Day4_Input_Copy.txt"))
for i in range(len(codes)):
    codes[i] = codes[i].rstrip()

#practice = ["aaaaa-bbb-z-y-x-123[abxyz]",
#"a-b-c-d-e-f-g-h-987[abcde]",
#"not-a-real-room-404[oarel]",
#"totally-real-room-200[decoy]"]

sectorID = 0
realRooms = 0
frequencyCount = []
tempStore = ""
rooms = []

def codeCheck(ID, No):
    global frequencyCount
    global tempStore
    global realRooms
    global sectorID

    #Stores the count of the values up to last 10 (checksum and ID) from the current room name
    tempStore = str(collections.Counter((ID[No])[:-10]))
    #print(tempStore)

    for i in range(round(len(tempStore)/8-1)):
        if tempStore[(i+1)*8+2].isalpha() == True:
            frequencyCount.append("{}{}".format(tempStore[(i+1)*8+6], tempStore[(i+1)*8+2]))

    #print(frequencyCount)  
    #frequencyCount.sort(key = operator.itemgetter(1, 0))
    frequencyCount = sorted(sorted(frequencyCount, key = lambda x : x[1]), key = lambda x : x[0], reverse = True)
    #print(frequencyCount)
    
    if str((frequencyCount[0])[1]+(frequencyCount[1])[1]+(frequencyCount[2])[1]+(frequencyCount[3])[1]+(frequencyCount[4])[1]) == str((ID[No])[-6:-1]):
        realRooms += 1
        sectorID += int((ID[No])[-10:-7])
        rooms.append(ID[No])
    
    tempStore = ""
    frequencyCount = []

for i in range(len(codes)):
    codeCheck(codes, i)

print(sectorID)
print(realRooms)
print("\n".join(rooms))
print(frequencyCount)
                              
