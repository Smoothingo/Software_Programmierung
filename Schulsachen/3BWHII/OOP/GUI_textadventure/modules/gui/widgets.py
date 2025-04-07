import customtkinter as ctk

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._parent_frame.configure(height=600,)  # Force minimum height

class TransparentScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color="transparent")  # Make the frame transparent
        
class ActionButton(ctk.CTkButton):
    def __init__(self, master, text, command):
        super().__init__(
            master,
            text=text,
            command=command,
            corner_radius=8,
            fg_color="#2A2D2E",
            hover_color="#3B3F41",
            height=40
        )

class InventoryWindow(ctk.CTkToplevel):
    def __init__(self, master, player):
        super().__init__(master)
        self.player = player
        self.title("Inventory")
        self.geometry("400x600")
        
        self.scroll_frame = ScrollableFrame(self)
        self.scroll_frame.pack(fill="both", expand=True)
        
        self.update_inventory()
    
    def update_inventory(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        for item in self.player.inventory.get_formatted_inventory():
            frame = ctk.CTkFrame(self.scroll_frame)
            frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(frame, text=f"{item['name']} x{item['quantity']}"
                        ).pack(side="left", padx=5)
            ctk.CTkLabel(frame, text=f"{item['value']}"            
                        ).pack(side="left", padx=5)