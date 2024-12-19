import json
import os
import random
from typing import List, Dict, Any

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item_id: int, quantity: int = 1):
        item = self.load_item_data(r'modules/lookuptable.json', item_id)
        existing_item = next((i for i in self.items if i['name'] == item['name']), None)
        if existing_item:
            existing_item['amount'] += quantity
        else:
            item['amount'] = quantity
            self.items.append(item)

    def remove_item(self, item_id: int, quantity: int = 1):
        item = next((i for i in self.items if i['id'] == item_id), None)
        if item:
            if item['amount'] > quantity:
                item['amount'] -= quantity
            else:
                self.items.remove(item)
        else:
            print(f"Item with ID {item_id} not found in inventory.")

    @staticmethod
    def load_item_data(file_path: str, item_id: int) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data['items'][str(item_id)]

class Character:
    def __init__(self, name: str):
        self.name = name

class Player(Character):
    def __init__(self, name: str):
        super().__init__(name)
        self.inventory = Inventory()
        self.level = 1
        self.initial_items_added = False  # Flag to track if initial items have been added

class Game:
    def __init__(self, story_path: str):
        self.story = self.load_story(story_path)
        self.player = Player(name="Adventurer")
        self.current_island = self.story['islands'][0]  # Start at the first island (Intro)

    @staticmethod
    def load_story(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def start(self):
        self.player.name = input("Enter your name: ").strip()
        print(f"Welcome, {self.player.name}! Let the adventure begin.")
        self.display_island()

    def display_island(self):
        print(f"\n{self.current_island['name']}")
        print(self.current_island['description'])
        for npc in self.current_island.get('npcs', []):
            print(f"{npc['name']} ({npc['role']}): {npc['dialogue']}")
        print("-" * 40)
        self.display_actions(self.current_island['actions'])

    def display_actions(self, actions: List[Dict[str, Any]]):
        while True:
            print("Available Actions:")
            for idx, action in enumerate(actions, start=1):
                print(f"[{idx}] {action['description']}")
            print("[0] Exit Game")

            choice = input("Choose an action: ").strip()
            if choice == "0":
                print("Thanks for playing!")
                exit()

            try:
                selected_id = int(choice) - 1
                if 0 <= selected_id < len(actions):
                    selected_action = actions[selected_id]
                    self.handle_action(selected_action)
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def handle_action(self, action: Dict[str, Any]):
        if action.get("response") == "// show inventory":
            self.show_inventory()
        elif action.get("response") == "// initiate combat":
            self.initiate_combat()
        elif action.get("response") == "// bazzar":
            self.bazaar()
        else:
            print(f"\n{action.get('response', 'No response available.')}")
            if "add_items" in action:
                self.modify_inventory(action["add_items"], add=True)
            if "remove_items" in action:
                self.modify_inventory(action["remove_items"], add=False)

            if "next_location" in action:
                self.travel_to(action["next_location"])
            else:
                self.display_island()  # Redisplay the same location after action

    def modify_inventory(self, items: Dict[int, int], add: bool = True):
        for item_id, quantity in items.items():
            if add:
                self.player.inventory.add_item(item_id, quantity)
            else:
                self.player.inventory.remove_item(item_id, quantity)

    def travel_to(self, island_name: str):
        island = next((i for i in self.story.get("islands", []) if i['name'] == island_name), None)
        if island:
            self.current_island = island
            self.display_island()
        else:
            print("Island not found.")

    def show_inventory(self):
        print("\n🧳 Inventory:")
        if not self.player.inventory.items:
            print("Your inventory is empty.")
        else:
            for idx, item in enumerate(self.player.inventory.items, start=1):
                print(f"[{idx}] {item['name']} - Quantity: {item['amount']}")
        print("-" * 40)


    def initiate_combat(self, mob_name):
        print("⚔️ Combat initiated! Prepare for battle.")
        mobs = self.current_island.get('mobs', [])
        mob = next((m for m in mobs if m['name'] == mob_name), None)
        if not mob:
            print("No such enemy to fight here.")
            return

        print(f"You encounter a {mob['name']}!")
        print(mob['description'])

        player_health = 100
        enemy_health = mob['stats']['health']

        while player_health > 0 and enemy_health > 0:
            action = input("Choose your action: [1] Attack [2] Run: ").strip()
            if action == "1":
                damage = random.randint(5, 15)
                enemy_health -= damage
                print(f"You dealt {damage} damage to the {mob['name']}. Enemy health: {enemy_health}")

                if enemy_health <= 0:
                    print(f"You defeated the {mob['name']}!")
                    self.modify_inventory(mob['drops'], add=True)
                    break

                enemy_damage = random.randint(0, mob['stats']['attack'])
                player_health -= enemy_damage
                print(f"The {mob['name']} dealt {enemy_damage} damage to you. Your health: {player_health}")

                if player_health <= 0:
                    print("You have been defeated!")
                    break
            elif action == "2":
                print("You ran away from the battle.")
                break
            else:
                print("Invalid action. Choose [1] to Attack or [2] to Run.")

        self.display_island()

    def bazaar(self):
        items = self.load_item_data(r'modules/lookuptable.json')
        while True:
            print("\n🛒 Bazaar:")
            for item_id, item in items.items():
                print(f"[{item_id}] {item['name']} - {item['description']} - Value: {item['value']} Gold")
            print("[0] Exit Bazaar")

            choice = input("Choose an item to buy/sell or exit: ").strip()
            if choice == "0":
                break

            try:
                item_id = int(choice)
                if str(item_id) in items:
                    self.trade_item(item_id, items[str(item_id)])
                else:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")

    def trade_item(self, item_id: int, item: Dict[str, Any]):
        print(f"\nTrading {item['name']}:")
        print("[1] Buy")
        print("[2] Sell")
        print("[0] Cancel")

        choice = input("Choose an action: ").strip()
        if choice == "1":
            self.buy_item(item_id, item)
        elif choice == "2":
            self.sell_item(item_id, item)
        elif choice == "0":
            return
        else:
            print("Invalid choice. Try again.")

    def buy_item(self, item_id: int, item: Dict[str, Any]):
        if self.player.gold >= item['value']:
            self.player.gold -= item['value']
            self.player.inventory.add_item(item_id)
            print(f"Bought {item['name']} for {item['value']} Gold. Remaining Gold: {self.player.gold}")
        else:
            print("Not enough gold to buy this item.")

    def sell_item(self, item_id: int, item: Dict[str, Any]):
        if any(i['id'] == item_id for i in self.player.inventory.items):
            self.player.inventory.remove_item(item_id)
            self.player.gold += item['value']
            print(f"Sold {item['name']} for {item['value']} Gold. Total Gold: {self.player.gold}")
        else:
            print("You don't have this item in your inventory.")

if __name__ == "__main__":
    story_path = r"modules/story_blocks.json"
    game = Game(story_path)
    game.start()