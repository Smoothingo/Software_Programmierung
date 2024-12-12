
class Person:
    def __init__(self, vorname, nachname, adresse, geburtsdatum):
        self.vorname = vorname
        self.nachname = nachname
        self.adresse = adresse
        self.geburtsdatum = geburtsdatum

class Mitarbeiter:
    def __init__(self, vorname, nachname, adresse, geburtsdatum, gehalt):
        self.vorname = vorname
        self.nachname = nachname
        self.adresse = adresse
        self.geburtsdatum = geburtsdatum
        self.gehalt = gehalt

    def get_gehalt(self):
        return self.gehalt

    def set_gehalt(self, gehalt):
        if gehalt < 0:
            print("Gehalt kann nicht negativ sein.")
        else:
            self.gehalt = gehalt

if __name__ == "__main__":
    person = Person("Anna", "Musterfrau", "Musterstraße 1", "01.01.1990")

    mitarbeiter = Mitarbeiter("Ben", "Mustermann", "Beispielweg 2", "02.02.1985", 50000)

    print(f"Person: {person.vorname} {person.nachname}, Adresse: {person.adresse}, Geburtsdatum: {person.geburtsdatum}")
    print(f"Mitarbeiter: {mitarbeiter.vorname} {mitarbeiter.nachname}, Adresse: {mitarbeiter.adresse}, Geburtsdatum: {mitarbeiter.geburtsdatum}, Gehalt: {mitarbeiter.get_gehalt()}")

    mitarbeiter.set_gehalt(55000)
    print(f"Neues Gehalt des Mitarbeiters: {mitarbeiter.get_gehalt()}")

    mitarbeiter.set_gehalt(-1000)
    print(f"Gehalt nach negativem Setzversuch: {mitarbeiter.get_gehalt()}")