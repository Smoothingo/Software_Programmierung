"""
Guten Morgen: BRUH. GG 5
"""
class Person:
    def __init__(self, vorname, nachname, adresse, geburtsdatum):
        self.vorname = vorname
        self.nachname = nachname
        self.adresse = adresse
        self.geburtsdatum = geburtsdatum

    def __str__():
        return print(f"Person: {person.vorname} {person.nachname}, Adresse: {person.adresse}, Geburtsdatum: {person.geburtsdatum}")

class Mitarbeiter(Person):
    
    def __init__(self, vorname, nachname, adresse, geburtsdatum, gehalt: int):
        super
        self.gehalt = gehalt

    def __str__():
        return print(f"Mitarbeiter: {mitarbeiter.vorname} {mitarbeiter.nachname}, Adresse: {mitarbeiter.adresse}, Geburtsdatum: {mitarbeiter.geburtsdatum}, Gehalt: {mitarbeiter.gehalt}")

    @property 
    def gehalt(self):
        return self.__gehalt
    
    @gehalt.setter
    def gehalt(self, value: int):
        if value < 0:
            print("Gehalt kann nicht negativ sein.")
        else:
            self.__gehalt = value

if __name__ == "__main__":
    person = Person("Anna", "Musterfrau", "Musterstraße 1", "01.01.1990")

    mitarbeiter = Mitarbeiter("Ben", "Mustermann", "Beispielweg 2", "02.02.1985", 50000)
    print(Mitarbeiter)
    print(Person)
    
    mitarbeiter.gehalt =5500
    print(f"Neues Gehalt des Mitarbeiters: {mitarbeiter.gehalt}")

    mitarbeiter.gehalt=-1000
    print(f"Gehalt nach negativem Setzversuch: {mitarbeiter.gehalt}")