from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"  #source https://www.youtube.com/watch?v=xdkY6yhEccA
import json
import os
import io 
import random
import time
from typing import List, Dict, Any
import pygame
import threading
import sys

#docstrings und paar comments mit chatgpt


def play_audio(file_path_music: str): #https://www.youtube.com/watch?v=xdkY6yhEccA
    """
    Plays an audio file using pygame.

    Args:
        file_path_music (str): The path to the audio file.
    """
    absolute_path = os.path.abspath(file_path_music)
    if not os.path.exists(absolute_path):
        print(f"File not found: {absolute_path}")
        return
    
    # Redirect stdout to suppress the pygame welcome message
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    pygame.mixer.init()
    
    # Restore stdout
    sys.stdout = original_stdout
    
    pygame.mixer.music.load(absolute_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def slow_print(text: str, delay: float = 0.1):
    """
    Prints text slowly, character by character.

    Args:
        text (str): The text to print.
        delay (float): The delay between each character.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def faster_print(text: str, delay: float = 0.07):
    """
    Prints text faster than slow_print, character by character.

    Args:
        text (str): The text to print.
        delay (float): The delay between each character.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def describe_print(text: str, delay: float = 0.084):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def load_ascii_art(filename):
    """
    Loads ASCII art from a file.

    Args:
        filename (str): The path to the ASCII art file.

    Returns:
        str: The contents of the ASCII art file.
    """
    with open(filename, 'r') as file:
        return file.read()

GOD_ASCII_ART = load_ascii_art(r'modules\ascii\angel.txt')
ANGEL_ASCII_ART = load_ascii_art(r'modules\ascii\god.txt')

class Inventory:
    def __init__(self):
        """
        Initializes an empty inventory.
        """
        self.items = []

    def add_item(self, item_id: int, quantity: int = 1):
        """
        Adds an item to the inventory.

        Args:
            item_id (int): The ID of the item to add.
            quantity (int): The quantity of the item to add.
        """
        item = self.load_item_data(r'modules/lookuptable.json', item_id)
        existing_item = next((i for i in self.items if i['id'] == item_id), None)
        if existing_item:
            existing_item['amount'] += quantity
        else:
            item['amount'] = quantity
            self.items.append(item)

    def remove_item(self, item_id: int, quantity: int = 1):
        """
        Removes an item from the inventory.

        Args:
            item_id (int): The ID of the item to remove.
            quantity (int): The quantity of the item to remove.
        """
        item = next((i for i in self.items if i['id'] == item_id), None)
        if item:
            if item['amount'] > quantity:
                item['amount'] -= quantity
            else:
                self.items.remove(item)
        else:
            print(f"Item with ID {item_id} not found in inventory.")


    def get_item_quantity(self, item_id: int) -> int:
        item = next((i for i in self.items if i['id'] == item_id), None)
        return item['amount'] if item else 0


    def modify_item_quantity(self, item_id: int, quantity: int):
        item = next((i for i in self.items if i['id'] == item_id), None)
        if item:
            item['amount'] += quantity
            if item['amount'] <= 0:
                self.items.remove(item)
        else:   
            if quantity > 0:
                    item = self.load_item_data(r'modules/lookuptable.json', item_id)
                    item['amount'] = quantity
                    self.items.append(item)
            else:
                print(f"Item with ID {item_id} not found in inventory.")

    @staticmethod
    def load_item_data(file_path: str, item_id: int = None) -> Dict[str, Any]:
        """
        Loads item data from a JSON file.

        Args:
            file_path (str): The path to the JSON file.
            item_id (int): The ID of the item to load.

        Returns:
            Dict[str, Any]: The item data.
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        if item_id is None:
            return data['items']
        return data['items'][str(item_id)]



class Character:
    def __init__(self, name: str):
        self.__name = name  # private Varible

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def describe(self) -> None:
        """
        Describes the character.
        """
        print(f"{self.name} is a character in the game.")
        

class Player(Character):
    def __init__(self, name: str, game, base_health: int = 100, base_attack: int = 10, base_defense: int = 5):
        """
        Initializes a player with default health.
        """
        super().__init__(name)
        self.game: 'Game' = game
        self.inventory: Inventory = Inventory()
        self.__level: int = 1  # Private level
        self.xp: int = 0
        self.base_health = base_health
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.health = self.base_health
        self.attack = self.base_attack
        self.defense = self.base_defense
        self.gold_item_id: int = 2
        self.initial_items_added: bool = False  # Flag to track if initial items have been added
        self.equipped_sword: str = None
        self.equipped_armor: str = None
        self.teleported_to_ender_island: bool = False

    @property
    def level(self):
        return self.__level

    @level.setter
    def level(self, level: int):
        self.__level = level


    def gain_xp(self, amount: int):
        self.xp += amount
        print(f"You gained {amount} XP. Total XP: {self.xp}")
        print(f"🔋 XP: {self.xp}/{self.level * 100}")
        self.check_level_up()  # Call check_level_up without returning a value

    def check_level_up(self):
        level_threshold = 100  # Fixed threshold: 100 XP per level
        while self.xp >= self.level * level_threshold:
            self.level += 1
            self.base_health += 10  # Increase base health on level up
            self.base_attack += 2   # Increase base attack on level up
            self.base_defense += 2  # Increase base defense on level up
            self.reset_stats()
            print(f"Congratulations! You leveled up to Level {self.level}.")
            print(f"New stats - Health: {self.health}, Attack: {self.attack}, Defense: {self.defense}")

            if self.level >= 10 and not self.teleported_to_ender_island:
                self.teleported_to_ender_island = True
                self.game.encounter_god()  # Call encounter_god directly

    def reset_stats(self):
        self.health = self.base_health
        self.attack = self.base_attack
        self.defense = self.base_defense
    
    def describe(self) -> None:
        """
        Describes the player.
        """
        describe_print(
            f"Welcome, brave adventurer {self.name}! 🌟\n"
            f"You stand at the dawn of an epic journey, filled with peril and glory.\n"
            f"At Level {self.level}, you are just beginning to uncover your true potential.\n"
            f"Health: {self.health}/{self.base_health} - Your vitality is strong, ready to face the challenges ahead.\n"
            f"Attack: {self.attack} - Your strikes are precise, capable of felling your foes.\n"
            f"Defense: {self.defense} - Your defenses are sturdy, protecting you from harm.\n"
            f"\n"
            f"Hear me, {self.name}, for you are chosen among mortals. Your journey is one of legend, and your deeds will echo through the annals of time.\n"
            f"Equipped with the strength of titans and the wisdom of sages, you will carve your path through the darkness, illuminating the way for others.\n"
            f"Your heart is pure, your resolve unbreakable. No foe can stand before you, no challenge too great.\n"
            f"\n"
            f"Rise, {self.name}, and begin your quest. The world watches in awe, and the gods themselves whisper your name in reverence.\n"
            f"May your blade stay sharp, your armor strong, and your spirit forever indomitable.\n"
            f"\n"
            f"Go forth, {self.name}, and let your legend be written in the stars.\n"
            f"Remember, as you grow stronger and gain experience, you will face greater challenges.\n"
            f"One day, you may need to confront the mighty Ender Dragon. Prepare yourself, for that battle will test your limits like never before.\n"
            f"Level up, gather powerful equipment, and hone your skills. The fate of this world may one day rest in your hands."
        )

    def take_damage(self, amount: int):
        """
        Reduces the player's health by a specified amount.

        Args:
            amount (int): The amount of damage to take.
        """
        self.health -= amount
        print(f"You took {amount} damage. Health is now {self.health}.")
        if self.health <= 0:
            player_death()

    def check_health(self):
        """
        Checks the player's health and triggers death if health is zero or below.
        """
        if self.health <= 0:
            player_death()

    def use_item(self, item_id: int, target=None):
        """
        Method for using an item specific to the player.
        """
        item = next((i for i in self.inventory.items if i['id'] == item_id), None)
        if item:
            item_data = self.inventory.load_item_data(r'modules/lookuptable.json', item_id)
            stats = item_data.get('stats', {})
            item_type = item_data.get('type', 'misc')
            if item_type == 'potion':
                if 'heal' in stats:
                    heal_amount = stats['heal']
                    self.health = min(self.health + heal_amount, self.base_health)  # Ensure health does not exceed base health
                    self.inventory.remove_item(item_id, 1)  # Remove one potion from inventory
                    print(f"You used a {item_data['name']} and restored {heal_amount} health.")
                    return heal_amount  # Return the amount of health restored
                if 'poison' in stats and target:
                    target['health'] -= stats['poison']
                    self.inventory.remove_item(item_id, 1)  # Remove one potion from inventory
                    print(f"You used a {item_data['name']} and dealt {stats['poison']} poison damage to the {target['name']}. Enemy health: {target['health']}")
            elif item_type == 'weapon':
                if 'attack' in stats:
                    self.attack += stats['attack']
                    self.equipped_sword = item_data['name']
                    print(f"You equipped a {item_data['name']}. Current attack: {self.attack}")
            elif item_type == 'armor':
                if 'defense' in stats:
                    self.defense += stats['defense']
                    self.equipped_armor = item_data['name']
                    print(f"You equipped a {item_data['name']}. Current defense: {self.defense}")
        else:
            print("Item not found in inventory.")
        return 0  # Return 0 if no health was restored

    def choose_equipment(self):
        while True:
            print("\nChoose an option:")
            print("[1] View current loadout/Stats")
            print("[2] Change loadout")
            print("[0] Cancel")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                print(f"\nCurrent Loadout:")
                print(f"🆙 Level: {self.level}")
                print(f"🔋 XP: {self.xp}/{self.level * 100}")
                print(f"❤️ Health: {self.health}")
                print(f"⚔️ Attack: {self.attack}")
                print(f"🛡️ Defense: {self.defense}")
                if self.equipped_sword:
                    print(f"🗡️ Sword: {self.equipped_sword}")
                else:
                    print("🗡️ Sword: Player is a no skin homeless nude enthusiast")
                if self.equipped_armor:
                    print(f"🛡️ Armor: {self.equipped_armor}")
                else:
                    print("🛡️ Armor: Player is a no skin homeless nude enthusiast")
            elif choice == "2":
                self.reset_stats()  # resets stat
                self.equipped_sword = None
                self.equipped_armor = None
                swords = [item for item in self.inventory.items if self.inventory.load_item_data(r'modules/lookuptable.json', item['id']).get('type') == 'weapon']
                armors = [item for item in self.inventory.items if self.inventory.load_item_data(r'modules/lookuptable.json', item['id']).get('type') == 'armor']

                if not swords and not armors:
                    print("You can't change loadout, you have nothing available.")
                    continue


                if swords:
                    print("\nChoose a sword to equip:")
                    for vorne_id, sword in enumerate(swords, start=1):
                        item_data = self.inventory.load_item_data(r'modules/lookuptable.json', sword['id'])
                        print(f"[{vorne_id}] {sword['name']} - Attack: +{item_data['stats']['attack']}")
                    sword_choice = input("Enter the sword number to equip or 0 to skip: ").strip()
                    if sword_choice != "0":
                        try:
                            sword_vorne_id = int(sword_choice) - 1
                            if 0 <= sword_vorne_id < len(swords):
                                self.use_item(swords[sword_vorne_id]['id'])
                            else:
                                print("Invalid choice. No sword equipped.")
                        except ValueError:
                            print("Invalid input. No sword equipped.")

                if armors:
                    print("\nChoose an armor to equip:")
                    for vorne_id, armor in enumerate(armors, start=1):
                        item_data = self.inventory.load_item_data(r'modules/lookuptable.json', armor['id'])
                        print(f"[{vorne_id}] {armor['name']} - Defense: +{item_data['stats']['defense']}")
                    armor_choice = input("Enter the armor number to equip or 0 to skip: ").strip()
                    if armor_choice != "0":
                        try:
                            armor_vorne_id = int(armor_choice) - 1
                            if 0 <= armor_vorne_id < len(armors):
                                self.use_item(armors[armor_vorne_id]['id'])
                            else:
                                print("Invalid choice. No armor equipped.")
                        except ValueError:
                            print("Invalid input. No armor equipped.")
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please choose a valid option.")

def player_death():
    """
    Handles the player's death by playing a sound and printing a game over message.
    """
    print("You have died.")
    play_audio(r'modules\audio\death_sound.mp3')  # Optional: Play a death sound
    slow_print("Game Over. Better luck next time!", 0.1)
    exit()

class Game:
    def __init__(self, story_path: str):
        self.story = self.load_story(story_path)
        self.player = Player(name="Adventurer", game=self)  # Pass the Game instance to Player
        self.current_island = self.story['islands'][0]  # Start at the first island (Intro)

    @staticmethod
    def load_story(file_path: str) -> Dict[str, Any]:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def start(self):
        """ Starts the game by welcoming the player and displaying the first island. """
        self.player.name = input("Enter your name: ").strip()
        slow_print(f"Welcome, {self.player.name}! Let the adventure begin.")
        self.display_island()

    def display_island(self):
        """ Displays the current island's description, NPCs, and available actions. """

        print(f"\n{self.current_island['name']}")
        print(self.current_island['description'])
        for npc in self.current_island.get('npcs', []):
            print(f"{npc['name']} ({npc['role']}): {npc['dialogue']}")
        print("-" * 40)
        self.display_actions(self.current_island['actions'])

    def display_actions(self, actions: List[Dict[str, Any]]):
        while True:
            print("Available Actions:")
            for vorne_id, action in enumerate(actions, start=1):
                print(f"[{vorne_id}] {action['description']}")
            print("[0] Exit Game")

            choice = input("Choose an action: ").strip()
            if choice == "0":
                player_death()

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
            self.initiate_combat(action.get("mob"))
        elif action.get("response") == "// bazzar":
            self.bazaar()
        elif action.get("response") == "// loser":
            print("You are a loser.")
            player_death()
        elif action.get("response") == "// travel":
            self.travel_to(action.get("next_location"))
        elif action.get("response") == "// ask god who you are":
            audio_thread = threading.Thread(target=play_audio, args=(r'modules\audio\player_introduc.mp3',))
            audio_thread.start()
            self.player.describe()

        elif action.get("response") == "// change loadout":
            self.player.choose_equipment()
        else:
            print(f"\n{action.get('response', 'No response available.')}")
            if "add_items" in action:  # items in inventar hinzufügen
                self.modify_inventory(action["add_items"], add=True)
            if "remove_items" in action:  # items aus inventor entfernen
                self.modify_inventory(action["remove_items"], add=False)
            if "add_xp" in action:
                self.player.gain_xp(action["add_xp"])

            if "next_location" in action:  # teleportation zu denb location in story.json festgelegt
                self.travel_to(action["next_location"])
            else:
                self.display_island()

    def encounter_god(self):
        """
        Handles the encounter with the god character, playing audio and printing messages.
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear terminal
        audio_thread = threading.Thread(target=play_audio, args=(r'modules\audio\GODTEXT.mp3',))
        audio_thread.start()
        print("👼 AN ANGEL APPEARS BEFORE YOU...")
        print(ANGEL_ASCII_ART)
        time.sleep(1)
        print(GOD_ASCII_ART)
        faster_print("Hello Adventurer, I am the God of this world.")
        faster_print("\nYou are the chosen hero who must fight the Ender Dragon.")
        faster_print("You are being teleported to Ender Island to save the Human race and become the strongest Adventurer that ever lived...\n")
        input("Press Enter to continue...")
        self.travel_to("Ender Island")

    def modify_inventory(self, items: Dict[int, int], add: bool = True):
        """
        Modifies the player's inventory by adding or removing items.

        Args:
            items (Dict[int, int]): A dictionary of item IDs and quantities.
            add (bool): If True, adds items to the inventory; if False, removes items.
        """
        for item_id, quantity in items.items():
            if add:
                self.player.inventory.add_item(item_id, quantity)
            else:
                self.player.inventory.remove_item(item_id, quantity)

    def travel_to(self, island_name: str):
        """
        Travels to a specified island.

        Args:
            island_name (str): The name of the island to travel to.
        """
        island = next((i for i in self.story.get("islands", []) if i['name'] == island_name), None)
        if island:
            self.current_island = island
            self.display_island()
        else:
            print("Island not found.")

    def ender_dragon_defeated(self):
        """
        Handles the event when the Ender Dragon is defeated.
        """
        slow_print("Congratulations! You have defeated the Ender Dragon!")
        slow_print("You are being teleported back to the hub...\n")
        self.travel_to("Hub Island")  # Teleport  hub

    def show_inventory(self):
        """
        Displays the player's inventory.
        """
        print("\n🧳 Inventory:")
        if not self.player.inventory.items:
            print("Your inventory is empty.")
        else:
            for vorne_id, item in enumerate(self.player.inventory.items, start=1):
                print(f"[{vorne_id}] {item['name']} - Quantity: {item['amount']}")
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

        player_health = self.player.health
        enemy_health = mob['stats']['health']

        while player_health > 0 and enemy_health > 0:
            print("\nChoose your action:")
            print("[1] Attack")
            print("[2] Use Item")
            print("[3] Run")
            action = input("Enter your choice: ").strip()

            if action == "1":
                damage = max(0, random.randint(5, 15) + self.player.attack - mob['stats']['defense'])
                enemy_health -= damage
                print(f"You dealt {damage} damage to the {mob['name']}. Enemy health: {enemy_health}")

                if enemy_health <= 0:
                    print(f"You defeated the {mob['name']}!")
                    self.modify_inventory(mob['drops'], add=True)
                    xp_gain = next((action['add_xp'] for action in self.current_island['actions'] if action.get('mob') == mob_name), 50)
                    self.player.gain_xp(xp_gain)  # Use XP value from the story

                    if mob_name == "Ender Dragon":
                        self.ender_dragon_defeated()  # Call ender_dragon_defeated method

                    break

                enemy_damage = max(0, random.randint(0, mob['stats']['attack']) - self.player.defense)
                player_health -= enemy_damage
                print(f"The {mob['name']} dealt {enemy_damage} damage to you. Your health: {player_health}")

                if player_health <= 0:
                    player_death()
            elif action == "2":
                print("[0] Cancel")
                potions = [item for item in self.player.inventory.items if self.player.inventory.load_item_data(r'modules/lookuptable.json', item['id']).get('type') == 'potion']
                if not potions:
                    print("You have no usable items.")
                    continue
                for vorne_id, potion in enumerate(potions, start=1):
                    item_data = self.player.inventory.load_item_data(r'modules/lookuptable.json', potion['id'])
                    print(f"[{vorne_id}] {potion['name']} - {item_data['description']}")
                item_choice = input("Enter the item number to use or 0 to cancel: ").strip()
                if item_choice == "0":
                    continue
                try:
                    item_vorne_id = int(item_choice) - 1
                    if 0 <= item_vorne_id < len(potions):
                        item = potions[item_vorne_id]
                        heal_amount = self.player.use_item(item['id'], target=mob)
                        player_health = min(player_health + heal_amount, self.player.base_health)  # Ensure health does not exceed base health
                        self.player.health = player_health  # Update player's health after using item
                        print(f"Your health after using the item: {self.player.health}")
                    else:
                        print("Invalid choice. Try again.")
                except ValueError:
                    print("Please enter a valid number.")
            elif action == "3":
                print("You ran away from the battle.")
                break
            else:
                print("Invalid action. Choose [1] to Attack, [2] to Use Item, or [3] to Run.")

        self.player.health = player_health  # Update player's health after combat
        self.display_island()

    
    def bazaar(self):
        items = self.player.inventory.load_item_data(r'modules/lookuptable.json')
        categorized_items = {
            "weapon": {},
            "armor": {},
            "potion": {},
            "ressource": {},
            "monster_drops": {},
            "misc": {},
            "currency": {}
        }

        for item_id, item in items.items():
            if item['type'] == 'currency' and item['name'].lower() == 'gold':
                continue  # Exclude gold from the bazaar
            categorized_items[item['type']][item_id] = item

        while True:
            print("\n" + "=" * 40)
            print("🛒 Bazaar:")
            print("=" * 40)

            for category, items in categorized_items.items():
                if items:
                    print(f"\n{category.capitalize()}:")
                    for item_id, item in items.items():
                        quantity = self.player.inventory.get_item_quantity(int(item_id))  # Ensure item_id is an integer
                        print(f"[{item_id}] {item['name']} - {item['description']} - Value: {item['value']} Gold - You have: {quantity}")

            print("\n[0] Exit Bazaar")
            print("=" * 40)

            choice = input("Choose an item to buy/sell or exit: ").strip()

            if choice == "0":
                break

            try:
                item_id = int(choice)  # Convert choice to integer
                found = False
                for category, items in categorized_items.items():
                    if item_id in map(int, items.keys()):  # Ensure keys are compared as integers
                        self.trade_item(item_id, items[str(item_id)])  # Convert item_id back to string for dictionary lookup
                        found = True
                        break
                if not found:
                    print("Invalid choice. Try again.")
            except ValueError:
                print("Please enter a valid number.")
                        
    def trade_item(self, item_id: int, item: Dict[str, Any]):
        while True:
            print("\n" + "-" * 40)
            print(f"\nTrading {item['name']}:")
            print("[1] Buy")
            print("[2] Sell")
            print("[0] Cancel")
            print("-" * 40)

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
        try:
            amount = int(input(f"How many {item['name']} do you want to buy? (You have {self.player.inventory.get_item_quantity(item_id)}): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

        total_cost = item['value'] * amount
        gold_quantity = self.player.inventory.get_item_quantity(self.player.gold_item_id)
        if gold_quantity >= total_cost:
            self.player.inventory.modify_item_quantity(self.player.gold_item_id, -total_cost)
            self.player.inventory.add_item(item_id, amount)
            print(f"Bought {amount} {item['name']} for {total_cost} Gold. Remaining Gold: {self.player.inventory.get_item_quantity(self.player.gold_item_id)}")
        else:
            print("Not enough gold to buy this item.")

    def sell_item(self, item_id: int, item: Dict[str, Any]):
        try:
            amount = int(input(f"How many {item['name']} do you want to sell? (You have {self.player.inventory.get_item_quantity(item_id)}): "))
            if amount <= 0:
                print("Amount must be greater than zero.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return

        if self.player.inventory.get_item_quantity(item_id) >= amount:
            total_value = item['value'] * amount
            self.player.inventory.remove_item(item_id, amount)
            self.player.inventory.modify_item_quantity(self.player.gold_item_id, total_value)
            print(f"Sold {amount} {item['name']} for {total_value} Gold. Total Gold: {self.player.inventory.get_item_quantity(self.player.gold_item_id)}")
        else:
            print("You don't have enough of this item in your inventory.")

        def sell_item(self, item_id: int, item: Dict[str, Any]):
            try:
                amount = int(input(f"How many {item['name']} do you want to sell? (You have {self.player.inventory.get_item_quantity(item_id)}): "))
                if amount <= 0:
                    print("Amount must be greater than zero.")
                    return
            except ValueError:
                print("Invalid amount. Please enter a number.")
                return

            if self.player.inventory.get_item_quantity(item_id) >= amount:
                total_value = item['value'] * amount
                self.player.inventory.remove_item(item_id, amount)
                self.player.inventory.modify_item_quantity(self.player.gold_item_id, total_value)
                print(f"Sold {amount} {item['name']} for {total_value} Gold. Total Gold: {self.player.inventory.get_item_quantity(self.player.gold_item_id)}")
            else:
                print("You don't have enough of this item in your inventory.")

if __name__ == "__main__":
    story_path = r"modules/story_blocks.json"
    game = Game(story_path)
    game.start()