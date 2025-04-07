import json
import json
import random
from .player import Player
from .constants import get_resource_path

class Game:
    def __init__(self, player_name="Adventurer"):
        self.story = self.load_story(get_resource_path(r"modules\story_blocks.json"))
        self.player = Player(player_name, self)
        self.current_island = self.story['islands'][0]
        self.audio_thread = None

    def load_story(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get_current_location_info(self):
        return {
            'name': self.current_island['name'],
            'description': self.current_island['description'],
            'actions': self.current_island.get('actions', []),
            'npcs': self.current_island.get('npcs', [])
        }

    def handle_action(self, action):
        if action.get("response") == "// ask god who you are":
            return {"type": "message", "text": f"You are {self.player.name}, a brave adventurer!"}
        
        # Handle other action types
        if action.get("type") == "bazaar":
            return {"type": "bazaar", "success": True}

        if action.get("type") == "combat":
            mob_name = action.get("mob")
            mob = self.initiate_combat(mob_name)
            if mob:
                return {"type": "combat", "mob": mob}
            else:
                return {"type": "message", "text": f"No mob named {mob_name} found!"}

        if action.get("type") == "equipment":
            return {"type": "equipment", "success": True}
        
        if "next_location" in action:
            next_location = action["next_location"]
            if self.travel_to(next_location):  # Update the player's location first
                return {
                    "type": "location_change",
                    "text": self.get_current_location_info()["description"]
                }

        # Handle actions with a response
        if "response" in action:
            return {"type": "message", "text": action["response"]}

        # Handle adding items
        if "add_items" in action:
            for item_id, quantity in action["add_items"].items():
                self.player.inventory.add_item(int(item_id), quantity)

        # Handle removing items
        if "remove_items" in action:
            for item_id, quantity in action["remove_items"].items():
                self.player.inventory.remove_item(int(item_id), quantity)

        # Handle adding XP
        if "add_xp" in action:
            self.player.gain_xp(action["add_xp"])

        return {"type": "message", "text": action.get('response', 'Action completed')}

    def travel_to(self, island_name):
        island = next((i for i in self.story["islands"] if i['name'] == island_name), None)
        if island:
            self.current_island = island
            return True
        return False

    def initiate_combat(self, mob_name):
        mob = next((m for m in self.current_island.get('mobs', []) if m['name'] == mob_name), None)
        if mob:
            mob['stats']['max_health'] = mob['stats']['health']  # Store max health
            return mob
        return None

    def player_death(self):
        self.player.health = 0
        return {"type": "death"}

    def ender_dragon_defeated(self):
        self.travel_to("Hub Island")
        return {"type": "boss_defeated"}