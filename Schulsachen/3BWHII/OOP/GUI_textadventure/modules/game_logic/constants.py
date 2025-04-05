import os

# Path constants
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORY_PATH = os.path.join(BASE_DIR, "story_blocks.json")
LOOKUP_TABLE_PATH = os.path.join(BASE_DIR, "lookuptable.json")
AUDIO_DIR = os.path.join(BASE_DIR, "modules", "audio")
ASCII_DIR = os.path.join(BASE_DIR, "modules", "ascii")