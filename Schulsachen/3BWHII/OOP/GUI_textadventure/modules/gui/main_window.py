import customtkinter as ctk
from .widgets import ScrollableFrame,TransparentScrollableFrame, ActionButton, InventoryWindow
from .combat_widget import CombatWidget
from .bazaar_widget import BazaarWidget
from .equipment_widget import EquipmentWidget


class MainWindow(ctk.CTk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("Archipelago Adventure")
        self.geometry("1200x800")  # Set the initial window size
        self.grid_rowconfigure(1, weight=1)  # Allow the main content to expand  # Set the initial window size to 1200px height
        self.grid_columnconfigure(1, weight=1)
        
        # Start with the name input screen
        self.show_name_input()

    def show_name_input(self):
        """Display the name input screen."""
        self.name_input_frame = ctk.CTkFrame(self)
        self.name_input_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        ctk.CTkLabel(self.name_input_frame, text="Enter your name:", font=("Arial", 16)).pack(pady=10)
        self.name_entry = ctk.CTkEntry(self.name_input_frame, width=200)
        self.name_entry.pack(pady=10)
        
        ctk.CTkButton(self.name_input_frame, text="Start Adventure", command=self.submit_name).pack(pady=10)

    def submit_name(self):
        """Handle name submission and transition to the main game UI."""
        name = self.name_entry.get().strip()
        if name:
            self.game.player.name = name  # Set the player's name
            self.name_input_frame.destroy()  # Remove the name input frame
            self.initialize_main_ui()  # Initialize the main game UI
        else:
            ctk.CTkLabel(self.name_input_frame, text="Name cannot be empty!", text_color="red").pack(pady=5)

    def initialize_main_ui(self):
        """Initialize the main game UI."""
        self.grid_columnconfigure(0, weight=1)  # Sidebar
        self.grid_columnconfigure(1, weight=30)  # Main content area
        self.grid_rowconfigure(1, weight=1)  # Header

        # Create the main UI components
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
        self.content_container = ctk.CTkFrame(self)
        self.content_container.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")
        self.content_container.grid_rowconfigure(0, weight=1)  # Allow content to expand vertically
        self.content_container.grid_columnconfigure(0, weight=1)  # Allow content to expand horizontally

        self.content_frame = TransparentScrollableFrame(self.content_container, height=650)
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
        # Action Buttons Frame
        self.actions_frame = ctk.CTkFrame(self.content_container)
        self.actions_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Log Display
        self.log_text = ctk.CTkTextbox(self.content_container, fg_color="transparent")
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
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
        """Handle player actions."""
        result = self.game.handle_action(action)


        if action.get("description") == "Talk with Jerry":
            # Show Jerry's introduction
            self.show_message(action["response"])

            # Add items and XP
            if "add_items" in action:
                for item_id, quantity in action["add_items"].items():
                    self.game.player.inventory.add_item(int(item_id), quantity)
            if "add_xp" in action:
                self.game.player.gain_xp(action["add_xp"])

            # Clear action buttons
            self.clear_widgets()

            # Show the "Explore" button
            self.show_explore_button(action.get("next_location"))
            return  # Stop further processing to avoid traveling immediately

        if result["type"] == "location_change":
            # Update the UI for the new location
            self.update_display()
            self.show_message(result["text"])  # Display the new location's description

        elif result["type"] == "message":
            self.show_message(result["text"])

        elif result["type"] == "combat":
            self.show_combat(result["mob"])

        elif result["type"] == "bazaar":
            self.show_bazaar()

        elif result["type"] == "equipment":
            self.show_equipment_manager()  # Open the equipment manager

    def clear_display(self):
        """Clear the log and action buttons."""
        # Clear the log
        self.log_text.configure(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.configure(state="disabled")
        
        # Clear action buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

    def clear_widgets(self):
        
        # Clear action buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

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
        if hasattr(self, 'combat_widget'):
            self.combat_widget.destroy()
        self.sidebar_frame.grid()
        self.header_frame.grid()
        self.content_container.grid()
        self.refresh_ui()

    def show_equipment_manager(self):
        """Open the equipment manager."""
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

    def show_combat(self, mob):
        # Hide all main content
        self.sidebar_frame.grid_remove()
        self.header_frame.grid_remove()
        self.content_container.grid_remove()

        # Create fullscreen combat widget
        self.combat_widget = CombatWidget(
            self,
            self.game,
            mob,
            on_close_callback=self.return_to_main_view  # Ensure this is passed correctly
        )
        self.combat_widget.grid(row=0, column=0, columnspan=2, rowspan=2, sticky="nsew")

   
    def show_explore_button(self, next_location):
        """Show the 'Ready to Explore' button."""
        # Add a message to the log
        self.log_text.configure(state="normal")
        self.log_text.insert("end", "\n\n[Click 'Ready to Explore' to continue your journey.]\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

        # Create the button
        self.ready_button = ctk.CTkButton(
            self.content_container,
            text="Ready to Explore",
            command=lambda: self.travel_to_location(next_location)
        )
        # Use grid instead of pack
        self.ready_button.grid(row=1, column=0, pady=10, sticky="nsew")

    def travel_to_location(self, location_name):
        # Remove the button
        self.ready_button.destroy()

        # Travel to the new location
        self.game.travel_to(location_name)
        self.update_display()
        self.show_message(self.game.get_current_location_info()['description'])