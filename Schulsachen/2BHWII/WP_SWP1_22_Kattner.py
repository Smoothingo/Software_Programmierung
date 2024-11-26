

strin = (input("Gib einen Zahlenwert zwischen 1 und 100 ein>")) # EIngabe der Zahl
intin = int(strin)         #wird in int umgewandelt
intcounter = 0

for i in range(intin):                       # Verarbeitung schleife um alle ergebnise in range zu printen
    print(i)
    intcounter = intcounter + i
print("Ergebnis = ", intcounter)             # Ausgabe endergebnis wird geprintet
