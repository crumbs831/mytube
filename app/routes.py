from flask import Blueprint, render_template, request, jsonify
from app.video_analyzer import VideoAnalyzer
from youtube_analyzer.app.services.youtube_service import extract_video_info
from youtube_analyzer.app.services.csv_service import video_exists_in_csv, save_to_csv
import os

main = Blueprint('main', __name__)
analyzer = VideoAnalyzer()

@main.route('/', methods=['GET', 'POST'])
def index():
    embed_url = None
    error = None
    url = None
    metadata = None
    csv_file = None
    message = None
    analysis_report = None

    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        
        if url:
            try:
                # Extract basic metadata
                metadata = extract_video_info(url)
                video_id = metadata['video_id']
                embed_url = f'https://www.youtube.com/embed/{video_id}'
                
                # Check if video exists and save metadata
                if video_exists_in_csv(video_id):
                    message = f"Video {video_id} already exists in database"
                    csv_file = os.path.join(os.getcwd(), 'youtube_metadata.csv')
                else:
                    csv_file, is_new = save_to_csv(metadata)
                    message = "New video metadata added to database"
                
                # Perform video analysis if requested
                if request.form.get('analyze', False):
                    analysis = analyzer.analyze_video(url)
                    analysis_report = analyzer.generate_report(analysis)
                
            except Exception as e:
                error = str(e)
                print(f"Error processing request: {str(e)}")

    return render_template(
        'index.html',
        embed_url=embed_url,
        error=error,
        url=url,
        metadata=metadata,
        csv_file=csv_file,
        message=message,
        analysis_report=analysis_report
    )

@main.route('/analyze_video/<video_id>', methods=['GET'])
def analyze_video(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        analysis = analyzer.analyze_video(url)
        report = analyzer.generate_report(analysis)
        
        # Save analysis to CSV
        if not video_exists_in_csv(video_id):
            metadata = extract_video_info(url)
            metadata['analysis'] = report
            save_to_csv(metadata)
        
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@main.route('/get_analysis/<video_id>', methods=['GET'])
def get_analysis(video_id):
    try:
        # Check if analysis exists in database
        if video_exists_in_csv(video_id):
            # Implement logic to retrieve existing analysis
            pass
        
        # If not, perform new analysis
        url = f"https://www.youtube.com/watch?v={video_id}"
        analysis = analyzer.analyze_video(url)
        report = analyzer.generate_report(analysis)
        
        return jsonify(report)
    except Exception as e:
        return jsonify({'error': str(e)}), 400