"""Vercel serverless function handler for Flask app."""

from flask import Flask, render_template, request, jsonify
import os
import sys
from detect_anomaly import CodeAnomalyDetector

app = Flask(__name__, template_folder='templates', static_folder='static')
detector = None
training_complete = False


def initialize_detector():
    """Initialize detector and train on normal files."""
    global detector, training_complete
    
    if detector is None:
        detector = CodeAnomalyDetector(semantic_weight=0.9, structural_weight=0.1)
        
    if not training_complete:
        try:
            detector.train_from_normal_files("normal_code")
            training_complete = True
        except Exception as e:
            print(f"Warning: Could not train detector: {e}")


@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze submitted code."""
    try:
        data = request.json
        code = data.get('code', '').strip()
        
        if not code:
            return jsonify({'error': 'Please paste some code to analyze'}), 400
        
        # Initialize detector if needed
        initialize_detector()
        
        # Phase 1: Extract metrics (instant)
        metrics = detector.extract_structural_metrics(code)
        
        # Phase 2: Generate embedding (medium)
        test_embedding = detector.embedder.get_embedding(code)
        
        # Phase 3: Calculate score (instant)
        similarity_score = detector.calculate_similarity(test_embedding)
        
        # Calculate final anomaly score
        anomaly_score = (metrics['anomaly_score'] + similarity_score) / 2
        
        is_anomaly = anomaly_score > detector.anomaly_threshold
        
        return jsonify({
            'anomaly_score': float(anomaly_score),
            'is_anomaly': bool(is_anomaly),
            'structural_metrics': metrics,
            'similarity_score': float(similarity_score),
            'threshold': float(detector.anomaly_threshold)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=False)
