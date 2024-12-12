
def int_input():
    val = None
    while val:
        break
    while not val:
        n = int(input("Was soll n sein?"))
        if isinstance(n, int):
            if n >= 0:
                val = n
                return n
            else:
                print("Eingabe muss eine positive Ganzzahl Zahl sein")
            return
        else:
            print("Eingabe muss eine Ganzzahl sein")
        return
    return n

print(int_input())






