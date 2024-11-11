import yt_dlp
import cv2
import numpy as np
import speech_recognition as sr
from moviepy.editor import VideoFileClip
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForObjectDetection
from transformers import pipeline
import os

class VideoAnalyzer:
    def __init__(self):
        # Initialize models
        self.scene_detector = pipeline("zero-shot-image-classification")
        self.object_detector = AutoModelForObjectDetection.from_pretrained("facebook/detr-resnet-50")
        self.image_processor = AutoImageProcessor.from_pretrained("facebook/detr-resnet-50")
        self.transcriber = sr.Recognizer()
        
    def download_video(self, url, output_path="temp_video"):
        """Download video for processing"""
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_path}/%(id)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return f"{output_path}/{info['id']}.{info['ext']}"

    def extract_frames(self, video_path, sample_rate=1):
        """Extract frames from video at given sample rate"""
        frames = []
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            if frame_count % sample_rate == 0:
                frames.append(frame)
            frame_count += 1
            
        cap.release()
        return frames

    def analyze_frame(self, frame):
        """Analyze a single frame for objects and scene content"""
        # Convert frame to PIL Image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        # Process image for object detection
        inputs = self.image_processor(images=image, return_tensors="pt")
        outputs = self.object_detector(**inputs)
        
        # Scene classification
        scene_results = self.scene_detector(
            image,
            candidate_labels=["indoor", "outdoor", "day", "night", "urban", "nature"]
        )
        
        return {
            "objects": outputs,
            "scene": scene_results
        }

    def extract_audio(self, video_path):
        """Extract audio from video and transcribe"""
        video = VideoFileClip(video_path)
        audio_path = "temp_audio.wav"
        video.audio.write_audiofile(audio_path)
        
        with sr.AudioFile(audio_path) as source:
            audio = self.transcriber.record(source)
            try:
                transcript = self.transcriber.recognize_google(audio)
            except sr.UnknownValueError:
                transcript = "Could not understand audio"
            except sr.RequestError:
                transcript = "Could not request results"
                
        os.remove(audio_path)
        return transcript

    def analyze_video(self, url):
        """Complete video analysis"""
        try:
            # Download video
            video_path = self.download_video(url)
            
            # Analysis results
            analysis = {
                "frames_analysis": [],
                "audio_transcript": "",
                "summary": {
                    "detected_objects": set(),
                    "dominant_scenes": {},
                    "duration": 0,
                    "frame_count": 0
                }
            }
            
            # Extract and analyze frames
            frames = self.extract_frames(video_path)
            analysis["summary"]["frame_count"] = len(frames)
            
            for frame in frames:
                frame_analysis = self.analyze_frame(frame)
                analysis["frames_analysis"].append(frame_analysis)
                
                # Update summary
                for obj in frame_analysis["objects"]:
                    analysis["summary"]["detected_objects"].add(obj)
                for scene in frame_analysis["scene"]:
                    if scene["label"] in analysis["summary"]["dominant_scenes"]:
                        analysis["summary"]["dominant_scenes"][scene["label"]] += 1
                    else:
                        analysis["summary"]["dominant_scenes"][scene["label"]] = 1
            
            # Audio analysis
            analysis["audio_transcript"] = self.extract_audio(video_path)
            
            # Clean up
            os.remove(video_path)
            
            return analysis
            
        except Exception as e:
            raise Exception(f"Error analyzing video: {str(e)}")

    def generate_report(self, analysis):
        """Generate a human-readable report from analysis"""
        report = {
            "content_summary": {
                "duration": analysis["summary"]["duration"],
                "frame_count": analysis["summary"]["frame_count"],
                "main_objects": list(analysis["summary"]["detected_objects"]),
                "dominant_scenes": analysis["summary"]["dominant_scenes"],
                "transcript": analysis["audio_transcript"]
            },
            "detailed_analysis": {
                "frame_by_frame": analysis["frames_analysis"]
            }
        }
        
        return report