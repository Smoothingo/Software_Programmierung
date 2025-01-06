# from os import environ
# import os

# import pygame
# environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
# def play_audio(file_path_music: str):
#     absolute_path = os.path.abspath(file_path_music)
#     if not os.path.exists(absolute_path):
#         print(f"File not found: {absolute_path}")
#         return
#     pygame.mixer.init()
#     pygame.mixer.music.load(absolute_path)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

# play_audio(r"modules\music\byebye.mp3")

import time
def faster_print(text: str, delay: float = 0.07):
    """
    Prints text faster than slow_print, character by character.

    Args:
        text (str): The text to print.
        delay (float): The delay between each character.
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

name = "John"   
faster_print(f"hello world {name}")