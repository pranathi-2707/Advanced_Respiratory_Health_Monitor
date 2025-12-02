import numpy as np
import tensorflow as tf
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import json

class AdvancedRespiratoryModel:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.anomaly_detector = IsolationForest(contamination=0.1)
        self.disease_risk_model = RandomForestClassifier()
        self.is_trained = False
        
    def create_model(self):
        """Create advanced neural network model"""
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(30,)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(5, activation='softmax')  # 5 classes
        ])
        
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        
        self.model = model
        return model
    
    def predict_respiratory_pattern(self, features):
        """Predict respiratory patterns with confidence scores"""
        if not self.is_trained:
            # For demo - return simulated predictions
            return self._simulate_prediction(features)
        
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)[0]
        
        return {
            'normal': float(prediction[0]),
            'wheeze': float(prediction[1]),
            'crackle': float(prediction[2]),
            'stridor': float(prediction[3]),
            'cough': float(prediction[4])
        }
    
    def predict_disease_risk(self, audio_features, environmental_data, patient_history=None):
        """Advanced disease risk prediction"""
        # Combine all features
        combined_features = list(audio_features.values())
        combined_features.extend([environmental_data['temperature'], 
                                environmental_data['humidity']])
        
        # Simulate disease risk prediction (in real implementation, use trained model)
        risk_scores = self._simulate_disease_risk(combined_features)
        
        return risk_scores
    
    def _simulate_prediction(self, features):
        """Simulate ML predictions for demo"""
        # Simulate based on feature patterns
        spectral_centroid = features.get('spectral_centroid_mean', 1000)
        breathing_rate = features.get('breathing_rate', 15)
        hnr = features.get('harmonic_noise_ratio', 1.0)
        
        # Simulation logic
        if spectral_centroid > 2000 and hnr < 0.5:
            return {'normal': 0.1, 'wheeze': 0.8, 'crackle': 0.05, 'stridor': 0.03, 'cough': 0.02}
        elif breathing_rate > 25:
            return {'normal': 0.2, 'wheeze': 0.3, 'crackle': 0.4, 'stridor': 0.05, 'cough': 0.05}
        else:
            return {'normal': 0.85, 'wheeze': 0.05, 'crackle': 0.05, 'stridor': 0.03, 'cough': 0.02}
    
    def _simulate_disease_risk(self, features):
        """Simulate disease risk assessment"""
        return {
            'asthma_risk': min(0.3 + features[0] / 10000, 0.95),
            'copd_risk': min(0.2 + features[1] / 5000, 0.9),
            'pneumonia_risk': min(0.1 + features[2] / 3000, 0.8),
            'bronchitis_risk': min(0.15 + features[3] / 4000, 0.85)
        }
    
    def detect_anomalies(self, features):
        """Detect anomalous breathing patterns"""
        anomaly_score = self.anomaly_detector.decision_function([list(features.values())])[0]
        return anomaly_score < 0  # Returns True if anomaly detected