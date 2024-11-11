from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # Configure app for Vercel environment
    app.config['CSV_FILE'] = '/tmp/youtube_metadata.csv'  # Use Vercel's temp directory
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app