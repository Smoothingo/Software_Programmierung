import customtkinter as ctk
from .fullscreen_widget import FullScreenWidget
from PIL import Image, ImageTk
from customtkinter import CTkImage
from modules.game_logic.constants import get_resource_path

class CombatWidget(FullScreenWidget):
    def __init__(self, master, game, mob, on_close_callback):
        super().__init__(master, f"Combat - {mob['name']}", on_close_callback)
        self.game = game
        self.mob = mob
        self.on_close_callback = on_close_callback

        self.create_content()
        self.update_display()

    def create_content(self):
        # Configure grid layout
        self.grid_rowconfigure(1, weight=1)  # Main content area
        self.grid_rowconfigure(2, weight=0)  # Action buttons
        self.grid_columnconfigure(0, weight=1)

        # Top bar for health, strength, and defense
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)
        self.top_bar.grid_columnconfigure(0, weight=1)
        self.top_bar.grid_columnconfigure(1, weight=1)

        # Mob stats bar (now on the left)
        self.mob_stats = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.mob_stats.grid(row=0, column=0, sticky="nsew", padx=10)
        self.mob_health_bar = ctk.CTkProgressBar(self.mob_stats, width=200)
        self.mob_health_bar.pack(pady=5)
        self.mob_health_label = ctk.CTkLabel(self.mob_stats, text=f"{self.mob['name']} HP: 100/100")
        self.mob_health_label.pack()

        # Player stats bar (now on the right)
        self.player_stats = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.player_stats.grid(row=0, column=1, sticky="nsew", padx=10)
        self.player_health_bar = ctk.CTkProgressBar(self.player_stats, width=200)
        self.player_health_bar.pack(pady=5)
        self.player_health_label = ctk.CTkLabel(self.player_stats, text="Player HP: 100/100")
        self.player_health_label.pack()

        # Main content area
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_content.grid_columnconfigure(0, weight=1)
        self.main_content.grid_columnconfigure(1, weight=1)

        # Mob image on the left
        self.mob_image_label = ctk.CTkLabel(self.main_content, text="")
        self.mob_image_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.load_mob_image()

        # Interactive fighting display on the right
        self.fight_display = ctk.CTkFrame(self.main_content, fg_color="transparent")
        self.fight_display.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.fight_display.grid_rowconfigure(0, weight=1)
        self.fight_display.grid_rowconfigure(1, weight=0)

        # Combat log
        self.combat_log = ctk.CTkTextbox(self.fight_display, height=300)
        self.combat_log.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.combat_log.configure(state="disabled")

        # Action buttons
        self.action_buttons = ctk.CTkFrame(self.fight_display, fg_color="transparent")
        self.action_buttons.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        self.create_action_buttons()

    def create_action_buttons(self):
        # Clear existing buttons
        for widget in self.action_buttons.winfo_children():
            widget.destroy()

        # Add default action buttons
        ctk.CTkButton(self.action_buttons, text="Attack", command=self.player_attack).pack(side="left", padx=5)

        # Only show "Use Potion" if the player has potions
        if self.game.player.inventory.get_item(5) and self.game.player.inventory.get_item(5)['quantity'] > 0:
            ctk.CTkButton(self.action_buttons, text="Use Potion", command=self.use_potion).pack(side="left", padx=5)

        ctk.CTkButton(self.action_buttons, text="Run", command=self.on_close_callback).pack(side="left", padx=5)

    def create_victory_buttons(self):
        # Clear existing buttons
        for widget in self.action_buttons.winfo_children():
            widget.destroy()

        # Add victory buttons
        ctk.CTkButton(self.action_buttons, text="Attack Another", command=self.attack_another).pack(side="left", padx=5)
        ctk.CTkButton(self.action_buttons, text="Go Back", command=self.on_close_callback).pack(side="left", padx=5)


    def load_mob_image(self):
        # Load and display the mob image
        try:
            image_path = get_resource_path(f"modules/extras/{self.mob['name'].lower().replace(' ', '_')}.jpg")
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.Resampling.LANCZOS)  # Resize and stretch to fit
            self.mob_image = CTkImage(light_image=image, dark_image=image, size=(300, 300))  # Use CTkImage
            self.mob_image_label.configure(image=self.mob_image)
        except FileNotFoundError:
            self.mob_image_label.configure(text="No Image Available")

    def update_display(self, message=None):
        # Update player and mob health bars
        player_health = self.game.player.health
        player_max_health = self.game.player.base_health
        self.player_health_bar.set(player_health / player_max_health)
        self.player_health_label.configure(text=f"Player HP: {player_health}/{player_max_health}")

        mob_health = self.mob['stats']['health']
        mob_max_health = self.mob['stats']['max_health']
        self.mob_health_bar.set(mob_health / mob_max_health)
        self.mob_health_label.configure(text=f"{self.mob['name']} HP: {mob_health}/{mob_max_health}")

        # Update combat log
        if message:
            self.combat_log.configure(state="normal")
            self.combat_log.insert("end", message + "\n")
            self.combat_log.see("end")
            self.combat_log.configure(state="disabled")

    def player_attack(self):
        # Player attacks the mob
        damage = max(0, self.game.player.attack - self.mob['stats']['defense'])
        self.mob['stats']['health'] -= damage
        self.update_display(f"You dealt {damage} damage to {self.mob['name']}!")

        # Check if the mob is defeated
        if self.mob['stats']['health'] <= 0:
            self.mob_defeated()
            return

        # Mob retaliates
        self.mob_attack()

    def mob_attack(self):
        # Mob attacks the player
        damage = max(0, self.mob['stats']['attack'] - self.game.player.defense)
        self.game.player.health -= damage
        self.update_display(f"{self.mob['name']} dealt {damage} damage to you!")

        # Check if the player is defeated
        if self.game.player.health <= 0:
            self.player_defeated()

    def mob_defeated(self):
        # Handle mob defeat
        self.update_display(f"You defeated {self.mob['name']}!")
        rewards = self.mob.get('add_items', {})
        xp = self.mob.get('add_xp', 0)  # Get XP from the mob's data

        # Add rewards to the player's inventory
        for item_id, quantity in rewards.items():
            print(f"Adding item to inventory: ID={item_id}, Quantity={quantity}")  # Debug statement
            self.game.player.inventory.add_item(int(item_id), quantity)  # Ensure item_id is an integer

        # Add XP to the player
        self.game.player.gain_xp(xp)

        # Display rewards
        reward_text = "Rewards:\n"
        for item_id, quantity in rewards.items():
            item = self.game.player.inventory.item_data[str(item_id)]
            reward_text += f"  - {item['name']} x{quantity} 🏆\n"
        reward_text += f"  - XP: {xp} ⭐"
        self.update_display(reward_text)

        # Replace action buttons with victory options
        self.create_victory_buttons()

    def player_defeated(self):
        # Handle player defeat
        self.update_display("You have been defeated! Game Over.")
        self.master.show_death_screen()
        

    def use_potion(self):
        # Check if the player has potions
        potion = self.game.player.inventory.get_item(5)  # Assuming item ID 5 is a healing potion
        if potion and potion['quantity'] > 0:
            self.game.player.inventory.remove_item(5, 1)  # Remove one potion
            self.game.player.health = min(
                self.game.player.health + potion['stats']['heal'], 
                self.game.player.base_health
            )
            self.update_display("You used a healing potion!")
        else:
            self.update_display("You don't have any healing potions!")
        
        # Update the UI
        self.update_display()
        self.create_action_buttons()  # Refresh buttons to hide "Use Potion" if no potions are left

    def attack_another(self):
        # Restart combat with the same mob type
        self.mob['stats']['health'] = self.mob['stats']['max_health']
        self.update_display(f"A new {self.mob['name']} appears!")
        self.create_action_buttons()