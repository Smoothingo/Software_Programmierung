
class person:

    id = 0

    @staticmethod
    def begrüßen():
        print("Hallo, ich bin ein Mensch")
    # @classmethod
    # def begrüßen(cls):


    def __init__(self, vorname : str, nachname : str, age : int):

        person.id +=1
        self.__vorname = vorname
        self.__nachname = nachname
        self.age = age
        self.id = person.id

    @property
    def vorname(self) -> str:
        return self.__vorname
    
    @vorname.setter
    def vorname(self, val : str) -> None:
        if not isinstance(val, str):
            raise ValueError("Vorname muss ein String sein")
        if len(val) == 0:
            raise ValueError("Vorname darf nicht leer sein")
        self.__vorname = val

    
    def __repr__(self) -> str:
        return f"Main Name ist: {self.__vorname} {self.__nachname} und ich bin ({self.age}) Jahre alt"
    
class mitarbeiter(person):

    id = 0

    def __init__(self, vorname : str, nachname : str, age : int, gehalt : float=2000.):
        super().__init__(vorname, nachname, age)

        """"
        Erstellt einen neuen Mitarbeiter

        Args:
        vorname (str): Vorname des Mitarbeiters
        nachname (str): Nachname des Mitarbeiters
        age (int): Alter des Mitarbeiters
        """

        @property
        def gehalt(self) -> float:
            return self.__gehalt
        
        @gehalt.setter
        def gehalt(self, val : float = 2000.) -> None:
            if not isinstance(val, (int, float)):
                raise ValueError("Gehalt muss ein Float sein")
            if val <= 0:
                raise ValueError("Gehalt darf nicht negativ sein")
            self.__gehalt = val


Paul = person("Paul", "Müller", 2)
Sirin = person("Sirin", "Kaya", 25)
Paul.begrüßen()
print(Paul)
print(Sirin)
