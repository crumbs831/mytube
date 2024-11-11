import os

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSV_FILE = os.path.join(BASE_DIR, 'youtube_metadata.csv')

    # Video analyzer settings
    TEMP_VIDEO_PATH = "youtube_analyzer/app/temp"
    SAMPLE_RATE = 1  # Frame sampling rate
    
    # Create temp directory if it doesn't exist
    import os
    os.makedirs(TEMP_VIDEO_PATH, exist_ok=True)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///youtube.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMP_VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'app', 'temp')