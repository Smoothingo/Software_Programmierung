from .inventory import Inventory

class Player:
    def __init__(self, name, game):
        self.name = name or "Adventurer"
        self.game = game
        self.inventory = Inventory()
        self.level = 1
        self.xp = 0
        self.base_health = 100
        self.base_attack = 10
        self.base_defense = 5
        self.health = self.base_health
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.equipped_sword = None
        self.equipped_armor = None

    def get_stats(self):
        return {
            'level': self.level,
            'xp': f"{self.xp}/{self.level * 100}",
            'health': self.health,
            'attack': self.attack,
            'defense': self.defense,
            'sword': self.equipped_sword['name'] if self.equipped_sword else "None",
            'armor': self.equipped_armor['name'] if self.equipped_armor else "None"
        }

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.level * 100:
            self.level += 1
            self.base_health += 10
            self.base_attack += 2
            self.base_defense += 2
            self.reset_stats()

    def reset_stats(self):
        self.health = self.base_health
        self.attack = self.base_attack
        self.defense = self.base_defense

        # Reapply equipped items' stats
        if self.equipped_sword:
            self.attack += self.equipped_sword['stats'].get('attack', 0)
        if self.equipped_armor:
            self.defense += self.equipped_armor['stats'].get('defense', 0)

    def use_item(self, item_id, target=None):
        item = self.inventory.get_item(item_id)
        if item['type'] == 'potion':
            if 'heal' in item['stats']:
                self.health = min(self.health + item['stats']['heal'], self.base_health)
            return True
        return False