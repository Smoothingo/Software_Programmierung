import numpy
import math as mt
from tgmtools.mathe import  *
import tgmtools.io

#numpy.... globales Modul / Bibliothek , numphy = Standard Bibliothek.
#Namensraum, d.h. Funktion in diesem Modul sind über den Namen des Moduls erreichbar.

sin_x = numpy.sin(0)
print(sin_x)

cos_x = mt.cos(0)
print(cos_x)

from tgmtools import hallob
from tgmtools.io import i_input


nummer1 = i_input(" GIb die 1. Zahl ein", float)
nummer2 = i_input(" GIb die 2. Zahl ein", float)
print(nummer1 + nummer2)
Anzahl_Hühnerspaltung = i_input(prompt = "Wie viele Fibonnaci Stellen?", type = int)
vieleListen = verarbeitung(Anzahl_Hühnerspaltung)
HühnerAUSGABEDERSPALTUNG(vieleListen)
#GUTEN TAG