import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from scipy import signal
from scipy.fft import fft

class AdvancedAudioProcessor:
    def __init__(self, sample_rate=22050):
        self.sample_rate = sample_rate
        self.audio_data = None
        
    def load_audio(self, audio_path):
        """Load audio file for analysis"""
        self.audio_data, _ = librosa.load(audio_path, sr=self.sample_rate)
        return self.audio_data
    
    def real_time_capture(self, duration=5):
        """Simulate real-time audio capture"""
        # In hardware, this would use PyAudio for actual recording
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Simulate different breathing patterns with added realism
        normal_breath = 0.5 * np.sin(2 * np.pi * 0.2 * t)
        wheeze_component = 0.3 * np.sin(2 * np.pi * 400 * t) * np.exp(-0.5 * t)
        crackle_component = 0.2 * signal.chirp(t, 100, duration, 1000)
        
        # Combine based on simulated condition
        condition = np.random.choice(['normal', 'wheeze', 'crackle', 'mixed'])
        
        if condition == 'normal':
            audio = normal_breath
        elif condition == 'wheeze':
            audio = normal_breath + wheeze_component
        elif condition == 'crackle':
            audio = normal_breath + crackle_component * (t % 1.5 > 1.4)
        else:  # mixed
            audio = normal_breath + 0.5 * wheeze_component + 0.3 * crackle_component * (t % 2 > 1.8)
        
        # Add noise and normalize
        noise = 0.01 * np.random.normal(size=len(t))
        self.audio_data = audio + noise
        self.audio_data = self.audio_data / np.max(np.abs(self.audio_data))
        
        return self.audio_data, condition
    
    def extract_advanced_features(self, audio_data):
        """Extract comprehensive audio features"""
        features = {}
        
        # Time domain features
        features['rms_energy'] = np.sqrt(np.mean(audio_data**2))
        features['zero_crossing_rate'] = np.mean(librosa.zero_crossings(audio_data))
        
        # Frequency domain features
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=self.sample_rate)[0]
        features['spectral_centroid_mean'] = np.mean(spectral_centroids)
        features['spectral_centroid_std'] = np.std(spectral_centroids)
        
        # MFCC features
        mfccs = librosa.feature.mfcc(y=audio_data, sr=self.sample_rate, n_mfcc=13)
        for i in range(13):
            features[f'mfcc_{i+1}_mean'] = np.mean(mfccs[i])
            features[f'mfcc_{i+1}_std'] = np.std(mfccs[i])
        
        # Advanced respiratory-specific features
        features['breathing_rate'] = self._estimate_breathing_rate(audio_data)
        features['inhale_exhale_ratio'] = self._analyze_breath_phases(audio_data)
        features['harmonic_noise_ratio'] = self._calculate_hnr(audio_data)
        
        return features
    
    def _estimate_breathing_rate(self, audio_data):
        """Estimate breathing rate from audio signal"""
        # Apply bandpass filter for breathing sounds (0.1-2 Hz equivalent in audio domain)
        nyquist = self.sample_rate / 2
        low = 100 / nyquist  # 100 Hz
        high = 1000 / nyquist  # 1000 Hz
        
        b, a = signal.butter(4, [low, high], btype='band')
        filtered = signal.filtfilt(b, a, audio_data)
        
        # Find peaks in the envelope
        envelope = np.abs(signal.hilbert(filtered))
        peaks, _ = signal.find_peaks(envelope, distance=self.sample_rate//2)
        
        if len(peaks) > 1:
            breathing_rate = (len(peaks) - 1) / (len(audio_data) / self.sample_rate) * 60
            return min(breathing_rate, 60)  # Cap at 60 breaths per minute
        return 12  # Default normal rate
    
    def _analyze_breath_phases(self, audio_data):
        """Analyze inhale/exhale phase ratio"""
        # Simplified analysis - in real implementation would use more sophisticated methods
        positive_energy = np.mean(np.maximum(audio_data, 0)**2)
        negative_energy = np.mean(np.maximum(-audio_data, 0)**2)
        
        return positive_energy / (negative_energy + 1e-8)
    
    def _calculate_hnr(self, audio_data):
        """Calculate Harmonic-to-Noise Ratio"""
        # Simplified HNR calculation
        autocorr = np.correlate(audio_data, audio_data, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        
        # Find first peak after zero (fundamental frequency)
        peaks, _ = signal.find_peaks(autocorr[:1000])
        if len(peaks) > 1:
            harmonic_energy = autocorr[peaks[1]]
            noise_energy = np.mean(autocorr[peaks[1]+100:peaks[1]+200])
            return harmonic_energy / (noise_energy + 1e-8)
        return 1.0