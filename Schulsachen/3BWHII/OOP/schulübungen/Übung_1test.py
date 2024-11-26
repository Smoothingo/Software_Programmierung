class Mammal():

    """
    Klasse Mammal  
    Name
    kann sprechen
    kann essen
    Verwendung:
    >>> mammal = Mammal("name")
    """
    klasse = "mammal"  #Klassen/statisches attribut
    def __init__ (self, name: str, extrements: int = 4) -> None:
        self.name = name #Dynamisches/instanz attribut (öffentlich/public)
        self.__extrements = extrements

    def speak(self) -> str:
        """Lässt tier sprechen"""
        return "spricht"
    
    @property
    def extrements(self) -> int:   # getter
        return self.__extrements   # private attribut

    @extrements.setter
    def extrements(self, extr: int): #setter
        if not isinstance(extr, int):
            raise TypeError("extrements muss eine Ganzzahl sein")
        if extr < 0 or extr > 4:
            raise ValueError("extrements muss zwischen 0 und 4 sein")

        return self.__extrements

    def __str__(self):
        return f"{self.name} ist ein {self.klasse}"
    
    def __repr__(self):
        return "Mammal('name')"
    
    






class Cat(Mammal):
    """
    Description: Klasse Cat

    name: Name der Katze

    fellfarbe: Farbe des Fells

    >>> cat = Cat("Minka", "schwarz")
    """
    def __innit__(self, name: str, fellfarbe: str) -> None:
        super().__init__(name)
        self.fellfarbe = fellfarbe

    def speak(self) -> str:
        return f"{self.name} miaut"

class Dog(Mammal):
    def speak(self) -> str:
        return f"{self.name} Wuff"
    
katze = Cat("Minka")
mutzi = Cat("Mutzi")
flecki = Cat("Flecki")
axel = Dog("Axel")
schurli = Dog("Schurli")
print(katze.speak())
print(axel.speak())






