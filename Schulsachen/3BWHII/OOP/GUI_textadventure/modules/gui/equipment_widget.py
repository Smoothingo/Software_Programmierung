import customtkinter as ctk
from .fullscreen_widget import FullScreenWidget

class EquipmentWidget(FullScreenWidget):
    def __init__(self, master, game, on_close_callback):
        super().__init__(master, "Equipment Manager", on_close_callback)
        self.game = game
        self.on_close_callback = on_close_callback
        

        # Remove the header frame's close button (X)
        for widget in self.header_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()

        self.error_message = None  # To display inline error messages
        self.create_content()
        self.update_equipment()

    def create_content(self):
        # Configure grid layout for the main widget
        self.grid_rowconfigure(1, weight=1)  # Content area expands
        self.grid_rowconfigure(2, weight=0)  # Exit button stays at the bottom
        self.grid_columnconfigure(0, weight=1)

        # Stats display at the top
        self.stats_label = ctk.CTkLabel(
            self.header_frame,
            text="Loading stats...",
            font=("Arial", 18, "bold")
        )
        self.stats_label.pack(side="left", padx=10)

        # Error message display
        self.error_label = ctk.CTkLabel(
            self.header_frame,
            text="",
            font=("Arial", 14),
            text_color="red"
        )
        self.error_label.pack(side="right", padx=10)

        # Main content area (will expand)
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        self.main_content.grid_rowconfigure(0, weight=1)  # Items container expands
        self.main_content.grid_columnconfigure(0, weight=1)

        # Items container - scrollable and expands
        self.items_container = ctk.CTkScrollableFrame(
            self.main_content,
            fg_color="transparent"
        )
        self.items_container.grid(row=0, column=0, sticky="nsew")

        # Exit button at the very bottom (row 2)
        self.exit_button = ctk.CTkButton(
            self,
            text="Exit Equipment Manager",
            command=self.on_close_callback,
            height=40,
            font=("Arial", 14)
        )
        self.exit_button.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))

    def update_equipment(self):
        """Update the equipment display, including equipped items."""
        # Update stats display
        stats = self.game.player.get_stats()
        self.stats_label.configure(
            text=f"Level: {stats['level']} | XP: {stats['xp']}\n"
                f"Health: {stats['health']} | Attack: {stats['attack']} | Defense: {stats['defense']}\n"
                f"Equipped Sword: {stats['sword']} | Equipped Armor: {stats['armor']}"
        )

        # Clear existing items in the container
        for widget in self.items_container.winfo_children():
            widget.destroy()

        # Filter owned items by type (weapon or armor)
        owned_items = [
            item for item in self.game.player.inventory.items
            if item['type'] in ['weapon', 'armor']
        ]

        # Add equipped items to the list if they are not already in the inventory
        if self.game.player.equipped_sword and self.game.player.equipped_sword not in owned_items:
            owned_items.append(self.game.player.equipped_sword)
        if self.game.player.equipped_armor and self.game.player.equipped_armor not in owned_items:
            owned_items.append(self.game.player.equipped_armor)

        # Group items by type
        grouped_items = {"weapon": [], "armor": []}
        for item in owned_items:
            grouped_items[item['type']].append(item)

        # Display grouped items
        for group, items in grouped_items.items():
            if items:  # Only display the group if there are items
                group_label = ctk.CTkLabel(
                    self.items_container,
                    text=group.capitalize(),
                    font=("Arial", 16, "bold"),
                    anchor="w"
                )
                group_label.pack(fill="x", pady=5, padx=5)

                for item in items:
                    self.create_item_row(item)

    def create_item_row(self, item):
        item_frame = ctk.CTkFrame(self.items_container)
        item_frame.pack(fill="x", pady=2, padx=5)

        # Item Info
        ctk.CTkLabel(
            item_frame,
            text=item['name'],
            font=("Arial", 14),
            width=180,
            anchor="w"
        ).pack(side="left")

        # Display item stats (e.g., attack or defense)
        stats_text = ""
        if 'stats' in item:
            if 'attack' in item['stats']:
                stats_text += f"Attack: {item['stats']['attack']} "
            if 'defense' in item['stats']:
                stats_text += f"Defense: {item['stats']['defense']}"

        ctk.CTkLabel(
            item_frame,
            text=stats_text.strip(),
            font=("Arial", 13),
            width=150,
            anchor="w"
        ).pack(side="left")

        # Equip/Unequip Button
        if self.is_equipped(item):
            ctk.CTkButton(
                item_frame,
                text="Unequip",
                width=80,
                command=lambda: self.unequip_item(item)
            ).pack(side="right", padx=5)
        else:
            ctk.CTkButton(
                item_frame,
                text="Equip",
                width=80,
                command=lambda: self.equip_item(item)
            ).pack(side="right", padx=5)

    def is_equipped(self, item):
        """Check if the item is currently equipped."""
        if item['type'] == 'weapon' and self.game.player.equipped_sword == item:
            return True
        if item['type'] == 'armor' and self.game.player.equipped_armor == item:
            return True
        return False

    def equip_item(self, item):
        """Equip the selected item."""
        if item['type'] == 'weapon':
            if self.game.player.equipped_sword:
                self.show_error("You can only equip one sword at a time!")
                return
            self.game.player.equipped_sword = item
            self.game.player.attack += item['stats'].get('attack', 0)  # Add attack stat
            self.game.player.inventory.remove_item(item['id'], 1)  # Remove one from inventory

        elif item['type'] == 'armor':
            if self.game.player.equipped_armor:
                self.show_error("You can only equip one armor at a time!")
                return
            self.game.player.equipped_armor = item
            self.game.player.defense += item['stats'].get('defense', 0)  # Add defense stat
            self.game.player.inventory.remove_item(item['id'], 1)  # Remove one from inventory

        # Update stats and UI
        self.update_equipment()
        self.refresh_stats_display()
        self.clear_error()

    def unequip_item(self, item):
        """Unequip the selected item."""
        if item['type'] == 'weapon' and self.game.player.equipped_sword == item:
            self.game.player.attack -= item['stats'].get('attack', 0)  # Subtract attack stat
            self.game.player.equipped_sword = None
            self.game.player.inventory.add_item(item['id'], 1)  # Add back to inventory

        elif item['type'] == 'armor' and self.game.player.equipped_armor == item:
            self.game.player.defense -= item['stats'].get('defense', 0)  # Subtract defense stat
            self.game.player.equipped_armor = None
            self.game.player.inventory.add_item(item['id'], 1)  # Add back to inventory

        # Update stats and UI
        self.update_equipment()
        self.refresh_stats_display()
        self.clear_error()

    def show_error(self, message):
        """Display an inline error message."""
        self.error_label.configure(text=message)

    def clear_error(self):
        """Clear the inline error message."""
        self.error_label.configure(text="")
    
    def refresh_stats_display(self):
        # Update stats display
        stats = self.game.player.get_stats()
        self.stats_label.configure(
            text=f"Level: {stats['level']} | XP: {stats['xp']}\n"
                f"Health: {stats['health']} | Attack: {stats['attack']} | Defense: {stats['defense']}\n"
                f"Equipped Sword: {stats['sword']} | Equipped Armor: {stats['armor']}"
        )