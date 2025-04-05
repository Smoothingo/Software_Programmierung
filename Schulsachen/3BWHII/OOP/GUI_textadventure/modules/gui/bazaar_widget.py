import customtkinter as ctk
from .widgets import ScrollableFrame

class BazaarWidget(ctk.CTkFrame):
    def __init__(self, master, game, on_close_callback):
        super().__init__(master)
        self.game = game
        self.on_close = on_close_callback
        self.selected_quantities = {}  # Track selected quantities for each item
        self.create_widgets()
        self.update_bazaar()

    def create_widgets(self):
        """Create all UI elements (pure GUI)"""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Gold Display
        self.gold_label = ctk.CTkLabel(self, font=("Arial", 14, "bold"))
        self.gold_label.pack(pady=10)
        
        # Category Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Item Display Frame
        self.item_frame = ScrollableFrame(self.tabview)
        self.tabview.add("Items")
        self.tabview.tab("Items").grid_columnconfigure(0, weight=1)
        
        # Back Button
        ctk.CTkButton(
            self,
            text="Back",
            command=self.on_close
        ).pack(pady=10)

    def update_bazaar(self):
        """Update the bazaar UI (no game logic here)"""
        gold = self.game.player.inventory.get_gold()
        self.gold_label.configure(text=f"💰 Gold: {gold}")
        
        # Clear previous items
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        
        # Load items from game data
        for item_id, item in self.game.player.inventory.get_available_items().items():
            if item['type'] == 'currency':
                continue
            self.create_item_row(item_id, item)

    def create_item_row(self, item_id, item):
        """Create a single item row (UI only)"""
        item_frame = ctk.CTkFrame(self.item_frame)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Item Info
        ctk.CTkLabel(item_frame, text=item['name'],
                   font=("Arial", 12)).pack(side="left", padx=10)
        ctk.CTkLabel(item_frame, text=f"Value: {item['value']} Gold"
                   ).pack(side="left", padx=10)
        
        # Current quantity
        current_qty = self.game.player.inventory.get_item_quantity(item_id)
        qty_label = ctk.CTkLabel(item_frame, text=f"Owned: {current_qty}")
        qty_label.pack(side="left", padx=10)
        
        # Buy/Sell controls
        self.create_trade_controls(item_frame, item_id, item['value'], qty_label)

    def create_trade_controls(self, parent, item_id, value, qty_label):
        """Create buy/sell UI controls"""
        trade_frame = ctk.CTkFrame(parent)
        trade_frame.pack(side="right", padx=10)
        
        # Buy controls
        buy_frame = ctk.CTkFrame(trade_frame)
        buy_frame.pack(side="left", padx=5)
        self.create_quantity_controls(buy_frame, item_id, "buy", qty_label)
        
        # Sell controls
        sell_frame = ctk.CTkFrame(trade_frame)
        sell_frame.pack(side="left", padx=5)
        self.create_quantity_controls(sell_frame, item_id, "sell", qty_label)

    def create_quantity_controls(self, parent, item_id, action, qty_label):
        """Create quantity selector UI"""
        if (item_id, action) not in self.selected_quantities:
            self.selected_quantities[(item_id, action)] = 1
            
        # Quantity display
        qty_display = ctk.CTkLabel(parent, text=str(self.selected_quantities[(item_id, action)]))
        qty_display.pack(side="left", padx=5)
        
        # Decrease button
        ctk.CTkButton(parent, text="-", width=30,
            command=lambda: self.adjust_quantity(item_id, action, -1, qty_display)
        ).pack(side="left")
        
        # Increase button
        ctk.CTkButton(parent, text="+", width=30,
            command=lambda: self.adjust_quantity(item_id, action, 1, qty_display)
        ).pack(side="left")
        
        # Action button
        ctk.CTkButton(parent, text=action.capitalize(), width=60,
            command=lambda: self.execute_trade(item_id, action, qty_label)
        ).pack(side="left", padx=5)

    def adjust_quantity(self, item_id, action, change, qty_display):
        """Adjust selected quantity (UI only)"""
        key = (item_id, action)
        new_qty = max(1, self.selected_quantities[key] + change)
        self.selected_quantities[key] = new_qty
        qty_display.configure(text=str(new_qty))

    def execute_trade(self, item_id, action, qty_label):
        """Handle trade button click (delegates to game logic)"""
        quantity = self.selected_quantities[(item_id, action)]
        
        if action == "buy":
            success = self.game.player.inventory.buy_item(item_id, quantity)
        else:
            success = self.game.player.inventory.sell_item(item_id, quantity)
        
        if success:
            self.update_display(qty_label, item_id)

    def update_display(self, qty_label, item_id):
        """Refresh UI after trade"""
        current_qty = self.game.player.inventory.get_item_quantity(item_id)
        qty_label.configure(text=f"Owned: {current_qty}")
        self.update_bazaar()