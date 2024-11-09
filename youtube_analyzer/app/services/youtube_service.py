import yt_dlp
from datetime import datetime

def extract_video_info(url):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            metadata = {
                'video_id': info.get('id', ''),
                'url': url,
                'title': info.get('title', ''),
                'description': info.get('description', '')[:1000],
                'view_count': info.get('view_count', 0),
                'like_count': info.get('like_count', 0),
                'duration': info.get('duration', 0),
                'channel': info.get('uploader', ''),
                'channel_id': info.get('channel_id', ''),
                'upload_date': info.get('upload_date', ''),
                'thumbnail_url': info.get('thumbnail', ''),
                'tags': ', '.join(info.get('tags', [])) if info.get('tags') else '',
                'categories': ', '.join(info.get('categories', [])) if info.get('categories') else '',
                'extracted_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return metadata
    except Exception as e:
        raise Exception(f"Error extracting video info: {str(e)}")