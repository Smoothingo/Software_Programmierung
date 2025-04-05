import os
import pygame

def load_audio_files(audio_dir):
    """
    Load all audio files from the specified directory.
    
    Args:
        audio_dir (str): The directory containing the audio files.
    
    Returns:
        dict: A dictionary mapping audio file names to their corresponding Pygame Sound objects.
    """
    audio_files = {}
    
    try:
        for filename in os.listdir(audio_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(audio_dir, filename)
                audio_files[os.path.splitext(filename)[0]] = pygame.mixer.Sound(file_path)
    except FileNotFoundError:
        print(f"Error: Audio directory '{audio_dir}' not found.")
    except pygame.error as e:
        print(f"Error loading audio file: {e}")
    
    return audio_files
