
from module import weird_shit
from module import rechenarten

def grund_stuff(ops, a, b):
    try:
        if ops == '+':
            return rechenarten.addiere(a, b)
        elif ops == '-':
            return rechenarten.subtrahiere(a, b)
        elif ops == '*':
            return rechenarten.multipliziere(a, b)
        elif ops == '/':
            result = rechenarten.dividiere(a, b)
            if result is None:
                print("Fehler: Division durch 0")
            return result
        else:
            print("Geh in die Grundschule zurück")
            return None
    except ValueError:
        return None

def special_stuff(ops, n):
    if ops == 'f':
        return weird_shit.fakultät(n)
    elif ops == 'g':
        return weird_shit.gauss_summe(n)
    else:
        print("Ungültige Operation.")
        return None

def logic_big_boy():
    rechenart = input(' "G" = normal Rechnen "S" weird Gauss/Fakultät:').lower()  # alles zu Klenbuchstabn

    if rechenart == 's':
        ops = input(" 'f' = Fakultät oder 'g' für Gauss ").lower()  
        n = int(input("Gib die Zahl n ein: "))
        fertich = special_stuff(ops, n)

    elif rechenart == 'g':
        try:
            a = float(input("Gib a ein: "))
            b = float(input("Gib b ein: "))
            ops = input("Gib '+, -, *, /' ein: ").lower()  
            fertich = grund_stuff(ops, a, b)
        except ValueError:
            print("Ungültige Eingabe. Bitte Zahlen eingeben.")
            return

    else:
        print("Ungültige Rechenart.")
        return

    print(f"fertich: {fertich}")