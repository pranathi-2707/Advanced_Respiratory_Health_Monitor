import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Audio Processing
    SAMPLE_RATE = 22050
    DURATION = 5
    N_MFCC = 13
    HOP_LENGTH = 512
    
    # ML Model
    MODEL_PATH = "data/models/respiratory_model.h5"
    CLASSES = ['normal', 'wheeze', 'crackle', 'stridor', 'cough']
    
    # Alert Thresholds
    WHEEZE_THRESHOLD = 0.7
    COUGH_THRESHOLD = 0.6
    CRACKLE_THRESHOLD = 0.65
    
    # Environmental
    TEMP_THRESHOLD = (18, 28)  # Celsius
    HUMIDITY_THRESHOLD = (30, 60)  # Percentage
    
    # Advanced Features
    ENABLE_PREDICTIVE_ANALYTICS = True
    ENABLE_VOICE_BIOMMARKERS = True
    ENABLE_SLEEP_ANALYSIS = True