import yt_dlp
from datetime import datetime

def extract_video_info(url):
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'writesubtitles': True,
            'allsubtitles': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            metadata = {
                # Basic Video Information
                'video_id': info.get('id', ''),
                'url': url,
                'title': info.get('title', ''),
                'description': info.get('description', ''),
                'upload_date': info.get('upload_date', ''),
                'modified_date': info.get('modified_date', ''),
                'duration': info.get('duration', 0),
                'language': info.get('language', ''),
                'audio_language': info.get('audio_language', ''),

                # Technical Details
                'format': info.get('format', ''),
                'format_id': info.get('format_id', ''),
                'ext': info.get('ext', ''),
                'filesize': info.get('filesize', 0),
                'filesize_approx': info.get('filesize_approx', 0),
                'video_codec': info.get('vcodec', ''),
                'audio_codec': info.get('acodec', ''),
                'width': info.get('width', 0),
                'height': info.get('height', 0),
                'fps': info.get('fps', 0),
                'audio_channels': info.get('audio_channels', 0),
                'loudness': info.get('loudness', 0),
                'subtitles': info.get('subtitles', {}),
                # 'automatic_captions': info.get('automatic_captions', {}),
                'is_live': info.get('is_live', False),
                'was_live': info.get('was_live', False),
                'live_status': info.get('live_status', ''),
                
                # Analytics and Statistics
                'view_count': info.get('view_count', 0),
                'like_count': info.get('like_count', 0),
                'dislike_count': info.get('dislike_count', 0),
                'comment_count': info.get('comment_count', 0),
                'repost_count': info.get('repost_count', 0),
                'average_rating': info.get('average_rating', 0),
                'age_limit': info.get('age_limit', 0),
                'availability': info.get('availability', ''),
                'geo_restriction': {
                    'blocked_countries': info.get('blocked_countries', []),
                    'allowed_countries': info.get('allowed_countries', [])
                },

                # Channel Information
                'channel': info.get('uploader', ''),
                'channel_id': info.get('channel_id', ''),
                'channel_url': info.get('channel_url', ''),
                'channel_follower_count': info.get('channel_follower_count', 0),
                'channel_description': info.get('channel_description', ''),
                'channel_banner': info.get('channel_banner', {}),
                
                # Media Assets
                'thumbnail_url': info.get('thumbnail', ''),
                # 'thumbnails': info.get('thumbnails', []),
                'watermark': info.get('watermark', ''),
                'preview_images': info.get('preview_images', []),
                'end_screen': info.get('end_screen', {}),

                # Additional Metadata
                'tags': info.get('tags', []),
                'categories': info.get('categories', []),
                'topics': info.get('topics', []),
                'chapters': info.get('chapters', []),
                'location': {
                    'latitude': info.get('latitude', None),
                    'longitude': info.get('longitude', None),
                    'location': info.get('location', ''),
                },
                'recording_date': info.get('recording_date', ''),
                'release_date': info.get('release_date', ''),
                'release_year': info.get('release_year', ''),
                'creator': info.get('creator', ''),
                'artist': info.get('artist', ''),
                'album': info.get('album', ''),
                'track': info.get('track', ''),
                'season_number': info.get('season_number', None),
                'episode_number': info.get('episode_number', None),
                'series': info.get('series', ''),
                'playlist': info.get('playlist', ''),
                'playlist_index': info.get('playlist_index', None),
                'license': info.get('license', ''),
                
                # Extraction Metadata
                'extractor': info.get('extractor', ''),
                'extractor_key': info.get('extractor_key', ''),
                'extracted_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return metadata
    except Exception as e:
        raise Exception(f"Error extracting video info: {str(e)}")