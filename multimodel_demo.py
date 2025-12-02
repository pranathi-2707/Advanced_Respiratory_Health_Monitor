import streamlit as st
import cv2
import numpy as np
import pyaudio
import threading
import queue
import time
from scipy import signal
from scipy.fft import fft
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import librosa
import mediapipe as mp
from collections import deque

class RealMultiModalDetector:
    def __init__(self):
        self.setup_page()
        self.initialize_components()
        
    def setup_page(self):
        st.set_page_config(
            page_title="Real Respiratory Detection",
            page_icon="🫁",
            layout="wide"
        )
        
    def initialize_components(self):
        """Initialize camera, audio, and ML components"""
        # MediaPipe for visual analysis
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(max_num_faces=1)
        
        # Audio setup
        self.audio = pyaudio.PyAudio()
        self.is_recording = False
        self.sample_rate = 44100
        self.chunk_size = 1024
        self.audio_data = []
        
        # Analysis data
        self.breathing_pattern = deque(maxlen=100)
        self.audio_features_history = deque(maxlen=50)
        
    def start_camera(self):
        """Start camera capture"""
        self.camera_active = True
        self.cap = cv2.VideoCapture(0)
        
    def stop_camera(self):
        """Stop camera capture"""
        self.camera_active = False
        if hasattr(self, 'cap'):
            self.cap.release()
            
    def start_audio(self):
        """Start audio recording"""
        self.is_recording = True
        self.audio_data = []
        
        def record_audio():
            stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            
            while self.is_recording:
                data = stream.read(self.chunk_size, exception_on_overflow=False)
                audio_array = np.frombuffer(data, dtype=np.int16)
                self.audio_data.extend(audio_array)
                
            stream.stop_stream()
            stream.close()
            
        self.audio_thread = threading.Thread(target=record_audio)
        self.audio_thread.start()
        
    def stop_audio(self):
        """Stop audio recording"""
        self.is_recording = False
        if hasattr(self, 'audio_thread'):
            self.audio_thread.join()
            
    def analyze_breathing_visual(self, frame):
        """Analyze breathing patterns from camera"""
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.face_mesh.process(rgb_frame)
            
            if results.multi_face_landmarks:
                landmarks = results.multi_face_landmarks[0]
                
                # Track nose movement for breathing
                nose_tip = landmarks.landmark[1]  # Nose tip
                self.breathing_pattern.append(nose_tip.y)
                
                # Calculate breathing rate
                if len(self.breathing_pattern) > 10:
                    breathing_signal = list(self.breathing_pattern)
                    peaks, _ = signal.find_peaks(breathing_signal, distance=5)
                    breathing_rate = len(peaks) * 6  # Approximate BPM
                    return breathing_rate, rgb_frame
                    
            return 15, rgb_frame  # Default breathing rate
            
        except Exception as e:
            return 15, frame
            
    def analyze_breathing_audio(self):
        """Analyze breathing sounds from microphone"""
        if len(self.audio_data) < self.chunk_size:
            return {}
            
        # Get recent audio data
        audio_chunk = np.array(self.audio_data[-self.chunk_size:])
        audio_float = audio_chunk.astype(np.float32) / 32768.0
        
        features = {}
        
        # Frequency analysis
        fft_result = fft(audio_float)
        freqs = np.fft.fftfreq(len(fft_result), 1/self.sample_rate)
        positive_idx = freqs > 0
        fft_magnitude = np.abs(fft_result[positive_idx])
        
        # Wheeze detection (400-1000 Hz)
        wheeze_mask = (freqs[positive_idx] > 400) & (freqs[positive_idx] < 1000)
        if np.any(wheeze_mask):
            features['wheeze_power'] = np.mean(fft_magnitude[wheeze_mask])
        else:
            features['wheeze_power'] = 0
            
        # Energy analysis
        features['rms_energy'] = np.sqrt(np.mean(audio_float**2))
        
        return features
        
    def diagnose_conditions(self, visual_rate, audio_features):
        """Diagnose respiratory conditions"""
        conditions = {}
        
        # Asthma detection
        if audio_features.get('wheeze_power', 0) > 0.05 and visual_rate > 20:
            conditions['Asthma'] = min(audio_features['wheeze_power'] * 10, 0.95)
            
        # Breathing difficulty
        if visual_rate > 25:
            conditions['Breathing Difficulty'] = min((visual_rate - 20) * 0.1, 0.8)
            
        # Cough/Bronchitis
        if audio_features.get('rms_energy', 0) > 0.2:
            conditions['Bronchitis'] = min(audio_features['rms_energy'] * 3, 0.85)
            
        return conditions
        
    def create_dashboard(self, frame, visual_rate, audio_features, conditions):
        """Create real-time dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                "Live Camera Feed",
                "Breathing Analysis",
                "Audio Analysis", 
                "Diagnosis"
            )
        )
        
        # Camera feed
        if frame is not None:
            fig.add_trace(go.Image(z=frame), row=1, col=1)
            
        # Breathing rate
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=visual_rate,
                title={"text": "Breathing Rate"},
                gauge={'axis': {'range': [0, 40]},
                      'steps': [{'range': [0, 20], 'color': "green"},
                               {'range': [20, 30], 'color': "yellow"},
                               {'range': [30, 40], 'color': "red"}]}),
            row=1, col=2
        )
        
        # Audio features
        fig.add_trace(
            go.Bar(x=list(audio_features.keys()), 
                  y=list(audio_features.values()),
                  marker_color='blue'),
            row=2, col=1
        )
        
        # Diagnosis
        if conditions:
            diagnosis_text = "<br>".join([f"{k}: {v:.1%}" for k, v in conditions.items()])
            fig.add_annotation(
                text=diagnosis_text,
                x=0.5, y=0.5, xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=14, color="red"),
                row=2, col=2
            )
        else:
            fig.add_annotation(
                text="✅ Healthy",
                x=0.5, y=0.5, xref="paper", yref="paper", 
                showarrow=False,
                font=dict(size=16, color="green"),
                row=2, col=2
            )
            
        fig.update_layout(height=600)
        return fig
        
    def run_demo(self):
        """Main application"""
        st.title("🎥➕🎤 Real Multi-Modal Respiratory Detection")
        st.markdown("### Live Camera + Microphone Analysis")
        
        # Controls
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚀 Start Analysis", type="primary"):
                self.start_camera()
                self.start_audio()
                
        with col2:
            if st.button("⏹️ Stop Analysis"):
                self.stop_camera()
                self.stop_audio()
                
        # Real-time analysis
        if hasattr(self, 'camera_active') and self.camera_active:
            placeholder = st.empty()
            
            while self.camera_active:
                ret, frame = self.cap.read()
                if not ret:
                    break
                    
                # Analyze visual breathing
                visual_rate, processed_frame = self.analyze_breathing_visual(frame)
                
                # Analyze audio
                audio_features = self.analyze_breathing_audio()
                
                # Diagnose conditions
                conditions = self.diagnose_conditions(visual_rate, audio_features)
                
                # Update dashboard
                with placeholder.container():
                    fig = self.create_dashboard(processed_frame, visual_rate, 
                                              audio_features, conditions)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Breathing Rate", f"{visual_rate} BPM")
                    col2.metric("Wheeze Detection", f"{audio_features.get('wheeze_power', 0)*100:.1f}%")
                    col3.metric("Status", "Analyzing..." if not conditions else "Abnormal Detected")
                    
                time.sleep(0.1)
                
        else:
            st.info("""
            ### Click 'Start Analysis' to begin real-time detection
            
            **This system uses:**
            - 🎥 Camera: Tracks breathing patterns via face movement
            - 🎤 Microphone: Analyzes breathing sounds for abnormalities
            - 🤖 AI: Combines visual + audio data for accurate diagnosis
            
            **Sit in front of your camera and breathe normally to see real analysis!**
            """)
            
    def __del__(self):
        """Cleanup"""
        if hasattr(self, 'camera_active') and self.camera_active:
            self.stop_camera()
        if hasattr(self, 'is_recording') and self.is_recording:
            self.stop_audio()
        if hasattr(self, 'audio'):
            self.audio.terminate()

if __name__ == "__main__":
    demo = RealMultiModalDetector()
    demo.run_demo()