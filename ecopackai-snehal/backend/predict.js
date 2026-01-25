/**
 * EcoPackAI - Complete Frontend JavaScript
 * Fixed to work with actual API response structure
 */

// ============================================
// CONFIGURATION
// ============================================
const API_BASE_URL = 'http://127.0.0.1:5000';
const API_ENDPOINTS = {
    predict: `${API_BASE_URL}/api/v1/predict`,
    health: `${API_BASE_URL}/health`,
    schema: `${API_BASE_URL}/api/v1/predict/schema`
};

// Global variables for charts
let costChart = null;
let co2Chart = null;
let sustainabilityChart = null;
let currentResults = null;

// ============================================
// FORM VALIDATION & SUBMISSION
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('productForm');
    
    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        event.stopPropagation();
        
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }
        
        if (!validateForm()) {
            return;
        }
        
        await submitPrediction();
    });
    
    addRealTimeValidation();
    checkAPIHealth();
});

function validateForm() {
    const weight = parseFloat(document.getElementById('productWeight').value);
    const fragility = parseInt(document.getElementById('fragilityIndex').value);
    
    if (weight <= 0) {
        showError('Weight must be a positive number');
        return false;
    }
    
    if (fragility < 1 || fragility > 5) {
        showError('Fragility index must be between 1 and 5');
        return false;
    }
    
    return true;
}

function addRealTimeValidation() {
    document.getElementById('productWeight').addEventListener('input', function() {
        const value = parseFloat(this.value);
        if (value <= 0) {
            this.setCustomValidity('Weight must be positive');
        } else {
            this.setCustomValidity('');
        }
    });
    
    document.getElementById('fragilityIndex').addEventListener('input', function() {
        const value = parseInt(this.value);
        if (value < 1 || value > 5) {
            this.setCustomValidity('Must be between 1 and 5');
        } else {
            this.setCustomValidity('');
        }
    });
}

// ============================================
// API INTEGRATION
// ============================================
async function submitPrediction() {
    showLoading();
    hideError();
    hideResults();
    
    const formData = {
        product_name: document.getElementById('productName').value,
        product_category: document.getElementById('productCategory').value,
        product_weight_kg: parseFloat(document.getElementById('productWeight').value),
        fragility_index: parseInt(document.getElementById('fragilityIndex').value),
        shipping_type: document.getElementById('shippingType').value
    };
    
    try {
        console.log('Sending request to:', API_ENDPOINTS.predict);
        console.log('Request data:', formData);
        
        const response = await fetch(API_ENDPOINTS.predict, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (!data.success) {
            throw new Error(data.error || 'Prediction failed');
        }
        
        currentResults = data;
        displayResults(data);
        
    } catch (error) {
        console.error('API Error:', error);
        showError(`Failed to get recommendations: ${error.message}. Make sure Flask server is running on port 5000.`);
    } finally {
        hideLoading();
    }
}

async function checkAPIHealth() {
    try {
        const response = await fetch(API_ENDPOINTS.health);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            console.log('✓ API is healthy');
        }
    } catch (error) {
        console.warn('⚠ API health check failed. Make sure Flask server is running:', error);
    }
}

// ============================================
// RESULTS DISPLAY
// ============================================
function displayResults(data) {
    // Get base prediction from API
    const basePrediction = data.predictions;
    
    // Update main statistics
    document.getElementById('statCost').textContent = `$${basePrediction.cost_usd.toFixed(2)}`;
    document.getElementById('statCO2').textContent = `${basePrediction.co2_kg.toFixed(3)} kg`;
    
    // Generate multiple material recommendations
    const recommendations = generateRecommendations(basePrediction, data.metadata);
    
    // Calculate and display average statistics
    displayAverageStats(recommendations);
    
    // Display recommendations table
    displayRecommendationsTable(recommendations);
    
    // Create all charts
    createAllCharts(recommendations);
    
    // Show results section
    showResults();
    
    // Smooth scroll to results
    setTimeout(() => {
        document.getElementById('resultsSection').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }, 100);
}

function generateRecommendations(basePrediction, metadata) {
    const materials = [
        { name: 'Recycled Cardboard', sustainability: 95, costFactor: 0.9, co2Factor: 0.85 },
        { name: 'Bio-Based Fillers', sustainability: 92, costFactor: 1.1, co2Factor: 0.75 },
        { name: 'Compostable Plastic', sustainability: 88, costFactor: 1.3, co2Factor: 0.9 },
        { name: 'Paper Packaging', sustainability: 85, costFactor: 0.8, co2Factor: 0.8 },
        { name: 'Recycled Plastic', sustainability: 75, costFactor: 0.7, co2Factor: 1.1 },
        { name: 'Standard Cardboard', sustainability: 70, costFactor: 0.6, co2Factor: 1.0 }
    ];
    
    return materials.map((material, index) => {
        const cost = (basePrediction.cost_usd * material.costFactor).toFixed(2);
        const co2 = (basePrediction.co2_kg * material.co2Factor).toFixed(3);
        const score = material.sustainability;
        
        return {
            rank: index + 1,
            material: material.name,
            cost: parseFloat(cost),
            co2: parseFloat(co2),
            score: score,
            sustainability: material.sustainability
        };
    }).sort((a, b) => b.score - a.score)
      .map((rec, idx) => ({ ...rec, rank: idx + 1 }));
}

function displayAverageStats(recommendations) {
    const avgCost = recommendations.reduce((sum, r) => sum + r.cost, 0) / recommendations.length;
    const avgCO2 = recommendations.reduce((sum, r) => sum + r.co2, 0) / recommendations.length;
    const avgSustainability = recommendations.reduce((sum, r) => sum + r.sustainability, 0) / recommendations.length;
    
    // Update stat cards with averages
    document.getElementById('statCost').textContent = `$${avgCost.toFixed(2)}`;
    document.getElementById('statCO2').textContent = `${avgCO2.toFixed(3)} kg`;
    document.getElementById('statScore').textContent = `${avgSustainability.toFixed(0)}/100`;
}

function displayRecommendationsTable(recommendations) {
    const tbody = document.getElementById('resultsBody');
    tbody.innerHTML = '';
    
    recommendations.forEach(rec => {
        const row = document.createElement('tr');
        
        let badgeClass = '';
        if (rec.rank === 1) badgeClass = 'rank-1';
        else if (rec.rank === 2) badgeClass = 'rank-2';
        else if (rec.rank === 3) badgeClass = 'rank-3';
        
        row.innerHTML = `
            <td><span class="badge ${badgeClass}">${rec.rank}</span></td>
            <td><strong>${rec.material}</strong></td>
            <td>$${rec.cost.toFixed(2)}</td>
            <td>${rec.co2.toFixed(3)} kg</td>
            <td>
                <div class="progress" style="height: 25px;">
                    <div class="progress-bar ${rec.score >= 85 ? 'bg-success' : rec.score >= 70 ? 'bg-warning' : 'bg-danger'}" 
                         role="progressbar" 
                         style="width: ${rec.score}%" 
                         aria-valuenow="${rec.score}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        ${rec.score}/100
                    </div>
                </div>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// ============================================
// ENHANCED CHARTS
// ============================================
function createAllCharts(recommendations) {
    if (costChart) costChart.destroy();
    if (co2Chart) co2Chart.destroy();
    if (sustainabilityChart) sustainabilityChart.destroy();
    
    const labels = recommendations.map(r => r.material);
    const costs = recommendations.map(r => r.cost);
    const co2Values = recommendations.map(r => r.co2);
    const scores = recommendations.map(r => r.score);
    
    // Cost Comparison Chart
    const costCtx = document.getElementById('costChart').getContext('2d');
    costChart = new Chart(costCtx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Cost (USD)',
                data: costs,
                backgroundColor: costs.map(cost => {
                    const minCost = Math.min(...costs);
                    return cost === minCost ? 'rgba(40, 167, 69, 0.8)' : 'rgba(40, 167, 69, 0.5)';
                }),
                borderColor: 'rgba(40, 167, 69, 1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Cost Comparison Across Materials',
                    font: { size: 16, weight: 'bold' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Cost: $${context.parsed.y.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
    
    // CO2 Impact Chart
    const co2Ctx = document.getElementById('co2Chart').getContext('2d');
    co2Chart = new Chart(co2Ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'CO₂ Emissions (kg)',
                data: co2Values,
                backgroundColor: 'rgba(32, 201, 151, 0.2)',
                borderColor: 'rgba(32, 201, 151, 1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: co2Values.map(val => {
                    const minCO2 = Math.min(...co2Values);
                    return val === minCO2 ? 'rgba(40, 167, 69, 1)' : 'rgba(32, 201, 151, 1)';
                }),
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'CO₂ Impact Comparison',
                    font: { size: 16, weight: 'bold' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `CO₂: ${context.parsed.y.toFixed(3)} kg`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value.toFixed(3) + ' kg';
                        }
                    }
                }
            }
        }
    });
}

// ============================================
// EXPORT FUNCTIONS
// ============================================
function exportCSV() {
    if (!currentResults) {
        alert('No data to export');
        return;
    }
    
    const recommendations = generateRecommendations(currentResults.predictions, currentResults.metadata);
    
    let csv = 'Rank,Material,Cost (USD),CO2 (kg),Sustainability Score\n';
    
    recommendations.forEach(rec => {
        csv += `${rec.rank},"${rec.material}",${rec.cost.toFixed(2)},${rec.co2.toFixed(3)},${rec.score}\n`;
    });
    
    downloadFile(csv, 'ecopackai_recommendations.csv', 'text/csv');
    console.log('✓ CSV exported');
}

function exportPDF() {
    if (!currentResults) {
        alert('No data to export');
        return;
    }
    
    const recommendations = generateRecommendations(currentResults.predictions, currentResults.metadata);
    
    let content = '='.repeat(60) + '\n';
    content += 'EcoPackAI - Packaging Recommendations Report\n';
    content += '='.repeat(60) + '\n\n';
    content += `Product: ${currentResults.metadata.product}\n`;
    content += `Category: ${currentResults.metadata.category}\n`;
    content += `Weight: ${currentResults.metadata.weight_kg} kg\n`;
    content += `Generated: ${new Date().toLocaleString()}\n\n`;
    content += '='.repeat(60) + '\n';
    content += 'RECOMMENDATIONS\n';
    content += '='.repeat(60) + '\n\n';
    
    recommendations.forEach(rec => {
        content += `${rec.rank}. ${rec.material}\n`;
        content += `   Cost: $${rec.cost.toFixed(2)}\n`;
        content += `   CO₂ Emissions: ${rec.co2.toFixed(3)} kg\n`;
        content += `   Sustainability Score: ${rec.score}/100\n\n`;
    });
    
    content += '='.repeat(60) + '\n';
    content += 'SUMMARY STATISTICS\n';
    content += '='.repeat(60) + '\n';
    const avgCost = recommendations.reduce((sum, r) => sum + r.cost, 0) / recommendations.length;
    const avgCO2 = recommendations.reduce((sum, r) => sum + r.co2, 0) / recommendations.length;
    content += `Average Cost: $${avgCost.toFixed(2)}\n`;
    content += `Average CO₂: ${avgCO2.toFixed(3)} kg\n`;
    content += `Best Option: ${recommendations[0].material}\n`;
    
    downloadFile(content, 'ecopackai_report.txt', 'text/plain');
    
    console.log('✓ Report exported');
    alert('Report downloaded successfully!');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type: type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// ============================================
// UI HELPERS
// ============================================
function showLoading() {
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('btnText').classList.add('d-none');
    document.getElementById('btnSpinner').classList.remove('d-none');
    document.querySelector('button[type="submit"]').disabled = true;
}

function hideLoading() {
    document.getElementById('loadingSpinner').style.display = 'none';
    document.getElementById('btnText').classList.remove('d-none');
    document.getElementById('btnSpinner').classList.add('d-none');
    document.querySelector('button[type="submit"]').disabled = false;
}

function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    document.getElementById('errorText').textContent = message;
    errorDiv.style.display = 'block';
}

function hideError() {
    document.getElementById('errorMessage').style.display = 'none';
}

function showResults() {
    document.getElementById('resultsSection').style.display = 'block';
}

function hideResults() {
    document.getElementById('resultsSection').style.display = 'none';
}

console.log('✓ EcoPackAI Frontend Loaded');
console.log('API Base URL:', API_BASE_URL);
console.log('Make sure Flask server is running: python app.py');