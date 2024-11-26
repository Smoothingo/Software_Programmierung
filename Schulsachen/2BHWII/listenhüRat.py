name = (input("SCHREIB>"))              #Name
vornamen_buchstaben = [] #vorname
nachnamen_buchstaben = [] #nachname

vornamen = ""        
nachname = ""

for i in range(len(name)):     # geht durch
    buchstabe = name[i]        # buchstabe definiert
    if buchstabe == " ":      #sucht nach leerzeichen
        continue
    if i < name.index(" "):     #sorgt für ausführung
        vornamen_buchstaben.append("ö" if buchstabe in "aeiouAUEIOU" else buchstabe)        # hängt ö dran an vornamen
    else:
        nachnamen_buchstaben.append("ö" if buchstabe in "aeiouAUEIOU" else buchstabe)            # hangt ö dran an nachnamen

vornamen = "".join(vornamen_buchstaben)        # fügt zusammen vornamen
nachname = "".join(nachnamen_buchstaben)         #fügt zusammen vornamen
 
name = vornamen + " " + nachname   # fügt ganzen namen zusammen
print(name)

