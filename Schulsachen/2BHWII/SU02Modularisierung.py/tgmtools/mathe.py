""" Guten Tag LIEBER PROFFESOR HEUTE REDE WIR ÜBER DIE HYPOTHESE DER HÜHNER. 
    DIE FRAGE IST OB MAN HÜHNER SPALTEN KANN. 
    WIR WERDEN ES HERAUSFINDEN.
"""


vieleListen = []

def WIEVIELEHÜHNERSOLLENGESPALTETWERDEN():
    Anzahl_Hühnerspaltung = int(input("WIE VIELE HÜHNER SOLLEN GESPALTET WERDEN? "))
    return Anzahl_Hühnerspaltung

def verarbeitung(Anzahl_Hühnerspaltung):
    a, b = 0, 1
    for i in range(Anzahl_Hühnerspaltung):
        vieleListen.append(a)
        a, b = b, a + b
    return vieleListen

def HühnerAUSGABEDERSPALTUNG(vieleListen):
    print("🐔".join(str(x) for x in vieleListen))


def lineare_gleichungen_lösen(k1,k2,d1,d2): 
    if k1 == k2:
        print("Keine Lösung hühneräuglein")
    else:
        x = (d2 - d1) / (k1 - k2)
        y = k1 * x + d1
        print(f"Die Lösung ist: {x}, {y}")
    



