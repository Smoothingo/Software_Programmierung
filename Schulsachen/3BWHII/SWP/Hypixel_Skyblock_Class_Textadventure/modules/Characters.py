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
import json
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

class Player():
    # Erbt alles von Character
    def __init__(self, name: str, level: int, inventory: list = [], strength: int = 1, mana: int = 1, coins: int = 1000, vitality: int = 1, defense: int = 100, health: int = 100):
        # Ruft den Konstruktor der Superklasse auf
        # Initialisiert die zusätzlichen Instanzvariablen
        self.__level = level
        self.strength = strength
        self.mana = mana

    @staticmethod
    def load_item_from_json(file_path, item_key):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['items'][item_key]
    
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
    
class Inventory():

    def __init__(self, items: list = []):
        # Initialisiert die Instanzvariable mit der übergebenen Liste
        self.items = items

    def add_item(self, item):
        # Fügt ein Item zur Liste hinzu
        self.items.append(item)

    def remove_item(self, item):
        # Entfernt ein Item aus der Liste
        self.items.remove(item)

    def __str__(self):
        # Gibt die Liste der Items als String zurück
        return str(self.items)
    
class Lootdrops(Inventory):
    # Erbt alles von Inventory
    def __init__(self, items: list = []):
        # Ruft den Konstruktor der Superklasse auf
        super().__init__(items)

    def add_item(self, item):
        # Überschreibt die Methode add_item aus der Superklasse
        # Fügt ein Item zur Liste hinzu und gibt eine Nachricht aus
        super().add_item(item)
        print(f"{item} wurde hinzugefügt!")

    def remove_item(self, item):
        # Überschreibt die Methode remove_item aus der Superklasse
        # Entfernt ein Item aus der Liste und gibt eine Nachricht aus
        super().remove_item(item)
        print(f"{item} wurde entfernt!")

# Beispiel für die Verwendung
player = Player("Steve", 1)
print(player.name)  # Ruft den Getter der Superklasse auf und gibt "Steve" aus
print(player.coins)  # Erbt das Attribut von der Superklasse und gibt 1000 aus
player.level_up()
print(player.level)  # Gibt 2 aus
print(f"Health: {player.health}")  # Gibt den Wert von health aus
