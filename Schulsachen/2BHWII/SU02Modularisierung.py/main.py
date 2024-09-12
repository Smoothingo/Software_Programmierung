import numpy
import math as mt
from tgmtools.mathe import  *
from tgmtools.io import *

#numpy.... globales Modul / Bibliothek , numphy = Standard Bibliothek.
#Namensraum, d.h. Funktion in diesem Modul sind über den Namen des Moduls erreichbar.

# sin_x = numpy.sin(0)
# print(sin_x)

# cos_x = mt.cos(0)
# print(cos_x)


from tgmtools.io import i_input


# nummer1 = i_input(" GIb die 1. Zahl ein", float)
# nummer2 = i_input(" GIb die 2. Zahl ein", float)
# print(nummer1 + nummer2)
# Anzahl_Hühnerspaltung = i_input(prompt = "Wie viele Fibonnaci Stellen?", type = int)
# vieleListen = verarbeitung(Anzahl_Hühnerspaltung)
# HühnerAUSGABEDERSPALTUNG(vieleListen)

action = input("Type 1 if u want to calculate a linear equation, type 2 if u want to get an intelligent print: ")
action = int(action)
if action == 1:
    k1 = i_input("Gib k1 ein: " , float)
    k2 = i_input("Gib k2 ein: " , float)
    d1 = i_input("Gib d1 ein: " , float)
    d2 = i_input("Gib d2 ein: " , float)
    lineare_gleichungen_lösen(k1,k2,d1,d2)
if action == 2:
    intelligent_print(["Hallo", "Welt", "!"])

#GUTEN TAG