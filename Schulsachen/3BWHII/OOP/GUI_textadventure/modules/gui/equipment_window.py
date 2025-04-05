import customtkinter as ctk
from .widgets import ScrollableFrame

class EquipmentWindow(ctk.CTkToplevel):
    def __init__(self, master, player):
        super().__init__(master)
        self.title("Equipment Manager")
        self.geometry("600x400")
        self.player = player
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
        self.update_equipment()
    
    def create_widgets(self):
        # Stats Display
        self.stats_label = ctk.CTkLabel(self, font=("Arial", 14))
        self.stats_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Equipment Frame
        self.equipment_frame = ScrollableFrame(self)
        self.equipment_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
    def update_equipment(self):
        stats = self.player.get_stats()
        self.stats_label.configure(
            text=f"Level: {stats['level']} | XP: {stats['xp']}\n"
                 f"Health: {stats['health']} | Attack: {stats['attack']} | Defense: {stats['defense']}\n"
                 f"Equipped Sword: {stats['sword']}\n"
                 f"Equipped Armor: {stats['armor']}"
        )
        
        # Add equipment management UI here