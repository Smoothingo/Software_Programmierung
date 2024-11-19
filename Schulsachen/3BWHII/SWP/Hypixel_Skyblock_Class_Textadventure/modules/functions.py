import json
from modules import Characters as ch


class Island:
    def __init__(self, name, description, npcs, resources, actions):
        self.name = name
        self.description = description
        self.npcs = npcs
        self.resources = resources
        self.actions = actions

    def enter(self):
        print(f"Entering {self.name}: {self.description}")

    def list_npcs(self):
        for npc in self.npcs:
            print(f"{npc['name']} - {npc['role']}")

    def list_resources(self):
        for resource in self.resources:
            print(resource)

    def load_islands_from_json(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        islands = []
        for island_data in data['story']['islands']:
            island = Island(
        name=island_data['name'],
        description=island_data['description'],
        npcs=island_data['npcs'],
        resources=island_data['resources'],
        actions=island_data['actions']
)
        islands.append(island)
        return islands


class Start:
    def __init__(self):
        self.player = ch.Player()

    def start(self):
        self.player()
        self.player.add_start_item()
        

    @staticmethod
    def read_json(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def print_text_from_json(data, key_path):
        keys = key_path.split('.')
        value = data
        for key in keys:
            value = value[key]
        print(value)
    
    def add_start_item(self):
        item = self.load_item_from_json('lookup_table.json', 'wooden_sword')
        self.inventory.append(item)
