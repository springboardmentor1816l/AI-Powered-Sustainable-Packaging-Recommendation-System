# Frontend-Backend Integration Documentation

**Module:** Frontend UI ↔ Flask Backend Integration  
**Task:** Connect Product Input UI with Flask `/recommend` API and Render Recommendations  
**Date:** January 7, 2026  
**Status:** ✅ COMPLETE

---

## 📋 Overview

This document details the complete integration between the EcoPackAI frontend and Flask backend for material recommendations. The integration enables users to:

1. Submit product specifications via the web form
2. Receive AI-powered cost and CO₂ predictions
3. Get ranked sustainable material recommendations
4. Compare and export recommendation results

---

## 🏗️ Architecture

### System Flow

```
┌─────────────────┐
│   User Input    │
│   (18 Fields)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Client-Side    │ ← predict.js
│  Validation     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  POST Request   │
│  /predict/all   │ ← Flask API
└────────┬────────┘
         │
         ├─► Cost Prediction (Random Forest)
         │
         └─► CO₂ Prediction (XGBoost)
         │
         ▼
┌─────────────────┐
│  Display        │
│  Predictions    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  POST Request   │
│  /recommend     │ ← Flask API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ MaterialRanker  │ ← Ranking Engine
│ Rank Materials  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Render Table    │ ← recommendations.js
│ with Rankings   │
└─────────────────┘
```

---

## 🔌 API Integration

### 1. Prediction Endpoint

**Endpoint:** `POST /api/v1/predict/all`

**Purpose:** Get cost and CO₂ predictions for material specifications

**Request Format:**
```javascript
{
  "recyclability_percent": 95.0,
  "recycled_content_percent": 70.0,
  "reusability_percent": 50.0,
  "biodegradation_time_days": 120,
  "end_of_life_disposal_percent": 95.0,
  "carbon_footprint_kg_co2_unit": 1.8,
  "waste_reduction_impact_percent": 80.0,
  "sustainability_target_progress_percent": 85.0,
  "load_handling_score": 8.0,
  "moisture_resistance_score": 7.0,
  "thermal_resistance_score": 7.0,
  "annual_usage_units": 15000,
  "total_material_weight_tons": 7.5,
  "supplier_sustainability_compliance_percent": 90.0,
  "co2_impact_index": 0.25,
  "cost_efficiency_index": 0.75,
  "material_suitability_score": 70.0,
  "overall_sustainability_score": 0.85
}
```

**Response Format:**
```javascript
{
  "status": "success",
  "timestamp": "2026-01-07T19:45:00",
  "prediction_type": "all",
  "results": {
    "predicted_cost": 12.45,
    "cost_confidence": 0.85,
    "predicted_co2": 1.234
  },
  "metadata": {
    "cost_model": "Random Forest",
    "co2_model": "XGBoost",
    "cost_r2": 0.997,
    "co2_r2": 0.994
  }
}
```

**Frontend Implementation:**
```javascript
// In predict.js
const response = await fetch(`${API_BASE_URL}/api/v1/predict/all`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
});

const result = await response.json();
displayResults(result);
```

---

### 2. Recommendation Endpoint

**Endpoint:** `POST /api/v1/recommend`

**Purpose:** Get ranked material recommendations based on product specifications

**Request Format:**
```javascript
{
  "product_data": {
    // All 18 features (same as prediction)
    "recyclability_percent": 95.0,
    "recycled_content_percent": 70.0,
    // ... etc
  },
  "ranking_mode": "balanced",      // balanced | cost_focused | eco_focused
  "top_n": 5,                       // Number of recommendations
  "include_explanations": true      // Include ranking explanations
}
```

**Response Format:**
```javascript
{
  "status": "success",
  "timestamp": "2026-01-07T19:45:00",
  "ranking_mode": "balanced",
  "top_n": 5,
  "total_evaluated": 10,
  "recommendations": [
    {
      "rank": 1,
      "material_name": "Recycled Cardboard",
      "predicted_cost": 9.96,
      "predicted_co2": 0.864,
      "sustainability_score": 1.02,
      "ranking_score": 0.92,
      "cost_confidence": 0.87,
      "cost_efficiency_index": 0.94,
      "co2_impact_index": 0.175,
      "material_suitability_score": 70.0,
      "explanation": "This material ranks #1 due to excellent balance..."
    },
    // ... more recommendations
  ],
  "input_data_summary": {
    "recyclability_percent": 95.0,
    "cost_efficiency_index": 0.75,
    "overall_sustainability_score": 0.85
  }
}
```

**Frontend Implementation:**
```javascript
// In recommendations.js
const recommendationsData = await getRecommendations(
  formData,           // Product specifications
  'balanced',         // Ranking mode
  5                   // Number of recommendations
);

renderRecommendationsTable(recommendationsData.recommendations);
```

---

### 3. Ranking Modes Endpoint

**Endpoint:** `GET /api/v1/recommend/modes`

**Purpose:** Get available ranking modes and their configurations

**Response Format:**
```javascript
{
  "status": "success",
  "modes": [
    {
      "name": "balanced",
      "description": "Balanced weighting of cost and sustainability",
      "weights": {
        "cost": 0.35,
        "co2": 0.35,
        "sustainability": 0.30
      }
    },
    {
      "name": "cost_focused",
      "description": "Prioritizes lower costs",
      "weights": {
        "cost": 0.60,
        "co2": 0.20,
        "sustainability": 0.20
      }
    },
    {
      "name": "eco_focused",
      "description": "Maximizes environmental sustainability",
      "weights": {
        "cost": 0.20,
        "co2": 0.40,
        "sustainability": 0.40
      }
    }
  ]
}
```

---

## 🎨 Frontend Components

### File Structure

```
frontend/
├── predict.html                          # Main prediction page
├── static/
│   ├── css/
│   │   ├── style.css                     # Base styles
│   │   └── recommendations.css           # NEW: Recommendation table styles
│   └── js/
│       ├── predict.js                     # UPDATED: Added recommendations call
│       └── recommendations.js             # NEW: Recommendation logic
```

### 1. HTML Structure (predict.html)

#### Recommendations Section
```html
<!-- Recommendations Container (Hidden by default) -->
<div id="recommendationsContainer" class="d-none">
  <div class="card">
    <div class="card-header">
      <!-- Mode Selector -->
      <select id="rankingMode" class="form-select">
        <option value="balanced">Balanced</option>
        <option value="cost_focused">Cost Focused</option>
        <option value="eco_focused">Eco Focused</option>
      </select>
      <button onclick="refreshRecommendations()">Refresh</button>
    </div>
    
    <!-- Action Buttons -->
    <div>
      <button onclick="compareTopRecommendations(3)">Compare Top 3</button>
      <button onclick="exportRecommendations()">Export CSV</button>
    </div>
    
    <!-- Dynamic Table Container -->
    <div id="recommendationsTableContainer"></div>
  </div>
</div>
```

### 2. JavaScript Modules

#### predict.js - Main Integration
```javascript
// After displaying prediction results, automatically fetch recommendations
function displayResults(result) {
  // ... display cost and CO2 predictions
  
  // Automatically fetch recommendations
  fetchAndDisplayRecommendations();
}

async function fetchAndDisplayRecommendations() {
  const formData = collectFormData();
  const rankingMode = document.getElementById('rankingMode').value;
  
  const recommendationsData = await getRecommendations(formData, rankingMode, 5);
  
  // Store globally
  window.currentRecommendations = recommendationsData.recommendations;
  
  // Render table
  renderRecommendationsTable(recommendationsData.recommendations);
  
  // Show container
  document.getElementById('recommendationsContainer').classList.remove('d-none');
}
```

#### recommendations.js - Recommendation Logic
```javascript
// API call
async function getRecommendations(productData, rankingMode, topN) {
  const response = await fetch(`${API_BASE_URL}/api/v1/recommend`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      product_data: productData,
      ranking_mode: rankingMode,
      top_n: topN,
      include_explanations: true
    })
  });
  
  return await response.json();
}

// Dynamic table rendering
function renderRecommendationsTable(recommendations) {
  // Creates table with columns:
  // - Rank (with badge styling for top 3)
  // - Material Name
  // - Cost
  // - CO₂
  // - Sustainability (progress bar)
  // - Ranking Score
  // - Details button
}

// Modal details view
function showRecommendationDetails(index) {
  // Shows detailed metrics and explanation in modal
}

// Comparison view
function compareTopRecommendations(n) {
  // Side-by-side comparison of top N materials
}

// Export functionality
function exportRecommendations() {
  // Downloads CSV file with recommendations
}
```

---

## 📊 Data Flow Mapping

### Frontend → Backend

| Frontend Field | Backend Parameter | Validation |
|----------------|-------------------|------------|
| `#recyclability_percent` | `recyclability_percent` | 0-100, float |
| `#recycled_content_percent` | `recycled_content_percent` | 0-100, float |
| `#reusability_percent` | `reusability_percent` | 0-100, float |
| ... (all 18 fields) | ... | ... |

**Transformation:** None required - direct 1:1 mapping

**Data Collection:**
```javascript
function collectFormData() {
  const data = {};
  REQUIRED_FIELDS.forEach(fieldName => {
    const input = document.getElementById(fieldName);
    data[fieldName] = parseFloat(input.value);
  });
  return data;
}
```

### Backend → Frontend

| Backend Field | Frontend Display | Format |
|---------------|------------------|--------|
| `rank` | Rank badge | Integer, styled 1-3 |
| `material_name` | Material column | String with badge |
| `predicted_cost` | Cost column | `$XX.XX` + confidence |
| `predicted_co2` | CO₂ column | `X.XXXX kg` |
| `sustainability_score` | Progress bar | 0-100% |
| `ranking_score` | Score column | 0-100%, color-coded |
| `explanation` | Modal details | Full text |

**Rendering Example:**
```javascript
function createRecommendationRow(rec) {
  return `
    <tr class="rank-${rec.rank}">
      <td><span class="rank-badge rank-${rec.rank}">${rec.rank}</span></td>
      <td><strong>${rec.material_name}</strong></td>
      <td>$${rec.predicted_cost.toFixed(2)}</td>
      <td>${rec.predicted_co2.toFixed(4)} kg</td>
      <td><progress value="${rec.sustainability_score * 100}">...</progress></td>
      <td>${(rec.ranking_score * 100).toFixed(0)}%</td>
      <td><button onclick="showDetails(...)">View</button></td>
    </tr>
  `;
}
```

---

## 🎯 User Interaction Flow

### Complete User Journey

1. **User opens predict.html**
   - Form loads with 18 input fields
   - API health check runs automatically
   - Success: "✅ API is healthy"

2. **User fills form (or uses sample data)**
   - Real-time validation on blur
   - Green borders for valid fields
   - Red borders for invalid fields
   - Descriptive error messages

3. **User clicks "Get Prediction"**
   - Form validation runs
   - If invalid: Alert + scroll to first error
   - If valid: Loading state shown
   - API call to `/predict/all`

4. **Prediction results display**
   - Cost metric card appears
   - CO₂ metric card appears
   - Model information table shown
   - Smooth scroll to results

5. **Recommendations auto-fetch**
   - Automatic call to `/recommend` API
   - Loading handled silently
   - Table renders below results
   - Success alert: "✅ Recommendations generated"

6. **User interacts with recommendations**
   - **View Details:** Click "View" button
     - Modal opens with full metrics
     - Explanation shown
     - "Select Material" button
   
   - **Change Ranking Mode:** Select dropdown
     - Click refresh button
     - Table updates with new rankings
   
   - **Compare:** Click "Compare Top 3"
     - Modal with side-by-side comparison
     - Shows all metrics for top 3
   
   - **Export:** Click "Export CSV"
     - Downloads CSV file
     - Filename: `ecopackai_recommendations_[timestamp].csv`

---

## 🧪 Testing Guide

### Manual Testing Checklist

#### Setup
- [ ] Backend running on `localhost:5000`
- [ ] Frontend served (e.g., `python -m http.server 8000`)
- [ ] Browser open to `http://localhost:8000/predict.html`

#### Test 1: Basic Prediction Flow
1. Load sample data: Open console, run `loadSampleData()`
2. Click "Get Prediction"
3. **Expected:**
   - ✅ Results appear
   - ✅ Recommendations table appears
   - ✅ 5 materials ranked
   - ✅ Rank #1 highlighted with gold badge

#### Test 2: Validation
1. Leave fields empty
2. Click "Get Prediction"
3. **Expected:**
   - ❌ Error alert
   - ❌ Red borders on empty fields
   - ❌ Scroll to first invalid field

#### Test 3: Ranking Modes
1. Run prediction
2. Change ranking mode dropdown
3. Click refresh button
4. **Expected:**
   - ✅ Table re-renders
   - ✅ Different ranking order
   - ✅ Stats update

#### Test 4: Detail Modal
1. Click "View" on any recommendation
2. **Expected:**
   - ✅ Modal opens
   - ✅ All metrics displayed
   - ✅ Explanation text shown
   - ✅ Close button works

#### Test 5: Comparison
1. Click "Compare Top 3"
2. **Expected:**
   - ✅ Comparison modal opens
   - ✅ 3 cards shown side-by-side
   - ✅ All metrics visible
   - ✅ Visual rank indicators

#### Test 6: Export
1. Click "Export CSV"
2. **Expected:**
   - ✅ CSV file downloads
   - ✅ Contains all recommendation data
   - ✅ Proper formatting

### API Testing

#### Test Recommendation Endpoint
```bash
curl -X POST http://localhost:5000/api/v1/recommend \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

**Expected Response:**
```json
{
  "status": "success",
  "recommendations": [...],
  "ranking_mode": "balanced"
}
```

#### Test Modes Endpoint
```bash
curl http://localhost:5000/api/v1/recommend/modes
```

**Expected Response:**
```json
{
  "status": "success",
  "modes": [{...}, {...}, {...}]
}
```

---

## 🐛 Error Handling

### Frontend Error Scenarios

| Error | Detection | Handling |
|-------|-----------|----------|
| Empty fields | Client validation | Alert + scroll to field |
| Invalid values | Client validation | Red border + error message |
| API unavailable | Fetch promise reject | Warning alert |
| Network timeout | Fetch timeout | Error alert with retry |
| 400 Bad Request | Response status | Parse error message, show alert |
| 500 Server Error | Response status | Generic error alert |
| Missing recommendations | Check response | Warning, hide table |

### Error Messages

**Client-Side:**
```javascript
// Validation errors
"❌ Validation Failed: Recyclability, Recycled Content, Reusability"

// API errors
"⚠️ Could not generate recommendations: Missing required features"
```

**Server-Side:**
```json
{
  "error": "Missing required features: recyclability_percent",
  "missing_features": ["recyclability_percent"],
  "status": "error"
}
```

---

## 🚀 Deployment Checklist

### Backend Deployment

- [ ] Update `recommend.py` with production model paths
- [ ] Verify MaterialRanker is initialized correctly
- [ ] Test all ranking modes work
- [ ] Enable error logging
- [ ] Configure CORS for production domain

### Frontend Deployment

- [ ] Update `API_BASE_URL` in both JS files
  ```javascript
  const API_BASE_URL = 'https://your-production-domain.com';
  ```
- [ ] Minify JavaScript files
- [ ] Minify CSS files
- [ ] Test on production backend
- [ ] Verify all features work

### Verification

- [ ] End-to-end test on production
- [ ] Performance check (< 2s for recommendations)
- [ ] Mobile responsiveness verified
- [ ] Cross-browser testing

---

## 📈 Performance Metrics

### Expected Response Times

| Operation | Target | Acceptable |
|-----------|--------|------------|
| Form validation | < 10ms | < 50ms |
| Prediction API call | < 200ms | < 500ms |
| Recommendation API call | < 300ms | < 800ms |
| Table rendering | < 100ms | < 200ms |
| Modal open | < 50ms | < 100ms |

### Optimization Tips

1. **Caching:** Cache ranking modes on first load
2. **Debouncing:** Debounce ranking mode changes
3. **Lazy Loading:** Load recommendations only when needed
4. **Progressive Enhancement:** Show table rows as they're generated

---

## 🔐 Security Considerations

### Input Validation

- ✅ Client-side validation (user experience)
- ✅ Server-side validation (security)
- ✅ Type checking on all inputs
- ✅ Range validation

### API Security

- ✅ CORS configured
- ⚠️ No authentication (add if needed)
- ✅ Rate limiting available
- ✅ Input sanitization

---

## 📚 Additional Resources

### Documentation Files

- `docs/frontend_wireframes.md` - UI specifications
- `docs/frontend_validation_behavior.md` - Validation rules
- `docs/FLASK_API_SUMMARY.md` - Complete API documentation
- `frontend/README.md` - Frontend overview

### Code References

- `backend/routes/recommend.py` - Recommendation endpoint
- `frontend/static/js/recommendations.js` - Recommendation logic
- `frontend/static/css/recommendations.css` - Table styling
- `frontend/predict.html` - Main UI

---

## ✅ Integration Complete

**Status:** ✅ Fully Functional

**Features Implemented:**
- ✅ Prediction API integration
- ✅ Recommendation API integration
- ✅ Dynamic table rendering
- ✅ Multiple ranking modes
- ✅ Detailed modal views
- ✅ Comparison functionality
- ✅ CSV export
- ✅ Error handling
- ✅ Responsive design

**Next Steps:**
- Consider adding user authentication
- Implement prediction history storage
- Add chart visualizations
- Enable batch predictions

---

**Last Updated:** January 7, 2026  
**Version:** 1.0.0  
**Maintainer:** EcoPackAI Development Team
