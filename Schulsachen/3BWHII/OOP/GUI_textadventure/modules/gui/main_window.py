import customtkinter as ctk
from .widgets import ScrollableFrame, ActionButton, InventoryWindow
from .combat_window import CombatWindow
from .bazaar_widget import BazaarWidget
from .equipment_widget import EquipmentWidget


class MainWindow(ctk.CTk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Archipelago Adventure")
        self.geometry("1000x800")
        
        # Configure grid layout (3 columns)
        self.grid_columnconfigure(0, weight=0)  # Sidebar
        self.grid_columnconfigure(1, weight=1)   # Main content
        self.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
        self.update_display()

    def create_widgets(self):
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=300)
        self.sidebar_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        
        # Inventory Section
        ctk.CTkLabel(self.sidebar_frame, text="Inventory", font=("Arial", 14, "bold")).pack(pady=10)
        self.inventory_scroll = ScrollableFrame(self.sidebar_frame)
        self.inventory_scroll.pack(fill="both", expand=True, padx=5)

        # Header Frame (main content area)
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")
        
        # Stats Display
        self.stats_label = ctk.CTkLabel(self.header_frame, font=("Arial", 12))
        self.stats_label.pack(side="left", padx=10)
        
        # Main Content
        self.content_container = ctk.CTkFrame(self)  # New container
        self.content_container.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)
        self.content_container.grid_columnconfigure(0, weight=1)
    
        self.content_frame = ScrollableFrame(self.content_container, height=650)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
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
        
        # Update inventory
        self.update_inventory_display()
        
        # Clear previous action buttons FIRST
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        # Add new actions from current location
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

    def update_inventory_display(self):
        # Clear existing inventory items
        for widget in self.inventory_scroll.winfo_children():
            widget.destroy()
        
        # Add current inventory items
        for item in self.game.player.inventory.get_formatted_inventory():
            item_frame = ctk.CTkFrame(self.inventory_scroll)
            item_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                item_frame, 
                text=f"{item['name']} x{item['quantity']}",
                width=120,
                anchor="w"
            ).pack(side="left", padx=5)
            
            ctk.CTkLabel(
                item_frame, 
                text=f"💰 {item['value']}",  
                width=100,
                anchor="e"  # Right-aligned for numbers
            ).pack(side="right", padx=5)

    def handle_action(self, action):
        result = self.game.handle_action(action)
        
        if result['type'] == "combat":
            CombatWindow(self, self.game, result['mob'])
        elif result['type'] == "bazaar":
            self.show_bazaar()
        elif result['type'] == "equipment":
            self.show_equipment_manager()  # Show the EquipmentWidget
        elif result['type'] == "message":
            self.show_message(result['text'])
        elif result['type'] == "location_change":
            self.update_display()  # Full refresh for location changes
        
        # Always update stats and inventory after any action
        self.refresh_ui()  # Add this line
        
        return result  # If you need to return the result

    def refresh_ui(self):
        """Update only the dynamic elements without recreating action buttons"""
        # Update stats
        stats = self.game.player.get_stats()
        self.stats_label.configure(text=
            f"Level: {stats['level']} | XP: {stats['xp']} | "
            f"HP: {stats['health']} | ATK: {stats['attack']} | DEF: {stats['defense']}"
        )
        
        # Update inventory
        self.update_inventory_display()

    def show_bazaar(self):
        # Hide all main content
        self.sidebar_frame.grid_remove()
        self.header_frame.grid_remove()
        self.content_container.grid_remove()
        
        # Create fullscreen bazaar
        self.bazaar_widget = BazaarWidget(
            self,
            self.game,
            on_close_callback=self.return_to_main_view
        )
        self.bazaar_widget.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")

    def return_to_main_view(self):
        if hasattr(self, 'bazaar_widget'):
            self.bazaar_widget.destroy()
        if hasattr(self, 'equipment_widget'):
            self.equipment_widget.destroy()
        self.sidebar_frame.grid()
        self.header_frame.grid()
        self.content_container.grid()

    def show_equipment_manager(self):
        # Hide all main content
        self.sidebar_frame.grid_remove()
        self.header_frame.grid_remove()
        self.content_container.grid_remove()

        # Create fullscreen equipment manager
        self.equipment_widget = EquipmentWidget(
            self,
            self.game,
            on_close_callback=self.return_to_main_view
        )
        self.equipment_widget.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")

    def show_message(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")