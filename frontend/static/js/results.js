/**
 * Results Page - Display Prediction History
 * Load and display predictions from localStorage
 */

document.addEventListener('DOMContentLoaded', () => {
    loadPredictionHistory();
});

/**
 * Load prediction history from localStorage
 */
function loadPredictionHistory() {
    const predictions = JSON.parse(localStorage.getItem('ecopackai_predictions') || '[]');

    if (predictions.length === 0) {
        // Show empty state
        document.getElementById('emptyState').style.display = 'block';
        document.getElementById('resultsList').style.display = 'none';
        return;
    }

    // Hide empty state
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('resultsList').style.display = 'block';

    // Clear existing results
    const resultsContainer = document.getElementById('resultsListContainer');
    resultsContainer.innerHTML = '';

    // Render each prediction
    predictions.forEach((prediction, index) => {
        const predictionCard = createPredictionCard(prediction, index);
        resultsContainer.appendChild(predictionCard);
    });

    // Update statistics
    updateStatistics(predictions);
}

/**
 * Create a prediction card element
 */
function createPredictionCard(prediction, index) {
    const card = document.createElement('div');
    card.className = 'card';
    card.style.cssText = 'background: var(--gray-50); cursor: pointer; margin-bottom: 1rem;';
    card.onclick = () => viewPredictionDetails(prediction);

    const results = prediction.results || {};
    const timestamp = new Date(prediction.timestamp);

    card.innerHTML = `
        <div class="d-flex" style="justify-content: space-between; align-items: flex-start; gap: 2rem; flex-wrap: wrap;">
            <div style="flex: 1;">
                <div class="d-flex gap-2" style="align-items: center; margin-bottom: 0.5rem;">
                    <h4 style="margin: 0; font-size: 1.1rem;">Prediction #${String(index + 1).padStart(3, '0')}</h4>
                    <div class="badge badge-success">Completed</div>
                </div>
                <p class="text-muted" style="margin: 0; font-size: 0.9rem;">
                    ${timestamp.toLocaleDateString()} • ${timestamp.toLocaleTimeString()}
                </p>
            </div>

            <div class="d-grid" style="grid-template-columns: repeat(2, 1fr); gap: 2rem; min-width: 400px;">
                <div class="text-center">
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--success);">
                        $${(results.predicted_cost || 0).toFixed(2)}
                    </div>
                    <div class="text-muted" style="font-size: 0.85rem;">Predicted Cost</div>
                </div>
                <div class="text-center">
                    <div style="font-size: 1.5rem; font-weight: 700; color: var(--info);">
                        ${(results.predicted_co2 || 0).toFixed(3)} kg
                    </div>
                    <div class="text-muted" style="font-size: 0.85rem;">CO₂ Impact</div>
                </div>
            </div>
            
            <div style="display: flex; gap: 0.5rem;">
                <button class="btn btn-sm btn-success" onclick="event.stopPropagation(); downloadPredictionCSV(${index})"
                    title="Download as CSV">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                        <polyline points="7 10 12 15 17 10" />
                        <line x1="12" y1="15" x2="12" y2="3" />
                    </svg>
                </button>
                <button class="btn btn-sm btn-danger" onclick="event.stopPropagation(); deletePrediction(${index})"
                    title="Delete prediction">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6" />
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    </svg>
                </button>
            </div>
        </div>
    `;

    return card;
}

/**
 * View prediction details in modal or expanded view
 */
function viewPredictionDetails(prediction) {
    alert(`Full prediction details:\n\n` +
        `Cost: $${prediction.results.predicted_cost.toFixed(2)}\n` +
        `CO₂: ${prediction.results.predicted_co2.toFixed(4)} kg\n` +
        `Timestamp: ${new Date(prediction.timestamp).toLocaleString()}\n\n` +
        `Click the download button to get the full CSV report.`);
}

/**
 * Download specific prediction as CSV
 */
function downloadPredictionCSV(index) {
    const predictions = JSON.parse(localStorage.getItem('ecopackai_predictions') || '[]');
    const prediction = predictions[index];

    if (!prediction) {
        alert('Prediction not found');
        return;
    }

    const rows = [];

    // Header
    rows.push(['Parameter', 'Value']);

    // Metadata
    rows.push(['Prediction ID', `#${String(index + 1).padStart(3, '0')}`]);
    rows.push(['Timestamp', new Date(prediction.timestamp).toLocaleString()]);
    rows.push(['Prediction Type', prediction.prediction_type || 'all']);
    rows.push(['', '']);

    // Results
    rows.push(['PREDICTION RESULTS', '']);
    if (prediction.results) {
        Object.entries(prediction.results).forEach(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            const formattedValue = typeof value === 'number' ? value.toFixed(4) : value;
            rows.push([label, formattedValue]);
        });
    }

    rows.push(['', '']);

    // Model Info
    if (prediction.metadata) {
        rows.push(['MODEL INFORMATION', '']);
        Object.entries(prediction.metadata).forEach(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            rows.push([label, value]);
        });
    }

    // Convert to CSV
    const csvContent = rows.map(row =>
        row.map(cell => {
            const cellStr = String(cell);
            if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n')) {
                return `"${cellStr.replace(/"/g, '""')}"`;
            }
            return cellStr;
        }).join(',')
    ).join('\n');

    // Download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ecopackai_prediction_${index + 1}_${Date.now()}.csv`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}

/**
 * Download all predictions as CSV
 */
function downloadAllPredictionsCSV() {
    const predictions = JSON.parse(localStorage.getItem('ecopackai_predictions') || '[]');

    if (predictions.length === 0) {
        alert('No predictions to export');
        return;
    }

    const rows = [];

    // Header
    rows.push(['ID', 'Timestamp', 'Predicted Cost ($)', 'Predicted CO₂ (kg)', 'Cost Confidence', 'Cost Model', 'CO₂ Model']);

    // Data
    predictions.forEach((prediction, index) => {
        const results = prediction.results || {};
        const metadata = prediction.metadata || {};

        rows.push([
            `#${String(index + 1).padStart(3, '0')}`,
            new Date(prediction.timestamp).toLocaleString(),
            (results.predicted_cost || 0).toFixed(2),
            (results.predicted_co2 || 0).toFixed(4),
            (results.cost_confidence || 0).toFixed(4),
            metadata.cost_model || 'N/A',
            metadata.co2_model || 'N/A'
        ]);
    });

    // Convert to CSV
    const csvContent = rows.map(row =>
        row.map(cell => {
            const cellStr = String(cell);
            if (cellStr.includes(',') || cellStr.includes('"') || cellStr.includes('\n')) {
                return `"${cellStr.replace(/"/g, '""')}"`;
            }
            return cellStr;
        }).join(',')
    ).join('\n');

    // Download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ecopackai_all_predictions_${Date.now()}.csv`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
}

/**
 * Delete a prediction
 */
function deletePrediction(index) {
    if (!confirm('Are you sure you want to delete this prediction?')) {
        return;
    }

    const predictions = JSON.parse(localStorage.getItem('ecopackai_predictions') || '[]');
    predictions.splice(index, 1);
    localStorage.setItem('ecopackai_predictions', JSON.stringify(predictions));

    // Reload view
    loadPredictionHistory();
}

/**
 * Clear all predictions
 */
function clearAllPredictions() {
    if (!confirm('Are you sure you want to delete ALL predictions? This cannot be undone.')) {
        return;
    }

    localStorage.removeItem('ecopackai_predictions');
    localStorage.removeItem('latest_prediction');

    // Reload view
    loadPredictionHistory();
}

/**
 * Update statistics
 */
function updateStatistics(predictions) {
    if (predictions.length === 0) return;

    const costs = predictions.map(p => p.results?.predicted_cost || 0);
    const co2s = predictions.map(p => p.results?.predicted_co2 || 0);

    const avgCost = costs.reduce((a, b) => a + b, 0) / costs.length;
    const minCost = Math.min(...costs);
    const maxCost = Math.max(...costs);

    const avgCO2 = co2s.reduce((a, b) => a + b, 0) / co2s.length;

    // Update DOM elements if they exist
    const avgCostEl = document.getElementById('statAvgCost');
    const costRangeEl = document.getElementById('statCostRange');
    const avgCO2El = document.getElementById('statAvgCO2');

    if (avgCostEl) avgCostEl.textContent = `$${avgCost.toFixed(2)}`;
    if (costRangeEl) costRangeEl.textContent = `$${minCost.toFixed(2)} - $${maxCost.toFixed(2)}`;
    if (avgCO2El) avgCO2El.textContent = `${avgCO2.toFixed(3)} kg`;
}

// Expose functions to global scope
window.viewPredictionDetails = viewPredictionDetails;
window.downloadPredictionCSV = downloadPredictionCSV;
window.downloadAllPredictionsCSV = downloadAllPredictionsCSV;
window.deletePrediction = deletePrediction;
window.clearAllPredictions = clearAllPredictions;

console.log('✅ results.js loaded successfully');
