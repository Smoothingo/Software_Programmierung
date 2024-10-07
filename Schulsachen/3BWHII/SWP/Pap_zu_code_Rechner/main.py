from module import rechenarten
from module import weird_shit

def grund_stuff(ops, a, b):
    try:
        if ops == '+':
            return rechenarten.addiere(a, b)
        elif ops == '-':
            return rechenarten.subtrahiere(a, b)
        elif ops == '*':
            return rechenarten.multipliziere(a, b)
        elif ops == '/':
            return rechenarten.dividiere(a, b)
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
        print("geht nicht weiter")
        return None
    
def big_boy():
    rechenart = input(' "G" = normal Rechnen "S" weird Gauss/Fakultät:').lower()  # alles zu Kleinbuchstaben

    if rechenart == 's':
        ops = input(" 'f' = Fakultät oder 'g' für Gauss ").lower()  # alles zu Kleinbuchstaben
        n = int(input("Gib die Zahl n ein: "))
        fertich = special_stuff(ops, n)

    elif rechenart == 'g':
        a = float(input("Gib a ein: "))
        b = float(input("Gib b ein: "))
        ops = input("Gib '+, -, *, /' ein: ").lower()  # alles zu Kleinbuchstaben
        fertich = grund_stuff(ops, a, b)

    else:
        print("Ungültige Rechenart.")
        return

    print(f"fertich: {fertich}")



if __name__ == "__main__":
    big_boy()
