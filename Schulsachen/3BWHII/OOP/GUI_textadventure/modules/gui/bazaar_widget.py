import customtkinter as ctk
from .fullscreen_widget import FullScreenWidget
from modules.game_logic.constants import get_resource_path
from PIL import Image
from customtkinter import CTkImage
from modules.gui.widgets import TransparentScrollableFrame

class BazaarWidget(FullScreenWidget):
    def __init__(self, master, game, on_close_callback):
        super().__init__(master, "Bazaar", on_close_callback)
        self.game = game
        self.selected_quantity = 1
        self.on_close_callback = on_close_callback

        try:
            image_path = get_resource_path("modules/extras/bazaar_backround.jpg")
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
            self.bg_image = CTkImage(light_image=bg_image, size=(self.winfo_screenwidth(), self.winfo_screenheight()))

            # Create a label to display the background image
            self.bg_label = ctk.CTkLabel(self, image=self.bg_image, text="")
            self.bg_label.place(relwidth=1, relheight=1)  # Stretch to fill the entire widget
        except FileNotFoundError:
            print(f"Background image not found at {image_path}")


        # Remove the header frame's close button (X)
        for widget in self.header_frame.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()

        self.create_content()
        self.update_bazaar()

    def create_content(self):
        # Configure grid layout for the main widget
        self.grid_rowconfigure(1, weight=1)  # Content area expands
        self.grid_rowconfigure(2, weight=0)  # Exit button stays at the bottom
        self.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))

        self.gold_label = ctk.CTkLabel(
            self.header_frame,
            text=f"💰 {self.game.player.inventory.get_gold()} Gold",
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        self.gold_label.pack(side="left", padx=10)


        # Main content area (will expand)
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 10))
        self.main_content.grid_rowconfigure(0, weight=1)  # Items container expands
        self.main_content.grid_columnconfigure(0, weight=1)

        # Items container - scrollable and expands
        self.items_container = TransparentScrollableFrame(
            self.main_content
        )
        self.items_container.grid(row=0, column=0, sticky="nsew")

        # Exit button at the very bottom (row 2)
        self.exit_button = ctk.CTkButton(
            self,
            text="Exit Bazaar",
            command=self.on_close_callback,
            height=40,
            font=("Arial", 14)
        )
        self.exit_button.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))

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
            # Skip gold item (ID 2)
            if int(item_id) == 2:
                continue
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

        ctk.CTkButton(
            item_frame,
            text="Sell All",
            command=lambda iid=item_id: self.execute_trade(iid, "sell_all", qty_label),
            width=80
        ).pack(side="right", padx=5)

    def execute_trade(self, item_id, action, qty_label):
        if action == "buy":
            success = self.game.player.inventory.buy_item(item_id, self.selected_quantity)
        elif action == "sell":
            success = self.game.player.inventory.sell_item(item_id, self.selected_quantity)
        elif action == "sell_all":
            success = self.game.player.inventory.sell_all_items(item_id)
            

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