import os
import pickle

def save_game(player, inventory, islands, current_island):
    """Save the current game state to a file."""
    try:
        with open("game_save.pkl", "wb") as f:
            pickle.dump((player, inventory, islands, current_island), f)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game():
    """Load the game state from a file."""
    try:
        if os.path.exists("game_save.pkl"):
            with open("game_save.pkl", "rb") as f:
                player, inventory, islands, current_island = pickle.load(f)
            print("Game loaded successfully!")
            return player, inventory, islands, current_island
        else:
            print("No saved game found.")
            return None, None, None, None
    except Exception as e:
        print(f"Error loading game: {e}")
        return None, None, None, None
