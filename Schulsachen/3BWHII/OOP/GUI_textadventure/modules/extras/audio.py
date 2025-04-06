# modules/services/audio.py
import pygame
import threading

class AudioService:
    @staticmethod
    def play_async(file_path):
        def play():
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
        thread = threading.Thread(target=play)
        thread.start()