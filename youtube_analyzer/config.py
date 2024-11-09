import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSV_FILE = os.path.join(BASE_DIR, 'youtube_metadata.csv')