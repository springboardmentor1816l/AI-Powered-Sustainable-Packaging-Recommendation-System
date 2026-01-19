/**
 * EcoPackAI - Recommendations Module
 * Handles API integration and dynamic table rendering for material recommendations
 */

// API Configuration
const RECOMMENDATION_API = {
    base: 'http://localhost:5000/api/v1/recommend',
    endpoints: {
        recommend: '',
        modes: '/modes',
        health: '/health'
    }
};

// Ranking modes
let availableRankingModes = [
    { name: 'balanced', description: 'Balanced cost and sustainability' },
    { name: 'cost_focused', description: 'Minimize costs' },
    { name: 'eco_focused', description: 'Maximize sustainability' }
];

/**
 * Get material recommendations from API
 */
async function getRecommendations(productData, rankingMode = 'balanced', topN = 5) {
    try {
        console.log('🔍 Requesting recommendations...', { rankingMode, topN });

        const response = await fetch(`${RECOMMENDATION_API.base}${RECOMMENDATION_API.endpoints.recommend}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                product_data: productData,
                ranking_mode: rankingMode,
                top_n: topN,
                include_explanations: true
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Recommendation request failed');
        }

        const data = await response.json();
        console.log('✅ Recommendations received:', data);

        return data;
    } catch (error) {
        console.error('❌ Recommendation error:', error);
        throw error;
    }
}

/**
 * Load available ranking modes from API
 */
async function loadRankingModes() {
    try {
        const response = await fetch(`${RECOMMENDATION_API.base}${RECOMMENDATION_API.endpoints.modes}`);

        if (response.ok) {
            const data = await response.json();
            availableRankingModes = data.modes;
            console.log('✅ Ranking modes loaded:', availableRankingModes);

            // Update mode selector if it exists
            updateModeSelector();
        }
    } catch (error) {
        console.warn('⚠️ Could not load ranking modes, using defaults:', error);
    }
}

/**
 * Update mode selector dropdown
 */
function updateModeSelector() {
    const selector = document.getElementById('rankingMode');
    if (!selector) return;

    selector.innerHTML = '';

    availableRankingModes.forEach(mode => {
        const option = document.createElement('option');
        option.value = mode.name;
        option.textContent = `${mode.name.replace('_', ' ').toUpperCase()} - ${mode.description}`;
        selector.appendChild(option);
    });
}

/**
 * Render recommendations table
 */
function renderRecommendationsTable(recommendations, rankingMode) {
    const container = document.getElementById('recommendationsTableContainer');

    if (!container) {
        console.error('Recommendations table container not found');
        return;
    }

    // Clear existing content
    container.innerHTML = '';

    // Create table wrapper
    const wrapper = document.createElement('div');
    wrapper.className = 'table-responsive';

    // Create table
    const table = document.createElement('table');
    table.className = 'recommendations-table';
    table.innerHTML = `
    <thead>
      <tr>
        <th class="rank-col">Rank</th>
        <th class="material-col">Material</th>
        <th class="cost-col">Cost ($)</th>
        <th class="co2-col">CO₂ (kg)</th>
        <th class="sustainability-col">Sustainability</th>
        <th class="score-col">Ranking Score</th>
        <th class="action-col">Details</th>
      </tr>
    </thead>
    <tbody id="recommendationsTableBody">
    </tbody>
  `;

    wrapper.appendChild(table);
    container.appendChild(wrapper);

    // Populate table body
    const tbody = document.getElementById('recommendationsTableBody');

    recommendations.forEach((rec, index) => {
        const row = createRecommendationRow(rec, index);
        tbody.appendChild(row);
    });

    // Show container with animation
    container.classList.remove('d-none');
    container.classList.add('fade-in');

    // Scroll to table
    container.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    console.log(`✅ Rendered ${recommendations.length} recommendations`);
}

/**
 * Create a single recommendation table row
 */
function createRecommendationRow(rec, index) {
    const row = document.createElement('tr');
    row.className = 'recommendation-row';
    row.dataset.rank = rec.rank;

    // Add top-3 highlight
    if (rec.rank <= 3) {
        row.classList.add(`rank-${rec.rank}`);
    }

    // Rank column with badge
    const rankCell = document.createElement('td');
    rankCell.className = 'rank-cell';
    rankCell.innerHTML = `<span class="rank-badge rank-${rec.rank}">${rec.rank}</span>`;

    // Material name
    const materialCell = document.createElement('td');
    materialCell.className = 'material-cell';
    materialCell.innerHTML = `
    <strong>${rec.material_name}</strong>
    ${rec.rank === 1 ? '<span class="badge badge-success ml-2">Recommended</span>' : ''}
  `;

    // Cost
    const costCell = document.createElement('td');
    costCell.className = 'cost-cell';
    costCell.innerHTML = `
    <span class="metric-value">$${rec.predicted_cost.toFixed(2)}</span>
    <small class="confidence">${(rec.cost_confidence * 100).toFixed(0)}% conf.</small>
  `;

    // CO₂
    const co2Cell = document.createElement('td');
    co2Cell.className = 'co2-cell';
    co2Cell.innerHTML = `<span class="metric-value">${rec.predicted_co2.toFixed(4)}</span>`;

    // Sustainability score
    const susCell = document.createElement('td');
    susCell.className = 'sustainability-cell';
    const susPercent = (rec.sustainability_score * 100).toFixed(0);
    susCell.innerHTML = `
    <div class="progress-container">
      <div class="progress">
        <div class="progress-bar" style="width: ${susPercent}%"></div>
      </div>
      <span class="progress-text">${susPercent}%</span>
    </div>
  `;

    // Ranking score
    const scoreCell = document.createElement('td');
    scoreCell.className = 'score-cell';
    const scorePercent = (rec.ranking_score * 100).toFixed(0);
    scoreCell.innerHTML = `
    <span class="ranking-score" style="color: ${getScoreColor(rec.ranking_score)}">
      ${scorePercent}%
    </span>
  `;

    // Details button
    const actionCell = document.createElement('td');
    actionCell.className = 'action-cell';
    actionCell.innerHTML = `
    <button class="btn-small btn-secondary" onclick="showRecommendationDetails(${index})">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="16" x2="12" y2="12"/>
        <line x1="12" y1="8" x2="12.01" y2="8"/>
      </svg>
      View
    </button>
  `;

    row.appendChild(rankCell);
    row.appendChild(materialCell);
    row.appendChild(costCell);
    row.appendChild(co2Cell);
    row.appendChild(susCell);
    row.appendChild(scoreCell);
    row.appendChild(actionCell);

    return row;
}

/**
 * Get color based on score value
 */
function getScoreColor(score) {
    if (score >= 0.8) return 'var(--success)';
    if (score >= 0.6) return 'var(--primary-green)';
    if (score >= 0.4) return 'var(--warning)';
    return 'var(--error)';
}

/**
 * Show detailed information for a recommendation
 */
let currentRecommendations = [];

function showRecommendationDetails(index) {
    const rec = currentRecommendations[index];

    if (!rec) {
        console.error('Recommendation not found:', index);
        return;
    }

    // Create modal content
    const modalContent = `
    <div class="modal-overlay" id="recommendationModal" onclick="closeRecommendationModal()">
      <div class="modal-content" onclick="event.stopPropagation()">
        <div class="modal-header">
          <h3>
            <span class="rank-badge rank-${rec.rank}">${rec.rank}</span>
            ${rec.material_name}
          </h3>
          <button class="btn-close" onclick="closeRecommendationModal()">×</button>
        </div>
        
        <div class="modal-body">
          <!-- Metrics Grid -->
          <div class="metrics-grid">
            <div class="metric-card">
              <div class="metric-label">Predicted Cost</div>
              <div class="metric-value">$${rec.predicted_cost.toFixed(2)}</div>
              <small>${(rec.cost_confidence * 100).toFixed(0)}% confidence</small>
            </div>
            
            <div class="metric-card">
              <div class="metric-label">CO₂ Emissions</div>
              <div class="metric-value">${rec.predicted_co2.toFixed(4)} kg</div>
              <small>Per unit</small>
            </div>
            
            <div class="metric-card">
              <div class="metric-label">Sustainability Score</div>
              <div class="metric-value">${(rec.sustainability_score * 100).toFixed(0)}%</div>
              <small>Overall rating</small>
            </div>
            
            <div class="metric-card">
              <div class="metric-label">Ranking Score</div>
              <div class="metric-value" style="color: ${getScoreColor(rec.ranking_score)}">
                ${(rec.ranking_score * 100).toFixed(0)}%
              </div>
              <small>Composite ranking</small>
            </div>
          </div>
          
          <!-- Additional Metrics -->
          <div class="additional-metrics">
            <h4>Material Characteristics</h4>
            <div class="metric-row">
              <span class="label">Cost Efficiency Index:</span>
              <span class="value">${(rec.cost_efficiency_index * 100).toFixed(0)}%</span>
            </div>
            <div class="metric-row">
              <span class="label">CO₂ Impact Index:</span>
              <span class="value">${(rec.co2_impact_index * 100).toFixed(0)}%</span>
            </div>
            <div class="metric-row">
              <span class="label">Material Suitability:</span>
              <span class="value">${(rec.material_suitability_score).toFixed(0)}%</span>
            </div>
          </div>
          
          <!-- Explanation -->
          ${rec.explanation ? `
            <div class="explanation-section">
              <h4>Why This Material?</h4>
              <p>${rec.explanation}</p>
            </div>
          ` : ''}
        </div>
        
        <div class="modal-footer">
          <button class="btn btn-secondary" onclick="closeRecommendationModal()">Close</button>
          <button class="btn btn-primary" onclick="selectRecommendation(${index})">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="20 6 9 17 4 12"/>
            </svg>
            Select This Material
          </button>
        </div>
      </div>
    </div>
  `;

    // Add modal to page
    const existingModal = document.getElementById('recommendationModal');
    if (existingModal) {
        existingModal.remove();
    }

    document.body.insertAdjacentHTML('beforeend', modalContent);

    // Add animation
    setTimeout(() => {
        const modal = document.getElementById('recommendationModal');
        if (modal) {
            modal.classList.add('show');
        }
    }, 10);
}

/**
 * Close recommendation modal
 */
function closeRecommendationModal() {
    const modal = document.getElementById('recommendationModal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

/**
 * Select a recommendation
 */
function selectRecommendation(index) {
    const rec = currentRecommendations[index];
    console.log('✅ Material selected:', rec.material_name);

    showAlert('success', `✅ Selected: ${rec.material_name} (Rank #${rec.rank})`, 5000);
    closeRecommendationModal();

    // You can add logic here to save the selection or proceed to next step
}

/**
 * Export recommendations to CSV
 */
function exportRecommendations() {
    if (!currentRecommendations || currentRecommendations.length === 0) {
        showAlert('warning', 'No recommendations to export', 3000);
        return;
    }

    // Create CSV content
    const headers = ['Rank', 'Material', 'Cost ($)', 'CO₂ (kg)', 'Sustainability (%)', 'Ranking Score (%)'];
    const rows = currentRecommendations.map(rec => [
        rec.rank,
        rec.material_name,
        rec.predicted_cost.toFixed(2),
        rec.predicted_co2.toFixed(4),
        (rec.sustainability_score * 100).toFixed(0),
        (rec.ranking_score * 100).toFixed(0)
    ]);

    const csvContent = [
        headers.join(','),
        ...rows.map(row => row.join(','))
    ].join('\n');

    // Download CSV
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `ecopackai_recommendations_${Date.now()}.csv`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);

    showAlert('success', '💾 Recommendations exported to CSV', 3000);
}

/**
 * Compare top recommendations
 */
function compareTopRecommendations(n = 3) {
    if (!currentRecommendations || currentRecommendations.length < 2) {
        showAlert('warning', 'Need at least 2 recommendations to compare', 3000);
        return;
    }

    const topN = currentRecommendations.slice(0, Math.min(n, currentRecommendations.length));

    // Create comparison modal
    const comparisonContent = `
    <div class="modal-overlay" id="comparisonModal" onclick="closeComparisonModal()">
      <div class="modal-content modal-large" onclick="event.stopPropagation()">
        <div class="modal-header">
          <h3>Top ${topN.length} Materials Comparison</h3>
          <button class="btn-close" onclick="closeComparisonModal()">×</button>
        </div>
        
        <div class="modal-body">
          <div class="comparison-grid">
            ${topN.map(rec => `
              <div class="comparison-card rank-${rec.rank}">
                <div class="comparison-header">
                  <span class="rank-badge rank-${rec.rank}">#${rec.rank}</span>
                  <h4>${rec.material_name}</h4>
                </div>
                
                <div class="comparison-metrics">
                  <div class="comp-metric">
                    <div class="label">Cost</div>
                    <div class="value">$${rec.predicted_cost.toFixed(2)}</div>
                  </div>
                  <div class="comp-metric">
                    <div class="label">CO₂</div>
                    <div class="value">${rec.predicted_co2.toFixed(3)} kg</div>
                  </div>
                  <div class="comp-metric">
                    <div class="label">Sustainability</div>
                    <div class="value">${(rec.sustainability_score * 100).toFixed(0)}%</div>
                  </div>
                  <div class="comp-metric">
                    <div class="label">Overall Score</div>
                    <div class="value" style="color: ${getScoreColor(rec.ranking_score)}">
                      ${(rec.ranking_score * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
        
        <div class="modal-footer">
          <button class="btn btn-secondary" onclick="closeComparisonModal()">Close</button>
        </div>
      </div>
    </div>
  `;

    document.body.insertAdjacentHTML('beforeend', comparisonContent);

    setTimeout(() => {
        const modal = document.getElementById('comparisonModal');
        if (modal) {
            modal.classList.add('show');
        }
    }, 10);
}

/**
 * Close comparison modal
 */
function closeComparisonModal() {
    const modal = document.getElementById('comparisonModal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

/**
 * Initialize recommendations module
 */
function initRecommendations() {
    console.log('🚀 Recommendations module initialized');

    // Load ranking modes
    loadRankingModes();

    // Check recommendation API health
    checkRecommendationHealth();
}

/**
 * Check recommendation API health
 */
async function checkRecommendationHealth() {
    try {
        const response = await fetch(`${RECOMMENDATION_API.base}${RECOMMENDATION_API.endpoints.health}`);
        const data = await response.json();

        if (data.status === 'healthy') {
            console.log('✅ Recommendation API is healthy');
        } else {
            console.warn('⚠️ Recommendation API status:', data.status);
        }
    } catch (error) {
        console.warn('⚠️ Recommendation API health check failed:', error);
    }
}

// Export functions for global access
window.getRecommendations = getRecommendations;
window.renderRecommendationsTable = renderRecommendationsTable;
window.showRecommendationDetails = showRecommendationDetails;
window.closeRecommendationModal = closeRecommendationModal;
window.selectRecommendation = selectRecommendation;
window.exportRecommendations = exportRecommendations;
window.compareTopRecommendations = compareTopRecommendations;
window.closeComparisonModal = closeComparisonModal;
window.currentRecommendations = currentRecommendations;

// Initialize on DOM load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initRecommendations);
} else {
    initRecommendations();
}

console.log('✅ recommendations.js loaded successfully');
