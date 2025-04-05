import random

# Define item properties
items = {
    "Wooden Sword": {
        "type": "weapon",
        "damage": 10,
        "price": 10
    },
    "Iron Sword": {
        "type": "weapon",
        "damage": 20,
        "price": 50
    },
    "Healing Potion": {
        "type": "consumable",
        "heal_amount": 50,
        "price": 15
    },
    "Mana Potion": {
        "type": "consumable",
        "mana_restore": 30,
        "price": 20
    },
    "Leather Armor": {
        "type": "armor",
        "defense": 5,
        "price": 25
    },
    "Iron Armor": {
        "type": "armor",
        "defense": 15,
        "price": 75
    }
}

# Define enemy properties
enemies = {
    "Slime": {
        "health": 50,
        "damage": 5,
        "exp": 10,
        "gold": 5
    },
    "Goblin": {
        "health": 100,
        "damage": 10,
        "exp": 20,
        "gold": 10
    },
    "Skeleton": {
        "health": 150,
        "damage": 15,
        "exp": 30,
        "gold": 15
    },
    "Ender Dragon": {
        "health": 1000,
        "damage": 50,
        "exp": 500,
        "gold": 100
    }
}

# Define player stats
player_stats = {
    "health": 100,
    "max_health": 100,
    "mana": 50,
    "max_mana": 50,
    "attack": 10,
    "defense": 5,
    "level": 1,
    "experience": 0,
    "gold": 100,
    "inventory": {
        "Wooden Sword": 1,
        "Healing Potion": 3,
        "Leather Armor": 1
    },
    "equipment": {
        "weapon": "Wooden Sword",
        "armor": "Leather Armor"
    }
}

def get_item_price(item_name):
    return items[item_name]["price"]

def get_item_type(item_name):
    return items[item_name]["type"]

def get_item_damage(item_name):
    return items[item_name]["damage"]

def get_item_defense(item_name):
    return items[item_name]["defense"]

def get_item_heal_amount(item_name):
    return items[item_name]["heal_amount"]

def get_item_mana_restore(item_name):
    return items[item_name]["mana_restore"]

def get_enemy_health(enemy_name):
    return enemies[enemy_name]["health"]

def get_enemy_damage(enemy_name):
    return enemies[enemy_name]["damage"]

def get_enemy_exp(enemy_name):
    return enemies[enemy_name]["exp"]

def get_enemy_gold(enemy_name):
    return enemies[enemy_name]["gold"]

def update_player_stats(stat_name, value):
    player_stats[stat_name] += value

    if stat_name == "health" and player_stats["health"] > player_stats["max_health"]:
        player_stats["health"] = player_stats["max_health"]
    elif stat_name == "mana" and player_stats["mana"] > player_stats["max_mana"]:
        player_stats["mana"] = player_stats["max_mana"]

def get_player_stat(stat_name):
    return player_stats[stat_name]

def add_item_to_inventory(item_name, quantity=1):
    if item_name in player_stats["inventory"]:
        player_stats["inventory"][item_name] += quantity
    else:
        player_stats["inventory"][item_name] = quantity

def remove_item_from_inventory(item_name, quantity=1):
    if item_name in player_stats["inventory"]:
        if player_stats["inventory"][item_name] >= quantity:
            player_stats["inventory"][item_name] -= quantity
            if player_stats["inventory"][item_name] <= 0:
                del player_stats["inventory"][item_name]
        else:
            return False
    else:
        return False
    return True

def equip_item(item_name):
    item_type = get_item_type(item_name)
    if item_type == "weapon":
        player_stats["equipment"]["weapon"] = item_name
    elif item_type == "armor":
        player_stats["equipment"]["armor"] = item_name

def unequip_item(item_name):
    item_type = get_item_type(item_name)
    if item_type == "weapon":
        player_stats["equipment"]["weapon"] = "Wooden Sword"
    elif item_type == "armor":
        player_stats["equipment"]["armor"] = "Leather Armor"

def combat(enemy_name):
    while player_stats["health"] > 0 and enemies[enemy_name]["health"] > 0:
        # Player's turn
        player_attack = player_stats["attack"] + get_item_damage(player_stats["equipment"]["weapon"])
        enemy_defense = enemies[enemy_name]["health"]
        damage_dealt = max(player_attack - enemy_defense, 1)
        enemies[enemy_name]["health"] -= damage_dealt
        print(f"You dealt {damage_dealt} damage to the {enemy_name}.")

        if enemies[enemy_name]["health"] <= 0:
            print(f"You defeated the {enemy_name}!")
            update_player_stats("experience", get_enemy_exp(enemy_name))
            update_player_stats("gold", get_enemy_gold(enemy_name))
            return

        # Enemy's turn
        enemy_attack = enemies[enemy_name]["damage"]
        player_defense = player_stats["defense"] + get_item_defense(player_stats["equipment"]["armor"])
        damage_taken = max(enemy_attack - player_defense, 1)
        update_player_stats("health", -damage_taken)
        print(f"The {enemy_name} dealt {damage_taken} damage to you.")

        if player_stats["health"] <= 0:
            print("You have been defeated.")
            return

def level_up():
    while player_stats["experience"] >= (player_stats["level"] * 100):
        update_player_stats("level", 1)
        update_player_stats("max_health", 20)
        update_player_stats("max_mana", 10)
        update_player_stats("attack", 2)
        update_player_stats("defense", 1)
        print(f"You leveled up to level {player_stats['level']}!")

def main():
    # Example usage
    print("Welcome to the game!")
    player_name = input("Enter your name: ")
    print(f"Hello, {player_name}!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Fight an enemy")
        print("2. Visit the Bazaar")
        print("3. Check your inventory")
        print("4. Equip/Unequip items")
        print("5. Travel to another island")
        print("6. Exit the game")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            enemy_name = random.choice(list(enemies.keys()))
            print(f"You encounter a {enemy_name}!")
            combat(enemy_name)
            level_up()
        elif choice == "2":
            print("Welcome to the Bazaar!")
            print("You have", player_stats["gold"], "gold.")
            print("What would you like to do?")
            print("1. Buy an item")
            print("2. Sell an item")
            bazaar_choice = input("Enter your choice (1-2): ")
            if bazaar_choice == "1":
                for item_name, item_data in items.items():
                    print(f"{item_name} - {item_data['price']} gold")
                buy_item = input("Enter the item you want to buy: ")
                if buy_item in items:
                    if player_stats["gold"] >= items[buy_item]["price"]:
                        update_player_stats("gold", -items[buy_item]["price"])
                        add_item_to_inventory(buy_item)
                        print(f"You bought a {buy_item}.")
                    else:
                        print("You don't have enough gold.")
                else:
                    print("Invalid item.")
            elif bazaar_choice == "2":
                for item_name, quantity in player_stats["inventory"].items():
                    print(f"{item_name} - {get_item_price(item_name)} gold (x{quantity})")
                sell_item = input("Enter the item you want to sell: ")
                if sell_item in player_stats["inventory"]:
                    update_player_stats("gold", get_item_price(sell_item))
                    remove_item_from_inventory(sell_item)
                    print(f"You sold a {sell_item}.")
                else:
                    print("You don't have that item in your inventory.")
            else:
                print("Invalid choice.")
        elif choice == "3":
            print("Your inventory:")
            for item_name, quantity in player_stats["inventory"].items():
                print(f"{item_name} (x{quantity})")
            print(f"Equipped weapon: {player_stats['equipment']['weapon']}")
            print(f"Equipped armor: {player_stats['equipment']['armor']}")
        elif choice == "4":
            print("Your inventory:")
            for item_name, quantity in player_stats["inventory"].items():
                print(f"{item_name} (x{quantity})")
            equip_item_name = input("Enter the item you want to equip: ")
            if equip_item_name in player_stats["inventory"]:
                equip_item(equip_item_name)
                print(f"You equipped {equip_item_name}.")
            else:
                print("You don't have that item in your inventory.")
            unequip_item_name = input("Enter the item you want to unequip: ")
            if unequip_item_name in player_stats["equipment"].values():
                unequip_item(unequip_item_name)
                print(f"You unequipped {unequip_item_name}.")
            else:
                print("You don't have that item equipped.")
        elif choice == "5":
            print("You travel to another island.")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
