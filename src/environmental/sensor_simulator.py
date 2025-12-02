import random
import time
from datetime import datetime

class EnvironmentalSensorSimulator:
    def __init__(self):
        self.temperature = 22.0
        self.humidity = 45.0
        self.air_quality = 85
        self.pressure = 1013.25
        
    def read_sensors(self):
        """Simulate sensor readings with realistic variations"""
        # Simulate realistic environmental changes
        self.temperature += random.uniform(-0.5, 0.5)
        self.temperature = max(15, min(35, self.temperature))  # Clamp values
        
        self.humidity += random.uniform(-2, 2)
        self.humidity = max(20, min(80, self.humidity))
        
        self.air_quality += random.uniform(-5, 5)
        self.air_quality = max(0, min(100, self.air_quality))
        
        self.pressure += random.uniform(-0.5, 0.5)
        
        return {
            'temperature': round(self.temperature, 2),
            'humidity': round(self.humidity, 2),
            'air_quality': round(self.air_quality, 2),
            'pressure': round(self.pressure, 2),
            'timestamp': datetime.now().isoformat()
        }
    
    def assess_environmental_risk(self, sensor_data):
        """Assess environmental risk factors"""
        risks = []
        
        if sensor_data['temperature'] < 18 or sensor_data['temperature'] > 28:
            risks.append('temperature_extreme')
        
        if sensor_data['humidity'] < 30 or sensor_data['humidity'] > 60:
            risks.append('humidity_extreme')
            
        if sensor_data['air_quality'] < 50:
            risks.append('poor_air_quality')
            
        return risks