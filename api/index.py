from flask import Flask, render_template_string, request
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# Store your API key securely (preferably as an environment variable)
YOUTUBE_API_KEY = 'AIzaSyBfCbZW4ci4azQVQOqN_h1T5YAJTcKdAtE'  # Replace with your actual API key

def get_video_id(url):
    if 'youtube.com/watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    return None

def get_video_info(video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    
    try:
        # Get video details
        video_response = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=video_id
        ).execute()

        if not video_response['items']:
            return None

        video_data = video_response['items'][0]
        
        return {
            'video_id': video_id,
            'title': video_data['snippet']['title'],
            'description': video_data['snippet']['description'][:1000],
            'view_count': video_data['statistics'].get('viewCount', 0),
            'like_count': video_data['statistics'].get('likeCount', 0),
            'channel': video_data['snippet']['channelTitle'],
            'published_at': video_data['snippet']['publishedAt'],
            'duration': video_data['contentDetails']['duration']
        }
    except Exception as e:
        print(f"Error fetching video info: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    embed_url = None
    metadata = None
    error = None

    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            video_id = get_video_id(url)
            if video_id:
                metadata = get_video_info(video_id)
                if metadata:
                    embed_url = f'https://www.youtube.com/embed/{video_id}'
                else:
                    error = "Could not fetch video information"
            else:
                error = "Invalid YouTube URL"

    return render_template_string(
        HTML_TEMPLATE,
        embed_url=embed_url,
        metadata=metadata,
        error=error
    )