import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time
import random

class MedicalDemonstration:
    def __init__(self):
        self.setup_page()
        self.initialize_demo()
    
    def setup_page(self):
        st.set_page_config(
            page_title="Respiratory Disease Detection Demo",
            page_icon="🫁",
            layout="wide"
        )
        
        # Medical-style CSS
        st.markdown("""
        <style>
        .doctor-section {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: center;
        }
        .patient-section {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            margin: 10px 0;
            text-align: center;
        }
        .disease-detected {
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            animation: pulse 2s infinite;
        }
        .healthy {
            background: linear-gradient(135deg, #6bcf7f 0%, #27ae60 100%);
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.02); }
            100% { transform: scale(1); }
        }
        .analysis-box {
            background: #f8f9fa;
            border-left: 5px solid #007bff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def initialize_demo(self):
        if 'demo_step' not in st.session_state:
            st.session_state.demo_step = 0
        if 'patient_data' not in st.session_state:
            st.session_state.patient_data = self.generate_patient()
    
    def generate_patient(self):
        """Generate random patient data"""
        conditions = ['Healthy', 'Asthma', 'COPD', 'Pneumonia', 'Bronchitis']
        condition = random.choice(conditions)
        
        return {
            'name': f"Patient {random.randint(1000, 9999)}",
            'age': random.randint(25, 75),
            'condition': condition,
            'breathing_rate': random.randint(12, 30) if condition != 'Healthy' else random.randint(12, 20),
            'oxygen_saturation': random.randint(85, 99) if condition != 'Healthy' else random.randint(95, 99),
            'symptoms': self.get_symptoms(condition)
        }
    
    def get_symptoms(self, condition):
        """Get symptoms based on condition"""
        symptoms = {
            'Healthy': ["Normal breathing", "Clear lungs", "No wheezing"],
            'Asthma': ["Wheezing sound", "Shortness of breath", "Chest tightness"],
            'COPD': ["Chronic cough", "Wheezing", "Shortness of breath", "Chest tightness"],
            'Pneumonia': ["Crackling sounds", "Fever", "Cough with phlegm", "Breathing difficulty"],
            'Bronchitis': ["Persistent cough", "Wheezing", "Chest discomfort", "Shortness of breath"]
        }
        return symptoms.get(condition, ["No specific symptoms"])
    
    def generate_breathing_pattern(self, condition):
        """Generate realistic breathing patterns for different conditions"""
        duration = 8
        t = np.linspace(0, duration, 1000)
        
        if condition == 'Healthy':
            # Normal rhythmic breathing
            signal = 0.8 * np.sin(2 * np.pi * 0.2 * t)
            noise = 0.1 * np.random.randn(len(t))
            return t, signal + noise, "Normal rhythmic pattern"
        
        elif condition == 'Asthma':
            # Wheezing pattern (high frequency modulation)
            base = 0.6 * np.sin(2 * np.pi * 0.25 * t)
            wheeze = 0.4 * np.sin(2 * np.pi * 8 * t) * np.exp(-0.3 * t)
            return t, base + wheeze, "High-frequency wheezing detected"
        
        elif condition == 'COPD':
            # Irregular pattern with prolonged expiration
            base = 0.7 * np.sin(2 * np.pi * 0.3 * t)
            irregular = 0.3 * np.sin(2 * np.pi * 0.1 * t) * (t > 2)
            return t, base + irregular, "Irregular breathing with prolonged expiration"
        
        elif condition == 'Pneumonia':
            # Crackles (random sharp peaks)
            base = 0.5 * np.sin(2 * np.pi * 0.35 * t)
            crackles = np.zeros_like(t)
            for _ in range(15):
                idx = random.randint(100, len(t)-100)
                crackles[idx:idx+10] = 0.6
            return t, base + crackles, "Crackling sounds detected"
        
        else:  # Bronchitis
            # Cough bursts
            base = 0.6 * np.sin(2 * np.pi * 0.22 * t)
            cough = np.zeros_like(t)
            cough[300:350] = 1.0
            cough[1500:1550] = 0.8
            return t, base + cough, "Cough bursts detected"
    
    def create_medical_visualization(self, t, signal, diagnosis, analysis):
        """Create medical visualization showing the analysis"""
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"colspan": 2}, None],
                   [{"type": "indicator"}, {"type": "indicator"}]],
            subplot_titles=(
                f"Real-time Breathing Analysis - {diagnosis}",
                "Breathing Rate Analysis",
                "Oxygen Saturation"
            ),
            row_heights=[0.7, 0.3]
        )
        
        # Breathing waveform
        fig.add_trace(
            go.Scatter(x=t, y=signal, line=dict(color='blue', width=3),
                      name="Breathing Pattern", fill='tozeroy'),
            row=1, col=1
        )
        
        # Add condition-specific annotations
        if "wheezing" in analysis.lower():
            fig.add_annotation(x=t[500], y=0.8, text="🚨 Wheezing Zone", 
                             showarrow=True, arrowhead=2, bgcolor="red")
        
        if "crackling" in analysis.lower():
            fig.add_annotation(x=t[700], y=0.6, text="⚠️ Crackles Detected", 
                             showarrow=True, arrowhead=2, bgcolor="orange")
        
        # Breathing rate gauge
        fig.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=st.session_state.patient_data['breathing_rate'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Breaths/Min"},
                gauge={'axis': {'range': [None, 40]},
                      'steps': [{'range': [0, 20], 'color': "lightgray"},
                               {'range': [20, 30], 'color': "yellow"},
                               {'range': [30, 40], 'color': "red"}],
                      'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': 25}}),
            row=2, col=1
        )
        
        # Oxygen saturation gauge
        fig.add_trace(
            go.Indicator(
                mode="gauge+number",
                value=st.session_state.patient_data['oxygen_saturation'],
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "O₂ Sat %"},
                gauge={'axis': {'range': [80, 100]},
                      'steps': [{'range': [80, 90], 'color': "red"},
                               {'range': [90, 95], 'color': "yellow"},
                               {'range': [95, 100], 'color': "lightgreen"}],
                      'threshold': {'line': {'color': "red", 'width': 4},
                                   'thickness': 0.75, 'value': 92}}),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False)
        return fig
    
    def show_doctor_analysis(self):
        """Show doctor's analysis and diagnosis"""
        patient = st.session_state.patient_data
        
        st.markdown(f"""
        <div class="doctor-section">
            <h2>👩‍⚕️ Dr. Sarah Mitchell - Pulmonologist</h2>
            <p><em>"Analyzing patient breathing patterns using AI-assisted diagnosis"</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="patient-section">
                <h3>👨‍💼 Patient Information</h3>
                <p><strong>Name:</strong> {patient['name']}</p>
                <p><strong>Age:</strong> {patient['age']} years</p>
                <p><strong>Presenting Condition:</strong> Respiratory Assessment</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if patient['condition'] == 'Healthy':
                st.markdown(f"""
                <div class="healthy">
                    <h3>✅ Diagnosis: HEALTHY</h3>
                    <p>Normal respiratory function detected</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="disease-detected">
                    <h3>🚨 Diagnosis: {patient['condition'].upper()}</h3>
                    <p>Abnormal breathing patterns detected</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Symptoms list
        st.subheader("📋 Clinical Symptoms Detected")
        for symptom in patient['symptoms']:
            if patient['condition'] != 'Healthy' and symptom != "Normal breathing":
                st.error(f"⚠️ {symptom}")
            else:
                st.success(f"✅ {symptom}")
    
    def show_comparison_demo(self):
        """Show comparison between healthy and diseased patterns"""
        st.markdown("---")
        st.subheader("🔬 Side-by-Side Comparison: Healthy vs Diseased Breathing")
        
        # Generate both patterns
        t_healthy, healthy_signal, healthy_analysis = self.generate_breathing_pattern('Healthy')
        t_disease, disease_signal, disease_analysis = self.generate_breathing_pattern(st.session_state.patient_data['condition'])
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=("Healthy Breathing Pattern", f"{st.session_state.patient_data['condition']} Breathing Pattern")
        )
        
        # Healthy pattern
        fig.add_trace(
            go.Scatter(x=t_healthy, y=healthy_signal, line=dict(color='green', width=3),
                      name="Healthy", fill='tozeroy'),
            row=1, col=1
        )
        
        # Diseased pattern
        fig.add_trace(
            go.Scatter(x=t_disease, y=disease_signal, line=dict(color='red', width=3),
                      name="Diseased", fill='tozeroy'),
            row=1, col=2
        )
        
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Analysis comparison
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**Healthy Analysis:** {healthy_analysis}")
        with col2:
            st.error(f"**Disease Analysis:** {disease_analysis}")
    
    def show_ai_detection_process(self):
        """Show how AI detects the disease"""
        st.markdown("---")
        st.subheader("🤖 AI Detection Process")
        
        steps = [
            "1. **Audio Capture**: Recording breathing sounds using digital stethoscope",
            "2. **Signal Processing**: Analyzing frequency patterns and waveforms",
            "3. **Feature Extraction**: Identifying key characteristics (wheezing, crackles, etc.)",
            "4. **Pattern Recognition**: Comparing with database of known respiratory conditions",
            "5. **Diagnosis**: Providing clinical assessment with confidence scores"
        ]
        
        for step in steps:
            st.markdown(f'<div class="analysis-box">{step}</div>', unsafe_allow_html=True)
        
        # Show confidence scores
        st.subheader("📊 Detection Confidence Scores")
        conditions = ['Healthy', 'Asthma', 'COPD', 'Pneumonia', 'Bronchitis']
        current_condition = st.session_state.patient_data['condition']
        
        for condition in conditions:
            if condition == current_condition:
                confidence = random.randint(85, 98)
                st.progress(confidence/100, text=f"🔴 {condition}: {confidence}% (DETECTED)")
            else:
                confidence = random.randint(5, 30)
                st.progress(confidence/100, text=f"⚪ {condition}: {confidence}%")
    
    def run_demo(self):
        """Run the main demonstration"""
        st.title("🫁 Respiratory Disease Detection - Medical Demonstration")
        st.markdown("### *AI-Powered Early Detection System*")
        
        # Generate breathing pattern for current patient
        t, signal, analysis = self.generate_breathing_pattern(st.session_state.patient_data['condition'])
        
        # Show doctor analysis
        self.show_doctor_analysis()
        
        # Show medical visualization
        st.markdown("---")
        st.subheader("📈 Real-time Breathing Pattern Analysis")
        fig = self.create_medical_visualization(t, signal, 
                                              st.session_state.patient_data['condition'], 
                                              analysis)
        st.plotly_chart(fig, use_container_width=True)
        
        # Show comparison
        self.show_comparison_demo()
        
        # Show AI detection process
        self.show_ai_detection_process()
        
        # Controls
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Analyze New Patient", use_container_width=True):
                st.session_state.patient_data = self.generate_patient()
                st.rerun()
        
        with col2:
            if st.session_state.patient_data['condition'] == 'Healthy':
                st.success("✅ Current: Healthy Patient")
            else:
                st.error(f"🚨 Current: {st.session_state.patient_data['condition']} Patient")
        
        with col3:
            if st.button("▶️ Simulate Real-time Monitoring", use_container_width=True):
                self.simulate_real_time()
    
    def simulate_real_time(self):
        """Simulate real-time monitoring"""
        placeholder = st.empty()
        
        for i in range(10):
            with placeholder.container():
                # Generate slightly varying pattern
                t, signal, analysis = self.generate_breathing_pattern(st.session_state.patient_data['condition'])
                
                # Add some random variation to simulate real-time
                signal = signal + 0.1 * np.random.randn(len(signal))
                
                st.info(f"🔄 Real-time monitoring... Cycle {i+1}/10")
                fig = self.create_medical_visualization(t, signal, 
                                                      st.session_state.patient_data['condition'], 
                                                      analysis)
                st.plotly_chart(fig, use_container_width=True)
                
                time.sleep(1)
        
        st.success("✅ Real-time monitoring completed!")

def main():
    demo = MedicalDemonstration()
    demo.run_demo()

if __name__ == "__main__":
    main()