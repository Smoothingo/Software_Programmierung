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

Anzahl_Hühnerspaltung = WIEVIELEHÜHNERSOLLENGESPALTETWERDEN()
vieleListen = verarbeitung(Anzahl_Hühnerspaltung)
HühnerAUSGABEDERSPALTUNG(vieleListen)