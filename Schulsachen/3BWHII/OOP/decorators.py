from time import time

# print("Start")
# hello()
# print("End")

# def dekorator(f):
#     print("Start Timer")
#     f()
#     print("Stop Timer")

# dekorator(hello)
# dekorator(hello)

from datetime import datetime
from time import sleep

def calculate_execution_time(f):
    def inner():
        start = datetime.now()
        f()
        stop = datetime.now()   
        print(f"Die ausführung daurte {stop - start} xy Sekunden")
    return inner

@calculate_execution_time
def hallo():
    ...
    print("Komplexer Algo läuft ewig")
    sleep(2)

@calculate_execution_time
def hello():
    print("nicht so komplex mässig")
    sleep(0.5)

# hello = calculate_execution_time(hello) # ohne @ syntactic sugar

hallo()
hello()


# decorated_function = calculate_execution_time(hallo)  # ich bin eine funktion
# decorated_function()

# def adder(x):
#     def inner(y):
#         return x + y
#     return inner

# add5 = adder(5)
# add2 = adder(2)
# print(add5(10), add2(10)) #15
