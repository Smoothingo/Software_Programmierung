import customtkinter as ctk
from .widgets import ScrollableFrame

class BazaarWindow(ctk.CTkToplevel):
    def __init__(self, master, game):
        super().__init__(master)
        self.title("Bazaar")
        self.geometry("800x600")
        self.game = game
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.create_widgets()
        self.update_bazaar()
    
    def create_widgets(self):
        # Gold Display
        self.gold_label = ctk.CTkLabel(self, font=("Arial", 14, "bold"))
        self.gold_label.pack(pady=10)
        
        # Category Tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Item Display
        self.item_frame = ScrollableFrame(self.tabview)
        self.tabview.add("Items")
        self.tabview.tab("Items").grid_columnconfigure(0, weight=1)
    
    def update_bazaar(self):
        gold = self.game.player.inventory.get_item_quantity(2)
        self.gold_label.configure(text=f"💰 Gold: {gold}")
        
        # Clear previous items
        for widget in self.item_frame.winfo_children():
            widget.destroy()
        
        # Load items
        items = self.game.player.inventory.load_item_data()
        for item_id, item in items.items():
            if item['type'] == 'currency': continue
            
            item_frame = ctk.CTkFrame(self.item_frame)
            item_frame.pack(fill="x", pady=5, padx=5)
            
            # Item Info
            ctk.CTkLabel(item_frame, text=item['name'], 
                       font=("Arial", 12)).pack(side="left", padx=10)
            ctk.CTkLabel(item_frame, text=item['description']
                       ).pack(side="left", padx=10)
            ctk.CTkLabel(item_frame, text=f"Value: {item['value']} Gold"
                       ).pack(side="left", padx=10)
            
            # Trade Buttons
            btn_frame = ctk.CTkFrame(item_frame)
            btn_frame.pack(side="right", padx=10)
            
            ctk.CTkButton(btn_frame, text="Buy", width=60,
                        command=lambda iid=item_id: self.trade_item(iid, "buy")
                        ).pack(side="left", padx=2)
            ctk.CTkButton(btn_frame, text="Sell", width=60,
                        command=lambda iid=item_id: self.trade_item(iid, "sell")
                        ).pack(side="left", padx=2)
    
    def trade_item(self, item_id, action):
        TradeDialog(self, self.game, int(item_id), action)