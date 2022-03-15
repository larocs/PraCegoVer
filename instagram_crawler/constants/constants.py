import os
from pathlib import Path

# paths
ROOT_DIR = os.path.dirname(Path(__file__).parent)

IMAGES_DIR_PATH = os.path.join(ROOT_DIR, "images")

POST_FILE_PATH = os.path.join(ROOT_DIR, "generated_files/posts.json")
PROFILE_FILE_PATH = os.path.join(ROOT_DIR, "generated_files/profiles.bin")
TOTAL_OF_POSTS_FILE = os.path.join(ROOT_DIR, "generated_files/total_latest.bin")

COOKIES_PATH = os.path.join(ROOT_DIR, "generated_files/cookies")

# Constants
HASHTAG = "#pracegover"
