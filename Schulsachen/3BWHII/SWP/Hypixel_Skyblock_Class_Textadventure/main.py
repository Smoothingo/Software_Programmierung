from modules.game import Game

if __name__ == "__main__":
    story_file_path = r"modules\story_blocks.json"
    game = Game(story_file_path)
    game.start()