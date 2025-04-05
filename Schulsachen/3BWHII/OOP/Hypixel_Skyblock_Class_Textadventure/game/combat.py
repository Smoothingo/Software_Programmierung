import random
import time
import customtkinter
import pygame

# Error handling for audio file loading
try:
    pygame.mixer.init()
    pygame.mixer.music.load("audio/battle_music.mp3")
except pygame.error:
    print("Error loading audio file. Continuing without sound.")

class CombatSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.combat_log = []

    def start_combat(self):
        pygame.mixer.music.play(-1)  # Play battle music on loop

        while self.player.health > 0 and self.enemy.health > 0:
            self.player_turn()
            if self.enemy.health > 0:
                self.enemy_turn()

        pygame.mixer.music.stop()  # Stop battle music

        if self.player.health <= 0:
            self.combat_log.append("You have been defeated.")
            return False
        else:
            self.combat_log.append(f"You have defeated the {self.enemy.name}!")
            self.player.gain_xp(self.enemy.xp_reward)
            return True

    def player_turn(self):
        print("Your turn!")
        self.combat_log.append("Your turn!")

        action = input("What do you want to do? (attack/item/run) ")

        if action == "attack":
            damage = self.player.attack(self.enemy)
            self.combat_log.append(f"You dealt {damage} damage to the {self.enemy.name}.")
            print(f"You dealt {damage} damage to the {self.enemy.name}.")
        elif action == "item":
            # Implement item usage logic
            pass
        elif action == "run":
            if random.random() < 0.5:
                self.combat_log.append("You successfully fled the battle.")
                print("You successfully fled the battle.")
                return
            else:
                self.combat_log.append("You failed to flee the battle.")
                print("You failed to flee the battle.")

    def enemy_turn(self):
        print(f"The {self.enemy.name} attacks!")
        self.combat_log.append(f"The {self.enemy.name} attacks!")

        damage = self.enemy.attack(self.player)
        self.combat_log.append(f"The {self.enemy.name} dealt {damage} damage to you.")
        print(f"The {self.enemy.name} dealt {damage} damage to you.")

        if self.player.health <= 0:
            self.combat_log.append("You have been defeated.")

    def display_combat_log(self):
        for message in self.combat_log:
            print(message)

class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100
        self.attack_power = 10
        self.defense = 5
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100

    def attack(self, enemy):
        damage = self.attack_power - enemy.defense
        if damage < 0:
            damage = 0
        enemy.health -= damage
        return damage

    def gain_xp(self, xp_amount):
        self.xp += xp_amount
        print(f"You gained {xp_amount} XP!")

        if self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp_to_next_level *= 2
        self.attack_power += 2
        self.defense += 1
        self.health += 20
        print(f"You leveled up to level {self.level}!")

class Enemy:
    def __init__(self, name, health, attack_power, defense, xp_reward):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.xp_reward = xp_reward

    def attack(self, player):
        damage = self.attack_power - player.defense
        if damage < 0:
            damage = 0
        player.health -= damage
        return damage

# Example usage
player = Player("Adventurer")
enemy = Enemy("Slime", 50, 5, 2, 20)

combat_system = CombatSystem(player, enemy)
combat_system.start_combat()
combat_system.display_combat_log()
