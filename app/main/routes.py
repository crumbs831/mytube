from flask import render_template, request
from app.main import bp
from app.services.youtube_service import extract_video_info
from app.services.csv_service import video_exists_in_csv, save_to_csv

@bp.route('/', methods=['GET', 'POST'])
def index():
    embed_url = None
    error = None
    url = None
    metadata = None
    csv_file = None
    message = None

    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if url:
            try:
                metadata = extract_video_info(url)
                video_id = metadata['video_id']
                embed_url = f'https://www.youtube.com/embed/{video_id}'
                
                if video_exists_in_csv(video_id):
                    message = f"Video {video_id} already exists in database"
                else:
                    csv_file, is_new = save_to_csv(metadata)
                    message = "New video metadata added to database"
                
            except Exception as e:
                error = str(e)

    return render_template(
        'main/index.html',
        embed_url=embed_url,
        error=error,
        url=url,
        metadata=metadata,
        csv_file=csv_file,
        message=message
    )