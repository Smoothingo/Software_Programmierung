import customtkinter as ctk
import tkinter as tk
from typing import Callable, Dict, Any
from tkinter import ttk


class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Adventure")
        self.root.geometry("1024x768")
        
        # Configure grid layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Create main frames
        self.create_header_frame()
        self.create_main_frame()
        self.create_action_frame()
        
        # Initialize callback storage
        self.action_callbacks: Dict[str, Callable] = {}
        
    def create_header_frame(self):
        """Creates the header frame with player stats"""
        self.header_frame = ctk.CTkFrame(self.root)
        self.header_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        # Player stats labels
        self.health_label = ctk.CTkLabel(self.header_frame, text="❤️ Health: 100/100")
        self.health_label.pack(side="left", padx=10)
        
        self.xp_label = ctk.CTkLabel(self.header_frame, text="🔋 XP: 0/100")
        self.xp_label.pack(side="left", padx=10)
        
        self.level_label = ctk.CTkLabel(self.header_frame, text="🆙 Level: 1")
        self.level_label.pack(side="left", padx=10)
        
        self.gold_label = ctk.CTkLabel(self.header_frame, text="💰 Gold: 0")
        self.gold_label.pack(side="left", padx=10)
        
    def create_main_frame(self):
        """Creates the main frame with the text output"""
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        
        # Create text widget for game output
        self.text_widget = ctk.CTkTextbox(self.main_frame, wrap="word", font=("Courier", 12))
        self.text_widget.pack(fill="both", expand=True, padx=5, pady=5)
        self.text_widget.configure(state="disabled")
        
    def create_action_frame(self):
        """Creates the action frame with buttons"""
        self.action_frame = ctk.CTkFrame(self.root)
        self.action_frame.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
    def update_actions(self, actions):
        """Updates the action buttons based on current available actions"""
        # Clear existing buttons
        for widget in self.action_frame.winfo_children():
            widget.destroy()
            
        # Create new buttons for each action
        for i, action in enumerate(actions):
            btn = ctk.CTkButton(
                self.action_frame,
                text=action['description'],
                command=lambda a=action: self.handle_action(a)
            )
            btn.pack(side="left", padx=5, pady=5)
            
    def handle_action(self, action):
        """Handles button clicks for actions"""
        if action['id'] in self.action_callbacks:
            self.action_callbacks[action['id']]()
            
    def register_action_callback(self, action_id: str, callback: Callable):
        """Registers a callback for an action"""
        self.action_callbacks[action_id] = callback
        
    def update_text(self, text: str):
        """Updates the main text display"""
        self.text_widget.configure(state="normal")
        self.text_widget.insert("end", text + "\n")
        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")
        
    def update_stats(self, health: int, max_health: int, xp: int, level: int, gold: int):
        """Updates the player stats display"""
        self.health_label.configure(text=f"❤️ Health: {health}/{max_health}")
        self.xp_label.configure(text=f"🔋 XP: {xp}/{level * 100}")
        self.level_label.configure(text=f"🆙 Level: {level}")
        self.gold_label.configure(text=f"💰 Gold: {gold}")
        
    def show_popup(self, title: str, message: str):
        """Shows a popup dialog"""
        popup = ctk.CTkToplevel(self.root)
        popup.title(title)
        popup.geometry("300x200")
        
        label = ctk.CTkLabel(popup, text=message)
        label.pack(pady=20)
        
        button = ctk.CTkButton(popup, text="OK", command=popup.destroy)
        button.pack(pady=10)

    def create_bazaar_window(self, items, buy_callback, sell_callback):
        """Creates a new window for the bazaar interface"""
        bazaar_window = ctk.CTkToplevel(self.root)
        bazaar_window.title("Bazaar")
        bazaar_window.geometry("600x400")

        # Create notebook for categories
        notebook = ttk.Notebook(bazaar_window)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs for each category
        for category, category_items in items.items():
            if category_items:
                frame = ctk.CTkFrame(notebook)
                notebook.add(frame, text=category.capitalize())

                for item_id, item in category_items.items():
                    item_frame = ctk.CTkFrame(frame)
                    item_frame.pack(fill='x', padx=5, pady=2)

                    # Item name and description
                    ctk.CTkLabel(item_frame, text=f"{item['name']} - {item['value']} Gold").pack(side='left', padx=5)

                    # Quantity spinbox
                    quantity_var = tk.StringVar(value='1')
                    quantity_frame = ctk.CTkFrame(item_frame)
                    quantity_frame.pack(side='right', padx=5)

                    ctk.CTkButton(quantity_frame, text="-", width=30,
                                command=lambda v=quantity_var: v.set(str(max(1, int(v.get()) - 1)))
                                ).pack(side='left', padx=2)

                    ctk.CTkEntry(quantity_frame, textvariable=quantity_var, width=50).pack(side='left', padx=2)

                    ctk.CTkButton(quantity_frame, text="+", width=30,
                                command=lambda v=quantity_var: v.set(str(int(v.get()) + 1))
                                ).pack(side='left', padx=2)

                    ctk.CTkButton(item_frame, text="Buy", command=lambda i=item_id, q=quantity_var: buy_callback(i, int(q.get()))).pack(side='right', padx=5)
                    ctk.CTkButton(item_frame, text="Sell", command=lambda i=item_id, q=quantity_var: sell_callback(i, int(q.get()))).pack(side='right', padx=5)

    def create_equipment_window(self, current_equipment, available_equipment, equip_callback):
        """Creates a window for equipment management"""
        equipment_window = ctk.CTkToplevel(self.root)
        equipment_window.title("Equipment Management")
        equipment_window.geometry("400x300")

        # Current equipment display
        current_frame = ctk.CTkFrame(equipment_window)
        current_frame.pack(fill='x', padx=10, pady=5)
        ctk.CTkLabel(current_frame, text="Current Equipment:").pack()
        ctk.CTkLabel(current_frame, text=f"Weapon: {current_equipment['weapon'] or 'None'}").pack()
        ctk.CTkLabel(current_frame, text=f"Armor: {current_equipment['armor'] or 'None'}").pack()

        # Equipment selection
        selection_frame = ctk.CTkFrame(equipment_window)
        selection_frame.pack(fill='x', padx=10, pady=5)

        # Weapon dropdown
        weapon_var = tk.StringVar(value=current_equipment['weapon'] or "None")
        weapon_menu = ctk.CTkOptionMenu(selection_frame, variable=weapon_var,
                                      values=["None"] + [w['name'] for w in available_equipment['weapons']])
        weapon_menu.pack(pady=5)

        # Add similar code for armor dropdown and equip button
