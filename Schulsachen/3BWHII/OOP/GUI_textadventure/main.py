import customtkinter as ctk
from modules.game_logic.game import Game
from modules.gui.main_window import MainWindow

class App:
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        self.game = Game()
        self.main_window = MainWindow(self.game)
        self.main_window.mainloop()

if __name__ == "__main__":
    App()