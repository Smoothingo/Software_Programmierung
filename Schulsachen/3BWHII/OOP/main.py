# 2 Attribute die mittel Get/Set zum Property erweitert wurden
# ein statisches Attribut
# eine statische Methode
# eine sinnvolle Vererbung
# Überschreiben des Konstruktors der Sub-Klasse, samt Laden des super-Konstruktors
# Überladen von 2 Methoden
# Überschreiben einer weiteren Methode
# Erstellen von 2 Objekten je Klasse und sinnvoller Anwendung der Methoden
# alles für das textadventure wo es um hypixel skyblock geht
# kommentare 

class Character:
    # Statisches Attribut
    player_count = 0

    def __init__(self, name: str, coins: int = 1000, vitality: int = 1, defense: int = 100, health: int = 100):
        # Initialisiert die Instanzvariablen mit den übergebenen Werten
        self.__name = name
        self.coins = coins
        self.vitality = vitality
        self.defense = defense
        self.health = health
        Character.player_count += 1

    @property
    def name(self):
        # Getter für die private Instanzvariable __name
        return self.__name

    @name.setter
    def name(self, name):
        # Setter für die private Instanzvariable __name
        self.__name = name

class Player(Character):
    # Erbt alles von Character
    def __init__(self, name: str, level: int, strength: int = 1, mana: int = 1, coins: int = 1000, vitality: int = 1, defense: int = 100, health: int = 100):
        # Ruft den Konstruktor der Superklasse auf
        super().__init__(name, coins, vitality, defense, health)
        # Initialisiert die zusätzlichen Instanzvariablen
        self.__level = level
        self.strength = strength
        self.mana = mana

    def level_up(self):
        # Erhöht den Level des Spielers um 1
        self.__level += 1

    @property
    def name(self):
        # Getter für die private Instanzvariable __name
        return self._Character__name

    @name.setter
    def name(self, name):
        # Setter für die private Instanzvariable __name
        self._Character__name = name

    @property
    def level(self):
        # Getter für die private Instanzvariable __level
        return self.__level

    @level.setter
    def level(self, level):
        # Setter für die private Instanzvariable __level
        self.__level = level

    @staticmethod
    def get_player(name):
        # Statische Methode, die einen neuen Spieler mit dem angegebenen Namen und Level 1 erstellt
        return Player(name, 1)

# Beispiel für die Verwendung
player = Player("Steve", 1)
print(player.name)  # Ruft den Getter der Superklasse auf und gibt "Steve" aus
print(player.coins)  # Erbt das Attribut von der Superklasse und gibt 1000 aus
player.level_up()
print(player.level)  # Gibt 2 aus
print(f"Health: {player.health}")  # Gibt den Wert von health aus
