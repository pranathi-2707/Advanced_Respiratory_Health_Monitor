import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import librosa
import librosa.display

class AdvancedDashboard:
    def __init__(self):
        self.setup_page()
        
    def setup_page(self):
        # Custom CSS for better styling
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
            padding: 8px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            margin: 5px 0;
        }
        .risk-medium {
            background-color: #ffd93d;
            padding: 8px;
            border-radius: 5px;
            color: black;
            font-weight: bold;
            margin: 5px 0;
        }
        .risk-low {
            background-color: #6bcf7f;
            padding: 8px;
            border-radius: 5px;
            color: white;
            font-weight: bold;
            margin: 5px 0;
        }
        .section-header {
            border-bottom: 2px solid #1f77b4;
            padding-bottom: 0.5rem;
            margin-bottom: 1rem;
            color: #1f77b4;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def display_header(self):
        st.markdown('<h1 class="main-header">🫁 Advanced Respiratory Health Monitoring System</h1>', 
                   unsafe_allow_html=True)
        st.markdown("---")
    
    def create_audio_visualization(self, audio_data, predictions, sample_rate=22050):
        """Create comprehensive audio visualization"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">🎵 Real-time Audio Analysis</div>', 
                       unsafe_allow_html=True)
            
            # Waveform
            fig_wave = go.Figure()
            t = np.linspace(0, len(audio_data)/sample_rate, len(audio_data))
            fig_wave.add_trace(go.Scatter(x=t, y=audio_data, 
                                        line=dict(color='#1f77b4'), name='Audio Signal'))
            fig_wave.update_layout(
                title='Breathing Audio Waveform',
                xaxis_title='Time (s)', 
                yaxis_title='Amplitude',
                height=300
            )
            st.plotly_chart(fig_wave, use_container_width=True)
            
        with col2:
            st.markdown('<div class="section-header">🔍 Pattern Detection Results</div>', 
                       unsafe_allow_html=True)
            
            # Prediction gauges
            self.create_prediction_gauges(predictions)
            
            # Feature analysis
            st.subheader("📈 Respiratory Features")
            features = {
                'Breathing Rate': np.random.randint(12, 20),
                'Inhale/Exhale Ratio': round(np.random.uniform(0.8, 1.2), 2),
                'Spectral Centroid': np.random.randint(800, 2500),
                'Signal Energy': round(np.random.uniform(0.1, 0.9), 3)
            }
            
            for feature, value in features.items():
                st.metric(label=feature, value=value)
    
    def create_prediction_gauges(self, predictions):
        """Create gauge charts for prediction probabilities"""
        # Create simpler horizontal bars for better mobile compatibility
        patterns = list(predictions.keys())
        probabilities = [predictions[p] * 100 for p in patterns]
        
        colors = ['#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#3498db']
        
        fig = go.Figure()
        
        for i, (pattern, prob) in enumerate(zip(patterns, probabilities)):
            fig.add_trace(go.Bar(
                y=[pattern],
                x=[prob],
                orientation='h',
                marker_color=colors[i],
                text=[f'{prob:.1f}%'],
                textposition='auto',
                name=pattern.capitalize()
            ))
        
        fig.update_layout(
            title='Respiratory Pattern Probabilities',
            xaxis_title='Probability (%)',
            yaxis_title='Patterns',
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def display_disease_risk_assessment(self, risk_scores):
        """Display disease risk assessment"""
        st.markdown('<div class="section-header">🩺 Disease Risk Assessment</div>', 
                   unsafe_allow_html=True)
        
        cols = st.columns(4)
        diseases = list(risk_scores.keys())
        
        for i, (col, disease) in enumerate(zip(cols, diseases)):
            risk = risk_scores[disease]
            
            with col:
                if risk > 0.7:
                    risk_class = "risk-high"
                    emoji = "🔴"
                elif risk > 0.4:
                    risk_class = "risk-medium"
                    emoji = "🟡"
                else:
                    risk_class = "risk-low"
                    emoji = "🟢"
                
                disease_name = disease.replace('_', ' ').title()
                st.markdown(f'<div class="{risk_class}">{emoji} {disease_name}<br>{risk*100:.1f}%</div>', 
                           unsafe_allow_html=True)
    
    def display_environmental_data(self, env_data, risks):
        """Display environmental monitoring data"""
        st.markdown('<div class="section-header">🌡️ Environmental Monitoring</div>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Temperature with color coding
        temp = env_data['temperature']
        temp_status = "Optimal" if 18 <= temp <= 28 else "Warning"
        temp_color = "normal" if 18 <= temp <= 28 else "off"
        
        with col1:
            st.metric("Temperature", f"{temp}°C", 
                     delta=temp_status, delta_color=temp_color)
        
        # Humidity with color coding
        humidity = env_data['humidity']
        humidity_status = "Optimal" if 30 <= humidity <= 60 else "Warning"
        humidity_color = "normal" if 30 <= humidity <= 60 else "off"
        
        with col2:
            st.metric("Humidity", f"{humidity}%", 
                     delta=humidity_status, delta_color=humidity_color)
        
        # Air Quality
        air_quality = env_data['air_quality']
        air_status = "Good" if air_quality > 70 else "Poor"
        air_color = "normal" if air_quality > 70 else "off"
        
        with col3:
            st.metric("Air Quality", f"{air_quality}/100",
                     delta=air_status, delta_color=air_color)
        
        with col4:
            st.metric("Pressure", f"{env_data['pressure']} hPa")
        
        # Environmental risks
        if risks:
            risk_text = ", ".join(risks).replace('_', ' ').title()
            st.warning(f"⚠️ Environmental Alert: {risk_text}")