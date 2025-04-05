import json

class Inventory:
    def __init__(self):
        self.items = []
        self.item_data = self.load_all_items()
        
    def add_item(self, item_id, quantity=1):
        item_data = self.item_data[str(item_id)]  # Access loaded item data
        existing = next((i for i in self.items if i['id'] == item_id), None)
        
        if existing:
            existing['quantity'] += item_data['base_quantity'] * quantity
        else:
            new_item = {
                'id': item_data['id'],
                'name': item_data['name'],
                'quantity': item_data['base_quantity'] * quantity,
                'description': item_data['description'],
                'value': item_data['value'],
                'type': item_data['type']
            }
            if 'stats' in item_data:
                new_item['stats'] = item_data['stats']
            self.items.append(new_item)

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
        with open("modules/lookuptable.json", 'r') as f:
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
        item = self.item_data[str(item_id)]
        total_value = item['value'] * quantity
        if self.get_item_quantity(item_id) >= quantity:
            self.remove_item(item_id, quantity)
            self.add_item(2, total_value)  # 2 = Gold ID
            return True
        return False
    
    def get_gold(self):
        return self.get_item_quantity(2)
    
    def load_all_items(self):
        with open("modules/lookuptable.json", 'r') as f:
            return json.load(f)['items']
    
    
