import customtkinter as ctk
from .fullscreen_widget import FullScreenWidget

class BazaarWidget(FullScreenWidget):
    def __init__(self, master, game, on_close_callback):
        super().__init__(master, "Bazaar", on_close_callback)
        self.game = game
        self.selected_quantity = 1
        self.create_content()
        self.update_bazaar()
        
        # Configure grid layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def create_content(self):
        # Configure content frame grid
        self.content_frame.grid_rowconfigure(1, weight=1)  # For items container
        self.content_frame.grid_columnconfigure(0, weight=1)

        # Gold display
        self.gold_frame = ctk.CTkFrame(self.content_frame)
        self.gold_frame.grid(row=0, column=0, sticky="ew", pady=5)
        self.gold_label = ctk.CTkLabel(
            self.gold_frame, 
            text="💰 Loading gold...",
            font=("Arial", 18, "bold")
        )
        self.gold_label.pack(side="left", padx=10)

        # Items container with scroll
        self.items_container = ctk.CTkScrollableFrame(self.content_frame)
        self.items_container.grid(row=1, column=0, sticky="nsew", pady=5)

        # Exit button at bottom
        exit_button = ctk.CTkButton(
            self.content_frame,
            text="Exit Bazaar",
            command=self.on_close,
            height=40,
            font=("Arial", 14)
        )
        exit_button.grid(row=2, column=0, sticky="ew", pady=10)

        # Configure grid weights
        self.content_frame.grid_rowconfigure(1, weight=1)  # Items container expands

    def adjust_quantity(self, change):
        self.selected_quantity = max(1, self.selected_quantity + change)
        self.qty_display.configure(text=str(self.selected_quantity))

    def update_bazaar(self):
        self.update_gold_display()
        self.update_item_display()

    def update_gold_display(self):
        self.gold_label.configure(text=f"💰 {self.game.player.inventory.get_gold()} Gold")

    def update_item_display(self):
        for widget in self.items_container.winfo_children():
            widget.destroy()
        
        items = self.game.player.inventory.item_data
        for item_id, item in items.items():
            self.create_item_row(int(item_id), item)

    def create_item_row(self, item_id, item):
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
        
        ctk.CTkLabel(
            item_frame,
            text=f"{item['value']} Gold",
            font=("Arial", 13),
            width=100
        ).pack(side="left")
        
        current_qty = self.game.player.inventory.get_item_quantity(item_id)
        qty_label = ctk.CTkLabel(
            item_frame,
            text=f"Owned: {current_qty}",
            font=("Arial", 13),
            width=100
        )
        qty_label.pack(side="left")
        
        # Action buttons
        btn_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(
            btn_frame,
            text="Buy",
            width=80,
            command=lambda iid=item_id: self.execute_trade(iid, "buy", qty_label)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Sell",
            width=80,
            command=lambda iid=item_id: self.execute_trade(iid, "sell", qty_label)
        ).pack(side="left", padx=5)

    def execute_trade(self, item_id, action, qty_label):
        if action == "buy":
            success = self.game.player.inventory.buy_item(item_id, self.selected_quantity)
        else:
            success = self.game.player.inventory.sell_item(item_id, self.selected_quantity)
        
        if success:
            self.update_gold_display()
            current_qty = self.game.player.inventory.get_item_quantity(item_id)
            qty_label.configure(text=f"Owned: {current_qty}")
            
            # Update parent inventory display
            parent = self.master
            while not hasattr(parent, 'update_inventory_display') and hasattr(parent, 'master'):
                parent = parent.master
            if hasattr(parent, 'update_inventory_display'):
                parent.update_inventory_display()