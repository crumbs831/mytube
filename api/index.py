# api/index.py
from flask import Flask, render_template_string, request
import yt_dlp

app = Flask(__name__)

# Minimize HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>YouTube Analyzer</title></head>
<body style="background:black;color:white;text-align:center">
    <form method="POST">
        <input name="url" placeholder="YouTube URL">
        <button>Analyze</button>
    </form>
    {% if embed_url %}
        <iframe width="560" height="315" src="{{ embed_url }}" frameborder="0" allowfullscreen></iframe>
    {% endif %}
    {% if metadata %}<pre>{{ metadata | tojson(indent=2) }}</pre>{% endif %}
</body>
</html>
'''

def extract_video_info(url):
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'video_id': info.get('id', ''),
            'title': info.get('title', ''),
            'views': info.get('view_count', 0)
        }

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        if url:
            try:
                metadata = extract_video_info(url)
                return render_template_string(
                    HTML_TEMPLATE,
                    embed_url=f"https://www.youtube.com/embed/{metadata['video_id']}",
                    metadata=metadata
                )
            except Exception as e:
                return f"Error: {str(e)}"
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run()