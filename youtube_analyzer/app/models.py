# youtube_analyzer/app/models.py

class VideoAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.String(20), unique=True, nullable=False)
    analysis_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content_summary = db.Column(db.JSON)
    detailed_analysis = db.Column(db.JSON)
    
    def __repr__(self):
        return f'<VideoAnalysis {self.video_id}>'