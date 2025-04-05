import customtkinter as ctk
import random
from .widgets import ActionButton

class CombatWindow(ctk.CTkToplevel):
    def __init__(self, master, game, mob):
        super().__init__(master)
        self.game = game
        self.mob = mob
        self.title(f"Combat - {mob['name']}")
        self.geometry("600x400")
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Combat Info
        self.info_text = ctk.CTkTextbox(self, wrap="word")
        self.info_text.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Action Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)
        
        ActionButton(btn_frame, text="Attack", command=self.player_attack
                   ).pack(side="left", padx=5)
        ActionButton(btn_frame, text="Use Item", command=self.use_item
                   ).pack(side="left", padx=5)
        ActionButton(btn_frame, text="Run", command=self.destroy
                   ).pack(side="left", padx=5)

    def player_attack(self):
        player_dmg = max(0, random.randint(5,15) + self.game.player.attack - self.mob['stats']['defense'])
        self.mob['stats']['health'] -= player_dmg
        self.update_display(f"You deal {player_dmg} damage!")
        
        if self.mob['stats']['health'] <= 0:
            self.victory()
            return
            
        enemy_dmg = max(0, random.randint(0, self.mob['stats']['attack']) - self.game.player.defense)
        self.game.player.health -= enemy_dmg
        self.update_display(f"{self.mob['name']} deals {enemy_dmg} damage!")
        
        if self.game.player.health <= 0:
            self.defeat()

    def update_display(self, message=None):
        self.info_text.configure(state="normal")
        self.info_text.delete("1.0", "end")
        self.info_text.insert("end",
            f"{self.mob['name']}\n"
            f"Health: {self.mob['stats']['health']}\n"
            f"Your Health: {self.game.player.health}\n\n"
        )
        if message:
            self.info_text.insert("end", message + "\n")
        self.info_text.configure(state="disabled")

    def victory(self):
        self.update_display(f"You defeated {self.mob['name']}!")
        self.game.handle_action({'add_items': self.mob['drops']})
        self.after(2000, self.destroy)

    def defeat(self):
        self.update_display("You have been defeated!")
        self.after(2000, self.game.player_death)
        self.destroy()