/**
 * EcoPackAI - Prediction Form Validation & API Integration
 * Client-side validation and submission logic for material predictions
 */

// API Configuration
const API_BASE_URL = 'http://localhost:5000';
const API_ENDPOINTS = {
    predictAll: `${API_BASE_URL}/api/v1/predict/all`,
    predictCost: `${API_BASE_URL}/api/v1/predict/cost`,
    predictCO2: `${API_BASE_URL}/api/v1/predict/co2`,
    health: `${API_BASE_URL}/health`
};

// Field Validation Rules
const VALIDATION_RULES = {
    // Sustainability Metrics (Percentages 0-100)
    recyclability_percent: { min: 0, max: 100, type: 'float', unit: '%' },
    recycled_content_percent: { min: 0, max: 100, type: 'float', unit: '%' },
    reusability_percent: { min: 0, max: 100, type: 'float', unit: '%' },
    biodegradation_time_days: { min: 0, max: 3650, type: 'integer', unit: 'days' },
    end_of_life_disposal_percent: { min: 0, max: 100, type: 'float', unit: '%' },
    waste_reduction_impact_percent: { min: 0, max: 100, type: 'float', unit: '%' },

    // Environmental Impact
    carbon_footprint_kg_co2_unit: { min: 0, max: 50, type: 'float', unit: 'kg CO₂' },
    sustainability_target_progress_percent: { min: 0, max: 100, type: 'float', unit: '%' },
    co2_impact_index: { min: 0, max: 1, type: 'float', unit: '' },

    // Material Properties (Scores 1-10)
    load_handling_score: { min: 1, max: 10, type: 'float', unit: '' },
    moisture_resistance_score: { min: 1, max: 10, type: 'float', unit: '' },
    thermal_resistance_score: { min: 1, max: 10, type: 'float', unit: '' },

    // Usage & Supply Chain
    annual_usage_units: { min: 0, max: null, type: 'integer', unit: 'units' },
    total_material_weight_tons: { min: 0, max: null, type: 'float', unit: 'tons' },
    supplier_sustainability_compliance_percent: { min: 0, max: 100, type: 'float', unit: '%' },

    // Composite Scores
    cost_efficiency_index: { min: 0, max: 1, type: 'float', unit: '' },
    material_suitability_score: { min: 0, max: 100, type: 'float', unit: '' },
    overall_sustainability_score: { min: 0, max: 1, type: 'float', unit: '' }
};

// Required fields (all 18 features)
const REQUIRED_FIELDS = Object.keys(VALIDATION_RULES);

// Store last prediction results
let lastPredictionResults = null;

/**
 * Initialize form when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    initializeForm();
    checkAPIHealth();
});

/**
 * Initialize form event listeners and validation
 */
function initializeForm() {
    const form = document.getElementById('predictionForm');

    if (!form) {
        console.error('Prediction form not found');
        return;
    }

    // Add submit event listener
    form.addEventListener('submit', handleFormSubmit);

    // Add real-time validation to all inputs
    REQUIRED_FIELDS.forEach(fieldName => {
        const input = document.getElementById(fieldName);
        if (input) {
            // Validate on blur
            input.addEventListener('blur', () => validateField(fieldName));

            // Clear error on focus
            input.addEventListener('focus', () => {
                input.classList.remove('is-invalid', 'is-valid');
            });

            // Validate on input for immediate feedback
            input.addEventListener('input', () => {
                if (input.value) {
                    validateField(fieldName);
                }
            });
        }
    });

    console.log('✅ Form initialized successfully');
}

/**
 * Check API health status
 */
async function checkAPIHealth() {
    try {
        const response = await fetch(API_ENDPOINTS.health);
        const data = await response.json();

        if (data.status === 'healthy') {
            showAlert('success', '✅ API is healthy and ready for predictions', 3000);
        }
    } catch (error) {
        showAlert('warning', '⚠️ Warning: Could not connect to API. Please ensure the backend is running on localhost:5000', 10000);
    }
}

/**
 * Handle form submission
 */
async function handleFormSubmit(event) {
    event.preventDefault();

    console.log('🚀 Form submission started');

    // Validate all fields
    const validationResult = validateAllFields();

    if (!validationResult.isValid) {
        showAlert('error', `❌ Validation Failed: ${validationResult.errors.join(', ')}`, 5000);
        scrollToFirstError();
        return;
    }

    // Collect form data
    const formData = collectFormData();
    console.log('📦 Form data collected:', formData);

    // Submit to API
    await submitPrediction(formData);
}

/**
 * Validate a single field
 */
function validateField(fieldName) {
    const input = document.getElementById(fieldName);
    const rules = VALIDATION_RULES[fieldName];

    if (!input || !rules) {
        return false;
    }

    const value = input.value.trim();

    // Check if empty
    if (value === '') {
        setFieldInvalid(input, 'This field is required');
        return false;
    }

    // Parse value
    const numValue = parseNumber(value);

    // Check if numeric
    if (isNaN(numValue)) {
        setFieldInvalid(input, 'Please enter a valid number');
        return false;
    }

    // Check minimum
    if (rules.min !== null && numValue < rules.min) {
        setFieldInvalid(input, `Value must be at least ${rules.min}`);
        return false;
    }

    // Check maximum
    if (rules.max !== null && numValue > rules.max) {
        setFieldInvalid(input, `Value must not exceed ${rules.max}`);
        return false;
    }

    // Check integer requirement
    if (rules.type === 'integer' && !Number.isInteger(numValue)) {
        setFieldInvalid(input, 'Value must be a whole number');
        return false;
    }

    // Validation passed
    setFieldValid(input);
    return true;
}

/**
 * Validate all fields in the form
 */
function validateAllFields() {
    const errors = [];
    let isValid = true;

    REQUIRED_FIELDS.forEach(fieldName => {
        const fieldValid = validateField(fieldName);

        if (!fieldValid) {
            isValid = false;
            const input = document.getElementById(fieldName);
            const label = document.querySelector(`label[for="${fieldName}"]`);
            const fieldLabel = label ? label.textContent.split('*')[0].trim() : fieldName;
            errors.push(fieldLabel);
        }
    });

    return {
        isValid,
        errors: errors.slice(0, 3) // Limit to first 3 errors
    };
}

/**
 * Collect form data into a structured object
 */
function collectFormData() {
    const data = {};

    REQUIRED_FIELDS.forEach(fieldName => {
        const input = document.getElementById(fieldName);
        if (input) {
            const value = parseNumber(input.value.trim());
            data[fieldName] = value;
        }
    });

    return data;
}

/**
 * Submit prediction to API
 */
async function submitPrediction(data) {
    const predictBtn = document.getElementById('predictBtn');
    const btnText = document.getElementById('btnText');

    // Show loading state
    predictBtn.disabled = true;
    btnText.innerHTML = '<span class="spinner"></span> Predicting...';

    try {
        console.log('📡 Sending request to API...');

        const response = await fetch(API_ENDPOINTS.predictAll, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || 'Prediction failed');
        }

        console.log('✅ Prediction successful:', result);

        // Store results
        lastPredictionResults = result;

        // Save to localStorage for results page
        savePredictionToStorage(result, data);

        // Display results
        displayResults(result);

        // Show success message
        showAlert('success', '✅ Prediction completed successfully! Click "View Results" to see on results page.', 5000);

    } catch (error) {
        console.error('❌ Prediction error:', error);
        showAlert('error', `❌ ERROR: ${error.message}`, 10000);
    } finally {
        // Reset button
        predictBtn.disabled = false;
        btnText.textContent = 'Get Prediction';
    }
}

/**
 * Display prediction results
 */
function displayResults(result) {
    const resultsContainer = document.getElementById('resultsContainer');
    const { results, metadata, timestamp } = result;

    // Update timestamp
    const timestampEl = document.getElementById('resultTimestamp');
    timestampEl.textContent = `Generated at ${formatTimestamp(timestamp)}`;

    // Update cost values
    document.getElementById('costValue').textContent = `$${results.predicted_cost.toFixed(2)}`;
    document.getElementById('costConfidence').textContent = `${(results.cost_confidence * 100).toFixed(1)}%`;

    // Update CO2 values
    document.getElementById('co2Value').textContent = results.predicted_co2.toFixed(4);

    // Update model information if available
    if (metadata) {
        document.getElementById('costModel').textContent = metadata.cost_model || 'Random Forest';
        document.getElementById('co2Model').textContent = metadata.co2_model || 'XGBoost';
        document.getElementById('costR2').textContent = metadata.cost_r2 ? metadata.cost_r2.toFixed(3) : '0.997';
        document.getElementById('co2R2').textContent = metadata.co2_r2 ? metadata.co2_r2.toFixed(3) : '0.994';
    }

    // Show results container with animation
    resultsContainer.classList.remove('d-none');
    resultsContainer.classList.add('fade-in');

    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Automatically fetch recommendations
    fetchAndDisplayRecommendations();
}

/**
 * Fetch and display material recommendations
 */
async function fetchAndDisplayRecommendations() {
    // Check if recommendations module is available
    if (typeof getRecommendations !== 'function') {
        console.warn('Recommendations module not loaded');
        return;
    }

    try {
        const formData = collectFormData();
        const rankingMode = document.getElementById('rankingMode')?.value || 'balanced';

        console.log('🔍 Fetching recommendations...');

        // Get recommendations from API
        const recommendationsData = await getRecommendations(formData, rankingMode, 5);

        if (recommendationsData && recommendationsData.recommendations) {
            // Store recommendations globally
            window.currentRecommendations = recommendationsData.recommendations;

            // Render recommendations table
            renderRecommendationsTable(recommendationsData.recommendations, rankingMode);

            // Update recommendations stats
            const statsEl = document.getElementById('recommendationsCount');
            if (statsEl) {
                statsEl.textContent = `${recommendationsData.recommendations.length} recommendations (${rankingMode} mode)`;
            }

            // Update subtitle
            const subtitleEl = document.getElementById('recommendationsSubtitle');
            if (subtitleEl) {
                subtitleEl.textContent = `Top ${recommendationsData.recommendations.length} materials ranked by ${rankingMode} criteria`;
            }

            // Show recommendations container
            const recommendationsContainer = document.getElementById('recommendationsContainer');
            if (recommendationsContainer) {
                recommendationsContainer.classList.remove('d-none');
                recommendationsContainer.classList.add('fade-in');
            }

            showAlert('success', '✅ Recommendations generated successfully!', 3000);
        }
    } catch (error) {
        console.error('❌ Failed to fetch recommendations:', error);
        showAlert('warning', `⚠️ Could not generate recommendations: ${error.message}`, 5000);
    }
}

/**
 * Refresh recommendations with new ranking mode
 */
async function refreshRecommendations() {
    if (!lastPredictionResults) {
        showAlert('warning', 'Please run a prediction first', 3000);
        return;
    }

    // Show loading indicator (could be enhanced)
    showAlert('info', '🔄 Refreshing recommendations...', 2000);

    // Fetch with new mode
    await fetchAndDisplayRecommendations();
}

// Expose refreshRecommendations to global scope
window.refreshRecommendations = refreshRecommendations;

/**
 * Reset the form
 */
function resetForm() {
    const form = document.getElementById('predictionForm');
    form.reset();

    // Clear validation states
    REQUIRED_FIELDS.forEach(fieldName => {
        const input = document.getElementById(fieldName);
        if (input) {
            input.classList.remove('is-valid', 'is-invalid');
        }
    });

    // Hide results
    const resultsContainer = document.getElementById('resultsContainer');
    resultsContainer.classList.add('d-none');

    showAlert('info', 'Form has been reset', 3000);
}

/**
 * Prepare for new prediction (keep results visible)
 */
function newPrediction() {
    resetForm();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Save prediction results to localStorage
 */
function savePredictionToStorage(result, inputData) {
    try {
        // Get existing predictions
        const existingPredictions = JSON.parse(localStorage.getItem('ecopackai_predictions') || '[]');

        // Create prediction record
        const prediction = {
            id: Date.now(),
            timestamp: result.timestamp || new Date().toISOString(),
            prediction_type: result.prediction_type || 'all',
            results: result.results,
            metadata: result.metadata,
            input_data: inputData
        };

        // Add to beginning of array (most recent first)
        existingPredictions.unshift(prediction);

        // Keep only last 50 predictions
        if (existingPredictions.length > 50) {
            existingPredictions.splice(50);
        }

        // Save back to localStorage
        localStorage.setItem('ecopackai_predictions', JSON.stringify(existingPredictions));
        localStorage.setItem('latest_prediction', JSON.stringify(prediction));

        console.log('✅ Prediction saved to localStorage');
    } catch (error) {
        console.error('Failed to save to localStorage:', error);
    }
}

/**
 * Save results to JSON or CSV file
 */
function saveResults(format = 'json') {
    if (!lastPredictionResults) {
        showAlert('warning', 'No results to save', 3000);
        return;
    }

    if (format === 'csv') {
        // Export as CSV
        exportResultsAsCSV(lastPredictionResults);
    } else {
        // Export as JSON (original functionality)
        const dataStr = JSON.stringify(lastPredictionResults, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });

        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `ecopackai_prediction_${Date.now()}.json`;

        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        URL.revokeObjectURL(url);

        showAlert('success', '💾 Results saved as JSON', 3000);
    }
}

/**
 * Export results as CSV
 */
function exportResultsAsCSV(result) {
    const rows = [];

    // Header
    rows.push(['Parameter', 'Value']);

    // Metadata
    rows.push(['Timestamp', result.timestamp || new Date().toISOString()]);
    rows.push(['Prediction Type', result.prediction_type || 'all']);
    rows.push(['', '']);

    // Results
    rows.push(['PREDICTION RESULTS', '']);
    if (result.results) {
        Object.entries(result.results).forEach(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            const formattedValue = typeof value === 'number' ? value.toFixed(4) : value;
            rows.push([label, formattedValue]);
        });
    }

    rows.push(['', '']);

    // Model Info
    if (result.metadata) {
        rows.push(['MODEL INFORMATION', '']);
        Object.entries(result.metadata).forEach(([key, value]) => {
            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            rows.push([label, value]);
        });
    }

    // Convert to CSV string
    const csvContent = rows.map(row =>
        row.map(cell => {
            // Escape cells that contain commas or quotes
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
    link.download = `ecopackai_prediction_${Date.now()}.csv`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);

    showAlert('success', '📊 Results exported as CSV', 3000);
}

/**
 * View results on results page
 */
function viewOnResultsPage() {
    if (!lastPredictionResults) {
        showAlert('warning', 'No results to view', 3000);
        return;
    }

    // Ensure data is saved
    savePredictionToStorage(lastPredictionResults, collectFormData());

    // Navigate to results page
    window.location.href = 'results.html';
}

/**
 * Utility: Set field as invalid
 */
function setFieldInvalid(input, message) {
    input.classList.remove('is-valid');
    input.classList.add('is-invalid');

    const feedback = input.nextElementSibling;
    if (feedback && feedback.classList.contains('invalid-feedback')) {
        feedback.textContent = message;
    }
}

/**
 * Utility: Set field as valid
 */
function setFieldValid(input) {
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
}

/**
 * Utility: Parse number (handles both integer and float)
 */
function parseNumber(value) {
    return parseFloat(value);
}

/**
 * Utility: Show alert message
 */
function showAlert(type, message, duration = 5000) {
    const container = document.getElementById('alertContainer');

    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;

    container.appendChild(alert);

    // Auto-remove after duration
    setTimeout(() => {
        alert.style.opacity = '0';
        alert.style.transition = 'opacity 0.3s';
        setTimeout(() => {
            container.removeChild(alert);
        }, 300);
    }, duration);
}

/**
 * Utility: Scroll to first error field
 */
function scrollToFirstError() {
    const firstInvalid = document.querySelector('.form-control.is-invalid');
    if (firstInvalid) {
        firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
        firstInvalid.focus();
    }
}

/**
 * Utility: Format timestamp
 */
function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

/**
 * Load sample data for testing
 */
function loadSampleData() {
    const sampleData = {
        recyclability_percent: 95.0,
        recycled_content_percent: 70.0,
        reusability_percent: 50.0,
        biodegradation_time_days: 120,
        end_of_life_disposal_percent: 95.0,
        carbon_footprint_kg_co2_unit: 1.8,
        waste_reduction_impact_percent: 80.0,
        sustainability_target_progress_percent: 85.0,
        load_handling_score: 8.0,
        moisture_resistance_score: 7.0,
        thermal_resistance_score: 7.0,
        annual_usage_units: 15000,
        total_material_weight_tons: 7.5,
        supplier_sustainability_compliance_percent: 90.0,
        co2_impact_index: 0.25,
        cost_efficiency_index: 0.75,
        material_suitability_score: 70.0,
        overall_sustainability_score: 0.85
    };

    Object.keys(sampleData).forEach(fieldName => {
        const input = document.getElementById(fieldName);
        if (input) {
            input.value = sampleData[fieldName];
        }
    });

    showAlert('info', '📋 Sample data loaded. You can now submit for testing.', 5000);
}

// Expose functions to global scope for inline event handlers
window.resetForm = resetForm;
window.newPrediction = newPrediction;
window.saveResults = saveResults;
window.loadSampleData = loadSampleData;
window.viewOnResultsPage = viewOnResultsPage;
window.exportResultsAsCSV = exportResultsAsCSV;

console.log('✅ predict.js loaded successfully');
