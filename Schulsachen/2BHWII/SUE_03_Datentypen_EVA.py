# SUE03 am 24.11.2022, Thema: Datentypen

intVar1 = 1    # Integer "Ganze Zahl"
strVar1 = "1"  # String  "Zeichen Kette" -> Wichtig: Anführungszeichen "" oder ''

intVar2 = 2
strVar2 = "2"

print(intVar1 + intVar2) # Ausgabe der Integer-Addition im Terminal
print(strVar1 + strVar2) # Ausgabe der String-Addition im Terminal
#print(intVar1 + intVar2) <- TypeError: + nicht für str + int

strhello = "Hello"
strWorld = "World"
strhelloworld = strhello + " " + strWorld
print(strhelloworld)

# type() -> gibt den Datentyp zurück
print(type(strVar1))
print(type(intVar1))

