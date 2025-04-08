import json
from .constants import get_resource_path

class Inventory:
    def __init__(self, game):
        self.game = game
        self.items = []
        self.item_data = self.load_all_items()
        
    def add_item(self, item_id, quantity=1):
        item_id = int(item_id)  # Ensure item_id is always an integer
        item_data = self.item_data[str(item_id)]  # Access loaded item data
        existing = next((i for i in self.items if i['id'] == item_id), None)
        
        if existing:
            existing['quantity'] += quantity  # Add directly to the existing quantity
        else:
            new_item = {
                'id': item_data['id'],
                'name': item_data['name'],
                'quantity': quantity,  # Use the provided quantity
                'description': item_data['description'],
                'value': item_data['value'],
                'type': item_data['type']
            }
            if 'stats' in item_data:
                new_item['stats'] = item_data['stats']
            self.items.append(new_item)
        
        # Notify the GUI to update the UI
        if hasattr(self, 'on_inventory_update'):
            self.on_inventory_update()

    def get_formatted_inventory(self):
        return [{
            'id': item['id'],
            'name': item['name'],
            'quantity': item['quantity'],
            'description': item['description'],
            'value': item['value']
        } for item in self.items]
    
    def remove_item(self, item_id, quantity=1):
        item = next((i for i in self.items if i['id'] == item_id), None)
        if item:
            if item['quantity'] > quantity:
                item['quantity'] -= quantity
            else:
                self.items.remove(item)
        
    def get_total_value(self):
        return sum(item['quantity'] * item['value'] for item in self.items)

    def get_item_quantity(self, item_id):
        item = next((i for i in self.items if i['id'] == item_id), None)
        return item['quantity'] if item else 0
        
    def load_all_items(self):
        with open(get_resource_path(r"modules/lookuptable.json"), 'r') as f:
            return json.load(f)['items']
    
    def buy_item(self, item_id, quantity):
        """Game logic for buying an item"""
        item = self.item_data[str(item_id)]
        total_cost = item['value'] * quantity
        if self.get_item_quantity(2) >= total_cost:  # 2 = Gold ID
            self.remove_item(2, total_cost)
            self.add_item(item_id, quantity)
            return True
        return False

    def sell_item(self, item_id, quantity):
        """Game logic for selling an item"""

        if self.is_item_unsellable(item_id):
            return False, True
        
        item = self.item_data[str(item_id)]
        total_value = item['value'] * quantity
        if self.get_item_quantity(item_id) >= quantity:
            self.remove_item(item_id, quantity)
            self.add_item(2, total_value)  # 2 = Gold ID
            return True, False
        return False, False
    
    def sell_all_items(self, item_id):
        """Sell all quantities of the specified item."""
        

        if self.is_item_unsellable(item_id):
            return False, 0, 0, True
        
        item = next((i for i in self.items if i['id'] == item_id), None)
        if item:
            quantity = item['quantity']
            total_value = item['value'] * quantity
            self.add_item(2, total_value)  # Add gold to the player's inventory (2 = Gold ID)
            self.items.remove(item)  # Remove the item from the inventory
            return True, quantity, total_value, False
        return False, 0, 0, False
    
    def is_item_unsellable(self, item_id):
        """Check if the item is equipped and cannot be sold."""
        equipped_items = [
            self.game.player.equipped_sword,
            self.game.player.equipped_armor
        ]
        # Check if the item is equipped and selling it would leave none
        for equipped_item in equipped_items:
            if equipped_item and equipped_item['id'] == item_id:
                current_quantity = self.get_item_quantity(item_id)
                if current_quantity <= 1:
                    return True  # Item is unsellable
        return False  # Item can be sold
    
    def get_gold(self):
        return self.get_item_quantity(2)
        
    def get_item(self, item_id):
        """Retrieve an item from the inventory by its ID."""
        return next((item for item in self.items if item['id'] == item_id), None)
        
    
