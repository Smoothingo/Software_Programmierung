import customtkinter as ctk
from .widgets import ScrollableFrame, ActionButton, InventoryWindow
from .combat_window import CombatWindow
from .bazaar_window import BazaarWindow
from .equipment_window import EquipmentWindow


class MainWindow(ctk.CTk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Archipelago Adventure")
        self.geometry("1000x800")
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Header Frame
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        
        # Stats Display
        self.stats_label = ctk.CTkLabel(self.header_frame, font=("Arial", 12))
        self.stats_label.pack(side="left", padx=10)
        
        # Inventory Button
        ctk.CTkButton(self.header_frame, text="Inventory", command=self.show_inventory
                    ).pack(side="right", padx=10)
        
        # Main Content
        self.content_frame = ScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        # Action Buttons Frame
        self.actions_frame = ctk.CTkFrame(self.content_frame)
        self.actions_frame.pack(fill="x", pady=5)
        
        # Log Display
        self.log_text = ctk.CTkTextbox(self.content_frame, height=200)
        self.log_text.pack(fill="x", pady=10)
        self.log_text.configure(state="disabled")

    def update_display(self):
        # Update stats
        stats = self.game.player.get_stats()
        self.stats_label.configure(text=
            f"Level: {stats['level']} | XP: {stats['xp']} | "
            f"HP: {stats['health']} | ATK: {stats['attack']} | DEF: {stats['defense']}"
        )
        
        # Clear previous actions
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        # Add new actions
        location_info = self.game.get_current_location_info()
        for action in location_info['actions']:
            ActionButton(
                self.actions_frame,
                text=action['description'],
                command=lambda a=action: self.handle_action(a)
            ).pack(side="left", padx=5)
            
        # Update NPC dialogues
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        for npc in location_info.get('npcs', []):
            self.log_text.insert("end", f"{npc['name']}: {npc['dialogue']}\n")
        self.log_text.configure(state="disabled")

    def handle_action(self, action):
        result = self.game.handle_action(action)
        
        if result['type'] == "combat":
            CombatWindow(self, self.game, result['mob'])
        elif result['type'] == "bazaar":
            BazaarWindow(self, self.game)
        elif result['type'] == "inventory":
            self.show_inventory(result['data'])
        elif result['type'] == "message":
            self.show_message(result['text'])
        elif result['type'] == "location_change":
            self.update_display()
            
    def show_inventory(self, items=None):
        InventoryWindow(self, self.game.player)

    def show_message(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")