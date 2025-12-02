# Advanced Respiratory Health Monitoring System

## Project Overview
An AI-powered multi-modal respiratory disease detection system that combines audio analysis and visual monitoring to detect early signs of respiratory conditions like Asthma, COPD, Pneumonia, and Bronchitis.

## Features

### Core Capabilities
- Real-time Audio Analysis: Detects wheezing, crackles, coughing patterns
- Visual Breathing Monitoring: Tracks breathing patterns via camera
- Multi-Modal Fusion: Combines audio + visual data for accurate diagnosis
- Disease Risk Assessment: Predicts specific respiratory conditions
- Smart Alert System: Immediate notifications for concerning patterns
- Comprehensive Dashboard: Real-time visualization and analysis

### Supported Conditions
1. Asthma - Wheezing detection and severity assessment
2. COPD - Chronic obstructive pulmonary disease monitoring
3. Pneumonia - Crackle detection and risk evaluation
4. Bronchitis - Cough pattern analysis
5. Sleep Apnea - Breathing pattern irregularities

## Technology Stack

### Backend & AI
- Python 3.9 - Core programming language
- Streamlit - Interactive web application framework
- NumPy/SciPy - Scientific computing and signal processing
- Librosa - Audio analysis and feature extraction
- MediaPipe - Visual pose and face landmark detection
- Plotly - Interactive data visualization

### Signal Processing
- FFT Analysis - Frequency domain transformation
- Spectral Features - MFCC, spectral centroids, bandwidth
- Time Domain Features - RMS energy, zero-crossing rate
- Pattern Recognition - Machine learning algorithms

## Installation

### Method 1: Using Conda (Recommended)
```bash
# Create environment
conda create -n respiratory python=3.9 -y

# Activate environment
conda activate respiratory

# Install packages
conda install -c conda-forge streamlit plotly numpy scipy scikit-learn matplotlib pandas librosa -y
pip install mediapipe pyaudio