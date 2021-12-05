instructions = ["rect 3x2",
                "rotate column x=1 by 1",
                "rotate row y=0 by 4",
                "rotate column x=1 by 1"]

#..................................................
#..................................................
#..................................................
#..................................................
#..................................................
#..................................................

lightMap = []
ledsOn = 0


for i in range(6):
    for i in range(50):
        lightMap.append(".")
    lightMap.append(" ")

print(lightMap)
print(lightMap[50])

for w in instructions:
    if "rect" in w:
        for i in range(int(w[-1])):
           w[0:int(w[-3])] = str("#"*int(int(w[-3])-1))
           print(lightMap)
    #if "rotate column x" in w:
        
    #if "rotate column y" in w:
        
    #if "rotate row x" in w:
        
    #if "rotate row y" in w:
        
    
