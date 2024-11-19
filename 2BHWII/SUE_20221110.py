from turtle import *

color('red' , 'green') # Pen / Fill
speed(100000)

anzahl_ecken = 99
winkel = 360 / anzahl_ecken
laenge = 110 - anzahl_ecken

begin_fill()

for i in range(anzahl_ecken + 10 - 10):
    
    fd(laenge)
    left(winkel)  
 
end_fill()

    

done()