
from modules.game_logic.game import Game
from modules.gui.main_window import MainWindow


class App:
    def __init__(self):
        # Initialize the game with a default player name
        self.game = Game("Adventurer")
        
        # Create the main application window
        self.main_window = MainWindow(self.game)
        
        # Link the main window to the game
        self.game.main_window = self.main_window
        
        # Start the main application loop
        self.main_window.mainloop()
if __name__ == "__main__":
    App()
    