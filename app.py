"""Flask web application for Code Anomaly Detection."""

from flask import Flask, render_template, request, jsonify
import os
import sys
from detect_anomaly import CodeAnomalyDetector

app = Flask(__name__)
detector = None
training_complete = False


def initialize_detector():
    """Initialize detector and train on normal files."""
    global detector, training_complete
    
    if detector is None:
        detector = CodeAnomalyDetector(semantic_weight=0.9, structural_weight=0.1)
        
    if not training_complete:
        detector.train_from_normal_files("normal_code")
        training_complete = True


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
        from sklearn.metrics.pairwise import cosine_similarity
        similarity = cosine_similarity(test_embedding, detector.normal_embedding)[0][0]
        semantic_score = 1.0 - similarity
        structural_score = detector.compute_structural_score(metrics)
        
        raw_score = detector.semantic_weight * semantic_score + detector.structural_weight * structural_score
        anomaly_score = raw_score * 150.0
        
        if anomaly_score < 7:
            classification = "NORMAL"
        else:
            classification = "ANOMALOUS"
        
        # Phase 4: Format results (instant)
        result = {
            'anomaly_score': f"{anomaly_score:.3f}",
            'classification': classification,
            'functions': metrics['functions'],
            'loops': metrics['loops'],
            'if_statements': metrics['if_statements'],
            'max_depth': metrics['max_depth'],
            'semantic_score': f"{semantic_score:.3f}",
            'structural_score': f"{structural_score:.3f}",
            'threshold': '< 7 = NORMAL | >= 7 = ANOMALOUS'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Error analyzing code: {str(e)}'}), 500


@app.route('/status', methods=['GET'])
def status():
    """Check initialization status."""
    global training_complete
    if training_complete:
        return jsonify({'status': 'ready', 'message': 'Detector ready for analysis'})
    else:
        return jsonify({'status': 'initializing', 'message': 'Initializing detector...'})


if __name__ == '__main__':
    # Initialize on startup
    initialize_detector()
    app.run(debug=True, port=5000)
