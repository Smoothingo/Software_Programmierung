# Taschenrechner - 0.1.12.2022
# 
zahl1 = float(input("Gib erste Zahl>")) # eingabe der ersten Zahl inkl umwandlung str-> float
operator = input(" Gib Rechenoperator")
zahl2 = float(input("Gib zweite Zahl>")) # eingabe der ersten Zahl inkl umwandlung str-> float

print(zahl1, operator, zahl2)         # ausgabe der werte die geschrieben wurden
 # plus und minus               
if operator == "+":                       # summe zahl1 und zahl2
    sum = zahl1 + zahl2                   # -> hier wird addiert
    print(sum)                            # -> ausgabe der Summe

elif operator == "-":                      # differenz aus zahl1 und zahl2
    differenz = zahl1 - zahl2
    print(differenz)

elif operator == "/":
    idiotenzahl = zahl1 / zahl2
    print(idiotenzahl)

elif operator == "*":
    dummezahl = zahl1 * zahl2
    print(dummezahl)

elif operator == "**":
    komischezahl = zahl1 ** zahl2 
    print(komischezahl)
    
else:
    print("falscher Operator")
    

    

