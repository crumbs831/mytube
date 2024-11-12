# youtube_analyzer/app/utils.py

import os
import shutil
from config import Config

def cleanup_temp_files():
    try:
        shutil.rmtree(Config.TEMP_VIDEO_PATH)
        os.makedirs(Config.TEMP_VIDEO_PATH)
    except Exception as e:
        logging.error(f"Cleanup failed: {str(e)}")