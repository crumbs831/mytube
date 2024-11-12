import csv
import os
from flask import current_app

def get_csv_path():
    return current_app.config['CSV_FILE']

def video_exists_in_csv(video_id):
    csv_file = get_csv_path()
    # ... rest of the function remains the same
    try:
        if not os.path.exists(csv_file):
            return False
            
        if os.path.getsize(csv_file) == 0:
            return False

        with open(csv_file, 'r', encoding='utf-8') as f:
            headers = f.readline().strip().split(',')
            if 'video_id' not in headers:
                return False
            
            for line in f:
                if video_id in line:
                    return True
            
        return False
            
    except Exception as e:
        print(f"Error checking CSV: {str(e)}")
        return False

def save_to_csv(metadata):
    csv_file = current_app.config['CSV_FILE']
    try:
        if video_exists_in_csv(metadata['video_id']):
            return csv_file, False

        os.makedirs(os.path.dirname(csv_file), exist_ok=True)
        file_exists = os.path.exists(csv_file) and os.path.getsize(csv_file) > 0

        fields = [
            'video_id', 'url', 'title', 'description', 'view_count', 
            'like_count', 'duration', 'channel', 'channel_id', 
            'upload_date', 'thumbnail_url', 'tags', 'categories', 
            'extracted_date'
        ]

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            
            if not file_exists:
                writer.writeheader()
            
            row_data = {field: metadata.get(field, '') for field in fields}
            writer.writerow(row_data)
        
        return csv_file, True
        
    except Exception as e:
        print(f"Error saving to CSV: {str(e)}")
        raise Exception(f"Error saving to CSV: {str(e)}")