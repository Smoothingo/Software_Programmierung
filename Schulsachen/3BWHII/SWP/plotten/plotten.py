import matplotlib.pyplot as plt #plots
import numpy as np #Mathe

# x = np.arange(0, 2*np.pi, 0.1) 
# y = ...

# print(x)
stat_X = 0 #startwert
end_x = 2*np.pi #endwert
step_size = 0.1 #Schrittweite
x = np.arange(stat_X, end_x + step_size, step_size)
y = np.sin(x) #Erzeugt ein Array mit den Sinuswerten von x
print(x)

plt.plot(x, y1, 'yo-',
         x, y2, 'r.--',
         x, y3, 'g^-',
        ) #Plottet die Werte von x gegen y in rot
plt.grid() #Zeigt das Gitter an
plt.title('Winkelfunktion') #Titel des Diagramms
plt.xlabel('x') #Beschriftung der x-Achse
plt.ylabel('y = sin(x)') #Beschriftung der y-Achse
plt.ylim(-1.1, 1.1)
plt.show() #Zeigt das Diagramm im TK-Frontend an

#Monte - Carlo- Simulation
# je mehr Wiederholungen desto genauer wird das Ergebnis
# Ziel: "Berechnung" der Zahl Pi

