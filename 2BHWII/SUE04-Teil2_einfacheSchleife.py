#for-Schleife

#for i in range(10):           # Für jedes i in range(10) (range = Bereich). range(10)  -> 0, 1, 2, 3, 4, 5, 6, 7, ,8 ,9, 10
    #print(i)                  # printe den Wert i in das Terminal

idiotwerdasliestSpaß = int(input('Gib Zahl>'))      # idiotwerdasliestSpaß = n

summe = 0                   
for i in range (idiotwerdasliestSpaß + 1):        # Für jeden Wert i im Bereich 1, 2, 3 
    summe = summe + i                          # neue Summe ist die alte Summe + Wert i -> Inkrementor
summ = idiotwerdasliestSpaß * (idiotwerdasliestSpaß + 1) / 2 
print(summe) 
print(summ)
# 1: i = 1 | summe = 0 | summe = summe + i = 0 + 1 = 1 -> summe = 1
# 2: i = 2 | summe = 0 | summe = summe + i = 1 + 2 = 3 -> summe = 3
# 3: i = 3 | summe = 0 | summe = summe + i = 3 + 3 = 6 -> summe = 6
# 4: i = 4 | summe = 0 | summe = summe + i = 6 + 4 = 6 -> summe = 10


