import json
import os
from modules import Characters as ch

class JSON:
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
        if isinstance(value, list):
            for item in value:
                print(f"- {item}")
        else:
            print(value)

class AddItems:
    def __init__(self):
        self.items = []

    def add_item(self, item_key):
        item = self.load_item_from_json('lookup_table.json', item_key)
        self.items.append(item)
        print(f"{item['name']} wurde hinzugefügt!")

    def remove_item(self, item_key):
        item = next((item for item in self.items if item['name'] == item_key), None)
        if item:
            self.items.remove(item)
            print(f"{item['name']} wurde entfernt!")
        else:
            print(f"{item_key} nicht im Inventar gefunden!")

    @staticmethod
    def load_item_from_json(file_path, item_key):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['items'][item_key]

class Island(JSON):
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

    @staticmethod
    def load_islands_from_json(file_path):
        data = JSON.read_json(file_path)
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

class Start(JSON):
    def __init__(self):
        self.player = ch.Player(name="Default", level=1)

    def start(self):
        self.player.name = input("Enter your name: ")
        print(f"Hello {self.player.name}!")
        # Print the intro story from the JSON file
        data = self.read_json(os.path.join(os.path.dirname(__file__), 'story_blocks.json'))
        self.print_text_from_json(data, 'story.intro.title')
        self.print_text_from_json(data, 'story.intro.description')
        self.print_text_from_json(data, 'story.intro.objectives')