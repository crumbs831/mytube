from flask import Flask, render_template_string, request
from googleapiclient.discovery import build
import os

app = Flask(__name__)

# Define HTML_TEMPLATE at the top, before any routes
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Analyzer</title>
    <style>
        body { 
            background: black; 
            color: white; 
            font-family: Arial; 
            text-align: center; 
            padding: 20px; 
        }
        input { 
            width: 300px; 
            padding: 10px; 
            margin: 10px; 
        }
        button { 
            background: red; 
            color: white; 
            border: none; 
            padding: 10px 20px; 
            cursor: pointer; 
        }
        .error { color: red; }
    </style>
</head>
<body>
    <h1>YouTube Video Analyzer</h1>
    <form method="POST">
        <input type="text" name="url" placeholder="Enter YouTube URL">
        <button type="submit">Analyze</button>
    </form>
    {% if error %}
        <p class="error">{{ error }}</p>
    {% endif %}
    {% if embed_url %}
        <iframe width="560" height="315" src="{{ embed_url }}" frameborder="0" allowfullscreen></iframe>
    {% endif %}
    {% if metadata %}
        <pre>{{ metadata | tojson(indent=2) }}</pre>
    {% endif %}
</body>
</html>
'''

# Get API key from environment variable
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_video_id(url):
    """Extract video ID from URL"""
    if 'youtube.com/watch?v=' in url:
        return url.split('watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        return url.split('youtu.be/')[1].split('?')[0]
    return None

def get_video_info(video_id):
    """Get video information using YouTube API"""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        response = youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        if not response['items']:
            return None

        video = response['items'][0]
        return {
            'title': video['snippet']['title'],
            'views': video['statistics'].get('viewCount', 0),
            'likes': video['statistics'].get('likeCount', 0),
            'channel': video['snippet']['channelTitle'],
            'published': video['snippet']['publishedAt']
        }
    except Exception as e:
        print(f"API Error: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if not url:
            return render_template_string(HTML_TEMPLATE, error="Please enter a URL")

        video_id = get_video_id(url)
        if not video_id:
            return render_template_string(HTML_TEMPLATE, error="Invalid YouTube URL")

        if not YOUTUBE_API_KEY:
            return render_template_string(HTML_TEMPLATE, error="YouTube API key not configured")

        metadata = get_video_info(video_id)
        if not metadata:
            return render_template_string(HTML_TEMPLATE, error="Could not fetch video information")

        return render_template_string(
            HTML_TEMPLATE,
            embed_url=f"https://www.youtube.com/embed/{video_id}",
            metadata=metadata
        )

    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)