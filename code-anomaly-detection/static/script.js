// Get DOM elements
const codeInput = document.getElementById('codeInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingIndicator = document.getElementById('loadingIndicator');
const resultsContainer = document.getElementById('resultsContainer');
const emptyState = document.getElementById('emptyState');
const errorContainer = document.getElementById('errorContainer');

// Event listeners
analyzeBtn.addEventListener('click', analyzeCode);
codeInput.addEventListener('input', () => {
    if (!codeInput.value.trim()) {
        showEmptyState();
    }
});

async function analyzeCode() {
    const code = codeInput.value.trim();

    if (!code) {
        alert('Please paste some code to analyze');
        return;
    }

    // Show loading, hide results
    showLoading();
    hideResults();
    hideError();

    try {
        // Phase 1: Extract metrics (simulated)
        console.log('Phase 1: Extracting structural metrics...');

        // Phase 2: Generate embedding (main processing)
        console.log('Phase 2: Generating CodeBERT embedding...');

        // Phase 3: Calculate score (simulated)
        console.log('Phase 3: Calculating anomaly score...');

        // Phase 4: Display results
        console.log('Phase 4: Formatting and displaying results...');

        // Make API call
        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });

        if (!response.ok) {
            const error = await response.json();
            showError(error.error || 'Unknown error occurred');
            hideLoading();
            return;
        }

        const result = await response.json();

        // Display results with animations
        displayResults(result);
        hideLoading();

    } catch (error) {
        showError(`Error: ${error.message}`);
        hideLoading();
    }
}

function displayResults(result) {
    if (result.error) {
        showError(result.error);
        return;
    }

    // Update classification
    const classLabel = document.getElementById('classificationLabel');
    classLabel.textContent = result.classification;
    classLabel.className = 'classification-label ' + result.classification.toLowerCase();

    // Update classification score
    document.getElementById('classificationScore').textContent = result.anomaly_score;

    // Update anomaly score with animation
    const scoreValue = parseFloat(result.anomaly_score);
    const scoreFill = document.getElementById('scoreFill');
    const scoreDisplay = document.getElementById('scoreValue');

    setTimeout(() => {
        scoreFill.style.width = (scoreValue / 10 * 100) + '%';
        scoreDisplay.textContent = result.anomaly_score + ' / 10.0';
    }, 100);

    // Update structural metrics
    document.getElementById('metricFunctions').textContent = result.functions;
    document.getElementById('metricLoops').textContent = result.loops;
    document.getElementById('metricIfs').textContent = result.if_statements;
    document.getElementById('metricDepth').textContent = result.max_depth;

    // Update detailed scores
    document.getElementById('semanticScore').textContent = result.semantic_score;
    document.getElementById('structuralScore').textContent = result.structural_score;

    // Show results
    showResults();
}

function showLoading() {
    loadingIndicator.classList.remove('hidden');
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';
}

function hideLoading() {
    loadingIndicator.classList.add('hidden');
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = 'Analyze Code';
}

function showResults() {
    emptyState.style.display = 'none';
    resultsContainer.classList.remove('hidden');
}

function hideResults() {
    resultsContainer.classList.add('hidden');
    emptyState.style.display = 'block';
}

function showEmptyState() {
    emptyState.style.display = 'block';
    resultsContainer.classList.add('hidden');
}

function showError(message) {
    errorContainer.classList.remove('hidden');
    document.getElementById('errorMessage').textContent = message;
}

function hideError() {
    errorContainer.classList.add('hidden');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    showEmptyState();
});
