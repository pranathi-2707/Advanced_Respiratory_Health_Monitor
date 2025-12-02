import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import json
from datetime import datetime

class AdvancedAlertSystem:
    def __init__(self):
        self.alert_history = []
        
    def generate_alert(self, prediction_results, environmental_risks, disease_risks):
        """Generate comprehensive health alerts"""
        alerts = []
        
        # Check respiratory patterns
        for pattern, probability in prediction_results.items():
            if pattern != 'normal' and probability > 0.6:
                alerts.append({
                    'type': 'respiratory_pattern',
                    'severity': 'high' if probability > 0.8 else 'medium',
                    'message': f'Detected {pattern} pattern with {probability*100:.1f}% confidence',
                    'timestamp': datetime.now().isoformat(),
                    'pattern': pattern,
                    'probability': probability
                })
        
        # Check environmental risks
        if environmental_risks:
            alerts.append({
                'type': 'environmental',
                'severity': 'medium',
                'message': f'Environmental risks: {", ".join(environmental_risks)}',
                'timestamp': datetime.now().isoformat(),
                'risks': environmental_risks
            })
        
        # Check disease risks
        high_disease_risks = {disease: risk for disease, risk in disease_risks.items() if risk > 0.7}
        if high_disease_risks:
            alerts.append({
                'type': 'disease_risk',
                'severity': 'high',
                'message': f'High disease risks detected: {", ".join(high_disease_risks.keys())}',
                'timestamp': datetime.now().isoformat(),
                'risks': high_disease_risks
            })
        
        # Store in history
        self.alert_history.extend(alerts)
        
        return alerts
    
    def send_mobile_notification(self, alert):
        """Simulate mobile notification"""
        print(f"📱 MOBILE ALERT: {alert['message']}")
        # In hardware implementation, this would integrate with Firebase Cloud Messaging or similar
        
    def generate_health_report(self, duration_hours=24):
        """Generate comprehensive health report"""
        recent_alerts = [alert for alert in self.alert_history 
                        if datetime.fromisoformat(alert['timestamp']) > 
                        datetime.now() - timedelta(hours=duration_hours)]
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'monitoring_duration': f'{duration_hours} hours',
            'total_alerts': len(recent_alerts),
            'high_severity_alerts': len([a for a in recent_alerts if a['severity'] == 'high']),
            'alert_breakdown': self._categorize_alerts(recent_alerts),
            'recommendations': self._generate_recommendations(recent_alerts)
        }
        
        return report
    
    def _categorize_alerts(self, alerts):
        """Categorize alerts by type and severity"""
        categories = {}
        for alert in alerts:
            alert_type = alert['type']
            if alert_type not in categories:
                categories[alert_type] = {'high': 0, 'medium': 0, 'low': 0}
            categories[alert_type][alert['severity']] += 1
        return categories
    
    def _generate_recommendations(self, alerts):
        """Generate health recommendations based on alerts"""
        recommendations = []
        
        respiratory_alerts = [a for a in alerts if a['type'] == 'respiratory_pattern']
        if respiratory_alerts:
            recommendations.append("Consult a healthcare professional for respiratory symptoms")
        
        environmental_alerts = [a for a in alerts if a['type'] == 'environmental']
        if environmental_alerts:
            recommendations.append("Consider improving indoor air quality and ventilation")
        
        if any(a['severity'] == 'high' for a in alerts):
            recommendations.append("Seek immediate medical attention if symptoms worsen")
        
        if not recommendations:
            recommendations.append("Continue regular monitoring. No significant issues detected.")
        
        return recommendations