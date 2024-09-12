# Fortsetzung: EVA
# E ..... Eingabe
# V ..... Verarbeitung
# A ..... Ausgabe, z.B. print() -> Ausgabe in das Terminal



strEingabe = input("Gib eine Zahl ein> ")
print(strEingabe, type(strEingabe))
# EingabeDoppelt = strEingabe * 200 -> 200x den selben string hintereinander
# print(eingabeDoppelt)

fltEingabe = float(strEingabe) # Versuche aus str ein float zu machen; int() str() bool()
print(fltEingabe)

strOperator = print("Gib einen Operater an")

if strOperator == "+":        # == Vergleichende Ist-gleich ... strOperator + ist
    print("Du hast addiert")  # Einrücken -> gehört zum "if" ... dann mach das
else:
    print("Du hast nicht addiert") # Einrücken -> gehört zum "else" ... mach dies
