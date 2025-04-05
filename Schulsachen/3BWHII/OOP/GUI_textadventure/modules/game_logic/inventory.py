import json

class Inventory:
    def __init__(self):
        self.items = []
        
    def add_item(self, item_id, quantity=1):
        item = self.load_item_data(item_id)
        existing = next((i for i in self.items if i['id'] == item_id), None)
        if existing:
            existing['quantity'] += quantity
        else:
            item['quantity'] = quantity
            self.items.append(item)
    
    def remove_item(self, item_id, quantity=1):
        item = next((i for i in self.items if i['id'] == item_id), None)
        if item:
            if item['quantity'] > quantity:
                item['quantity'] -= quantity
            else:
                self.items.remove(item)
    
    def load_item_data(self, item_id):
        with open("modules/lookuptable.json", 'r') as f:
            items = json.load(f)['items']
            return items[str(item_id)]
    
    def get_formatted_inventory(self):
        return [{
            'id': item['id'],
            'name': item['name'],
            'quantity': item['quantity'],
            'description': item['description']
        } for item in self.items]