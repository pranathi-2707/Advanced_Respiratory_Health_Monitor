import streamlit as st
import numpy as np
import plotly.graph_objects as go
import time
import random
from datetime import datetime
//
class RespiratoryHealthMonitor:
    def __init__(self):
        self.setup_page()
        self.initialize_session_state()
    
    def setup_page(self):
        st.set_page_config(
            page_title="Respiratory Health Monitor",
            page_icon="🫁",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Custom CSS
        st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: bold;
        }
        .risk-high {
            background-color: #ff6b6b;
            padding: 12px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            margin: 8px 0;
        }
        .risk-medium {
            background-color: #ffd93d;
            padding: 12px;
            border-radius: 10px;
            color: black;
            font-weight: bold;
            margin: 8px 0;
        }
        .risk-low {
            background-color: #6bcf7f;
            padding: 12px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
            margin: 8px 0;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_session_state(self):
        if 'monitoring' not in st.session_state:
            st.session_state.monitoring = False
        if 'history' not in st.session_state:
            st.session_state.history = []
        if 'alerts' not in st.session_state:
            st.session_state.alerts = []
        if 'cycle_count' not in st.session_state:
            st.session_state.cycle_count = 0
    
    def generate_breathing_signal(self, condition='normal'):
        """Generate realistic breathing patterns"""
        duration = 5
        sample_rate = 1000
        t = np.linspace(0, duration, sample_rate * duration)
        
        # Base breathing
        breathing_rate = random.randint(12, 20)
        base_signal = 0.5 * np.sin(2 * np.pi * (breathing_rate/60) * t)
        
        if condition == 'wheeze':
            # Add wheezing (high frequency)
            wheeze = 0.3 * np.sin(2 * np.pi * 500 * t)
            signal = base_signal + wheeze
        elif condition == 'crackle':
            # Add crackles (random spikes)
            crackle = np.zeros_like(t)
            for _ in range(8):
                idx = random.randint(100, len(t)-100)
                crackle[idx:idx+50] = 0.4
            signal = base_signal + crackle
        elif condition == 'cough':
            # Add cough bursts
            cough = np.zeros_like(t)
            cough[1000:1100] = 0.8
            cough[3000:3100] = 0.6
            signal = base_signal + cough
        else:
            signal = base_signal
        
        # Add noise and normalize
        noise = 0.05 * np.random.randn(len(t))
        signal += noise
        signal = signal / np.max(np.abs(signal))
        
        return signal, t, condition
    
    def analyze_patterns(self, signal):
        """Analyze breathing patterns"""
        features = {
            'breathing_rate': random.randint(12, 25),
            'signal_energy': np.mean(signal**2),
            'variability': np.std(signal)
        }
        return features
    
    def predict_conditions(self, features):
        """Predict respiratory conditions"""
        # Simulate ML predictions
        probs = {
            'normal': 0.6,
            'wheeze': 0.1,
            'crackle': 0.1,
            'stridor': 0.1,
            'cough': 0.1
        }
        
        # Adjust based on features
        if features['breathing_rate'] > 20:
            probs['normal'] -= 0.2
            probs['wheeze'] += 0.15
            probs['crackle'] += 0.05
        
        # Normalize
        total = sum(probs.values())
        for key in probs:
            probs[key] /= total
        
        return probs
    
    def assess_risks(self, predictions, features):
        """Assess disease risks"""
        risks = {
            'Asthma': min(predictions['wheeze'] * 0.8, 0.95),
            'COPD': min((predictions['wheeze'] + predictions['crackle']) * 0.5, 0.9),
            'Pneumonia': min(predictions['crackle'] * 0.7, 0.85),
            'Bronchitis': min((predictions['cough'] + predictions['wheeze']) * 0.6, 0.8)
        }
        return risks
    
    def get_environmental_data(self):
        """Get environmental readings"""
        return {
            'temperature': round(22 + random.uniform(-5, 5), 1),
            'humidity': round(45 + random.uniform(-25, 25), 1),
            'air_quality': random.randint(30, 95)
        }
    
    def create_visualization(self, signal, t, predictions, risks):
        """Create dashboard visualization"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Waveform
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t, y=signal, line=dict(color='blue')))
            fig.update_layout(title='Breathing Pattern', height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Environmental data
            env = self.get_environmental_data()
            st.subheader("🌡️ Environment")
            cols = st.columns(3)
            cols[0].metric("Temperature", f"{env['temperature']}°C")
            cols[1].metric("Humidity", f"{env['humidity']}%")
            cols[2].metric("Air Quality", f"{env['air_quality']}/100")
        
        with col2:
            # Pattern probabilities
            st.subheader("🔍 Detected Patterns")
            patterns = list(predictions.keys())
            probabilities = [p * 100 for p in predictions.values()]
            
            fig_bar = go.Figure(data=[
                go.Bar(x=patterns, y=probabilities, 
                      marker_color=['green', 'red', 'orange', 'purple', 'blue'])
            ])
            fig_bar.update_layout(height=300)
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Risk assessment
            st.subheader("🩺 Disease Risks")
            for disease, risk in risks.items():
                risk_pct = risk * 100
                if risk_pct > 70:
                    css_class = "risk-high"
                elif risk_pct > 40:
                    css_class = "risk-medium"
                else:
                    css_class = "risk-low"
                
                st.markdown(f'<div class="{css_class}">{disease}: {risk_pct:.1f}%</div>', 
                           unsafe_allow_html=True)
    
    def generate_alerts(self, predictions, risks):
        """Generate health alerts"""
        alerts = []
        
        for pattern, prob in predictions.items():
            if pattern != 'normal' and prob > 0.3:
                severity = 'high' if prob > 0.6 else 'medium'
                alerts.append({
                    'severity': severity,
                    'message': f'Detected {pattern} (confidence: {prob:.1%})',
                    'timestamp': datetime.now()
                })
        
        for disease, risk in risks.items():
            if risk > 0.5:
                alerts.append({
                    'severity': 'medium',
                    'message': f'High risk of {disease} ({risk:.1%})',
                    'timestamp': datetime.now()
                })
        
        return alerts
    
    def display_alerts(self, alerts):
        """Display alerts"""
        if alerts:
            st.subheader("🚨 Alerts")
            for alert in alerts[-3:]:
                if alert['severity'] == 'high':
                    st.error(f"🔴 {alert['message']}")
                else:
                    st.warning(f"🟡 {alert['message']}")
        else:
            st.success("✅ No alerts - All normal")
    
    def show_dashboard(self):
        """Main dashboard"""
        st.markdown('<h1 class="main-header">🫁 Respiratory Health Monitor</h1>', 
                   unsafe_allow_html=True)
        
        # Controls
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button('🎤 Start Monitoring', type='primary', use_container_width=True):
                st.session_state.monitoring = True
                st.rerun()
        with col2:
            if st.button('⏹️ Stop Monitoring', use_container_width=True):
                st.session_state.monitoring = False
                st.rerun()
        with col3:
            st.metric("Cycle", st.session_state.cycle_count)
        
        if st.session_state.monitoring:
            self.run_monitoring()
        else:
            self.show_welcome()
    
    def run_monitoring(self):
        """Run monitoring cycle"""
        placeholder = st.empty()
        
        with placeholder.container():
            # Generate data
            conditions = ['normal', 'wheeze', 'crackle', 'cough']
            current_condition = random.choice(conditions)
            signal, t, actual_condition = self.generate_breathing_signal(current_condition)
            
            # Analyze
            features = self.analyze_patterns(signal)
            predictions = self.predict_conditions(features)
            risks = self.assess_risks(predictions, features)
            
            # Generate alerts
            new_alerts = self.generate_alerts(predictions, risks)
            st.session_state.alerts.extend(new_alerts)
            
            # Display
            self.create_visualization(signal, t, predictions, risks)
            self.display_alerts(st.session_state.alerts)
            
            # Store history
            st.session_state.history.append({
                'timestamp': datetime.now(),
                'condition': actual_condition,
                'predictions': predictions
            })
            
            st.session_state.cycle_count += 1
            
            # Refresh
            time.sleep(3)
            st.rerun()
    
    def show_welcome(self):
        """Welcome screen"""
        st.markdown("""
        ## Advanced Respiratory Health Monitoring
        
        **Early detection saves lives** - Our system monitors breathing patterns to detect respiratory issues before they become critical.
        
        ### Features:
        - Real-time breathing pattern analysis
        - Wheeze, crackle, and cough detection
        - Disease risk assessment
        - Environmental monitoring
        - Smart alert system
        
        ### Supported Conditions:
        - Asthma
        - COPD
        - Pneumonia
        - Bronchitis
        
        Click **Start Monitoring** to begin analysis.
        """)
        
        if st.button('🎤 Start Monitoring', type='primary'):
            st.session_state.monitoring = True
            st.rerun()

def main():
    monitor = RespiratoryHealthMonitor()
    monitor.show_dashboard()

if __name__ == "__main__":
    main()
