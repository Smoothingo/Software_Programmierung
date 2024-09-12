import sys
import json
import time
import os 
def fibo_ask(): #hässliche funtkion
    try:
        abfrage = int(input("Wie viele Fibonacci-Zahlen sollen berechnet werden? "))
    except ValueError:  # error handling für buchstaben etc
        print('\nNIX INTEGER')  # exit message
        fibo_ask()  #exit vom programm
#error handling für 0 und negative zahlen
    if abfrage <= 0:
        print('\nNIX POSTIV/0')
        fibo_ask()
    else:
        fibo_list = [0, 1]    # basis Liste
        for i in range(2, abfrage+1):  
            fibo_list.append(fibo_list[i-1] + fibo_list[i-2])  # zusammenzählen der letzten beiden Zahlen und an die liste hängen
        print(fibo_list)  # ausgabe vom listenwahnsinn
        with open('fibo_massaker.json', 'w') as f:
            json.dump(fibo_list, f)
        print("wurden an fibo.json angehängt")
        time.sleep(3)
        os.system('cls')
        fibo_ask()




if __name__ == "__main__":
    fibo_ask() # test zeile 
