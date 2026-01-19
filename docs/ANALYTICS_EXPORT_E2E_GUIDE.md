# Analytics Visualization & Export Integration Guide

## 📊 Overview

This document provides comprehensive guidance on the Analytics Visualization, Export functionality, and End-to-End UI Testing implemented for EcoPackAI.

**Implementation Date:** January 12, 2026  
**Author:** EcoPackAI Team  
**Version:** 1.0.0

---

## 🎯 Features Implemented

### 1️⃣ Interactive Analytics Visualizations

**File:** `frontend/static/js/analytics.js`

Visualization capabilities using Chart.js:

- **CO₂ Emissions Comparison** - Bar chart showing carbon footprint across materials
- **Cost Comparison** - Bar chart analyzing predicted costs
- **Cost vs CO₂ Scatter Plot** - Relationship between cost and environmental impact
- **Sustainability Radar Chart** - Comprehensive view of sustainability metrics
- **Material Ranking** - Horizontal bar chart ranking materials by sustainability score

**Key Features:**
- Responsive charts that adapt to screen size
- Interactive tooltips with detailed information
- Color-coded visualizations (green for eco-friendly, red for high impact)
- Smooth animations and transitions
- Auto-resize on window resize events

**Usage Example:**
```javascript
// Initialize analytics manager
const analytics = window.AnalyticsManager;

// Create CO₂ comparison chart
analytics.createCO2ComparisonChart('chartCanvas', materialsData);

// Update chart with new data
analytics.updateChart('chartCanvas', newData);

// Clean up
analytics.destroyAll();
```

### 2️⃣ Export Functionality (CSV & PDF)

**Frontend:** `frontend/static/js/export.js`  
**Backend:** `backend/routes/export.py`

**Supported Export Formats:**

#### CSV Export
- Single prediction results
- Multiple materials comparison
- Complete data with metadata
- Excel-compatible formatting

#### PDF Export
- Client-side generation using jsPDF
- Server-side generation using ReportLab (optional)
- Formatted reports with branding
- Includes prediction results and model metadata

**Frontend Usage:**
```javascript
const exporter = window.ExportManager;

// Export to CSV
exporter.exportCurrentData('csv');

// Export to PDF
exporter.exportCurrentData('pdf');

// Export materials comparison
exporter.exportMaterialsComparison(materials, 'comparison.csv');
```

**Backend API Endpoints:**

```http
POST /api/v1/export/csv
Content-Type: application/json

{
  "export_type": "single",
  "prediction_data": { ... }
}
```

```http
POST /api/v1/export/pdf
Content-Type: application/json

{
  "prediction_data": { ... },
  "include_charts": true
}
```

```http
GET /api/v1/export/formats
```

### 3️⃣ End-to-End UI Testing

**Framework:** Playwright  
**Test Files:** `tests/e2e/test_ui_workflow.py`, `tests/e2e/conftest.py`

**Test Coverage:**

#### Functional Tests (14 tests)
1. ✅ Home page loads successfully
2. ✅ Navigation links work correctly
3. ✅ Form validation functionality
4. ✅ Prediction form submission
5. ✅ Results page display
6. ✅ CSV export button presence
7. ✅ PDF export button presence
8. ✅ API health check
9. ✅ API prediction endpoint
10. ✅ Responsive layout - mobile
11. ✅ Responsive layout - tablet
12. ✅ Dashboard page loads
13. ✅ Error handling
14. ✅ Chart library loaded

#### Analytics-Specific Tests (2 tests)
15. ✅ AnalyticsManager initialization
16. ✅ ExportManager initialization

**Running Tests:**

```bash
# Install Playwright browsers (first time only)
playwright install chromium

# Run all E2E tests
pytest tests/e2e/test_ui_workflow.py -v

# Run specific test
pytest tests/e2e/test_ui_workflow.py::TestEcoPackAIWorkflow::test_home_page_loads -v

# Run with verbose output
pytest tests/e2e/ -v -s

# Generate coverage report
pytest tests/e2e/ --cov=frontend --cov-report=html
```

---

## 🚀 Getting Started

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Install Playwright browsers:**
```bash
playwright install
```

3. **Install ReportLab (for server-side PDF generation):**
```bash
pip install reportlab
```

### Frontend Integration

Add these script tags to your HTML pages:

```html
<!-- Chart.js for visualizations -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>

<!-- jsPDF for client-side PDF generation -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>

<!-- EcoPackAI Analytics & Export -->
<script src="static/js/analytics.js"></script>
<script src="static/js/export.js"></script>
```

### Using the Analytics Page

Navigate to `/frontend/analytics.html` to view:
- Interactive charts displaying prediction data
- Key performance indicators (KPIs)
- Export options for CSV and PDF

**Data Source:**
The analytics page reads from `localStorage.analyticsData` for real data, or uses sample data for demonstration.

---

## 📁 File Structure

```
EcopackAI/
├── frontend/
│   ├── analytics.html              # NEW: Analytics dashboard page
│   ├── static/
│   │   └── js/
│   │       ├── analytics.js        # NEW: Chart visualization logic
│   │       └── export.js           # NEW: CSV/PDF export functionality
│   ├── predict.html
│   ├── results.html
│   └── index.html
├── backend/
│   └── routes/
│       ├── export.py               # NEW: Export API endpoints
│       ├── predict.py
│       └── health.py
├── tests/
│   └── e2e/
│       ├── __init__.py             # NEW: E2E package init
│       ├── conftest.py             # NEW: Playwright configuration
│       └── test_ui_workflow.py     # NEW: E2E test suite
└── requirements.txt                # UPDATED: Added Playwright & ReportLab
```

---

## 🎨 Analytics Page Features

### Key Performance Indicators
- Average Cost
- Average CO₂ Emissions
- Total Predictions
- Average Sustainability Score

### Interactive Charts

**CO₂ Emissions Comparison**
- Visual comparison of carbon footprint
- Color-coded by impact level
- Interactive tooltips

**Cost Analysis**
- Material cost predictions
- Side-by-side comparisons
- Confidence intervals

**Cost vs CO₂ Scatter Plot**
- Identify cost-effective, eco-friendly options
- Spot outliers and trends
- Interactive data points

**Sustainability Radar**
- Multi-dimensional sustainability view
- Shows 6 key metrics
- Single material analysis

### Export Options

**CSV Export Button**
```html
<button id="exportCSV" class="btn btn-primary">
  Export to CSV
</button>
```

**PDF Export Button**
```html
<button id="exportPDF" class="btn btn-secondary">
  Export to PDF
</button>
```

---

## 🧪 Testing Guide

### Test Scenarios Covered

#### 1. Navigation Flow
- Home → Predict → Results → Dashboard
- All navigation links functional
- Active state indicators

#### 2. Prediction Workflow
- Form validation
- Data submission
- API integration
- Results display

#### 3. Export Functionality
- CSV download
- PDF generation
- Data integrity

#### 4. Responsive Design
- Mobile (375x667)
- Tablet (768x1024)
- Desktop (1920x1080)

#### 5. API Integration
- Health check endpoint
- Prediction endpoints
- Error handling
- Response validation

### Writing New Tests

```python
def test_custom_feature(page: Page):
    """Test your custom feature"""
    page.goto(f"{BASE_URL}/frontend/your-page.html")
    
    # Your test logic
    element = page.locator("#yourElement")
    expect(element).to_be_visible()
    
    print("✓ Custom feature test passed")
```

---

## 📊 Analytics Data Format

### Material Data Structure

```json
{
  "name": "Recycled Cardboard",
  "predicted_cost": 12.45,
  "predicted_co2": 1.234,
  "cost_confidence": 0.95,
  "recyclability_percent": 95,
  "recycled_content_percent": 70,
  "reusability_percent": 50,
  "waste_reduction_impact_percent": 80,
  "sustainability_target_progress_percent": 85,
  "supplier_sustainability_compliance_percent": 90,
  "overall_sustainability_score": 0.85
}
```

### Storage Format (localStorage)

```javascript
localStorage.setItem('analyticsData', JSON.stringify([
  material1,
  material2,
  // ...
]));

localStorage.setItem('latestPrediction', JSON.stringify({
  timestamp: "2026-01-12T19:00:00",
  prediction_type: "all",
  results: { ... },
  metadata: { ... }
}));
```

---

## 🔧 Configuration

### Chart.js Configuration

Customize charts in `analytics.js`:

```javascript
const ChartConfig = {
  defaultColors: {
    primary: 'rgba(16, 185, 129, 0.8)',
    secondary: 'rgba(59, 130, 246, 0.8)',
    // ...
  },
  defaultOptions: {
    responsive: true,
    maintainAspectRatio: false,
    // ...
  }
};
```

### Export Settings

Configure in `export.js`:

```javascript
class ExportManager {
  constructor() {
    this.apiBase = '/api/v1';  // Change if needed
  }
  // ...
}
```

### Test Configuration

Configure in `tests/e2e/conftest.py`:

```python
BASE_URL = "http://localhost:5000"
TIMEOUT = 30000  # 30 seconds
```

---

## 🎯 Validation Checklist

Use this checklist to verify implementation:

### Analytics Visualization
- [ ] Charts render correctly with sample data
- [ ] Charts update dynamically with new data
- [ ] Tooltips display accurate information
- [ ] Charts are responsive across devices
- [ ] Color coding reflects data values appropriately
- [ ] Legends and labels are clear

### Export Functionality
- [ ] CSV export generates valid files
- [ ] CSV data matches on-screen data
- [ ] PDF export creates readable documents
- [ ] PDF includes all required sections
- [ ] Export buttons are accessible
- [ ] File naming is descriptive

### E2E Testing
- [ ] All 14 functional tests pass
- [ ] API integration tests succeed
- [ ] Responsive design tests pass
- [ ] Error handling works correctly
- [ ] Test coverage is comprehensive
- [ ] Tests are reproducible

---

## 📈 Performance Considerations

### Chart Rendering
- Limit data points to 50-100 for optimal performance
- Use chart destroy/update instead of recreating
- Debounce window resize events

### Export Operations
- Large datasets may cause browser lag
- Consider pagination for CSV exports > 10,000 rows
- PDF generation is CPU-intensive

### Testing
- Parallel test execution for faster runs
- Use headless mode in CI/CD
- Screenshot capture for failed tests

---

## 🐛 Troubleshooting

### Charts Not Displaying

**Issue:** Canvas element not found  
**Solution:** Ensure Chart.js is loaded before analytics.js

```html
<!-- Load Chart.js first -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<!-- Then load analytics -->
<script src="static/js/analytics.js"></script>
```

### Export Not Working

**Issue:** ExportManager undefined  
**Solution:** Check export.js is included

```html
<script src="static/js/export.js"></script>
```

**Issue:** PDF export fails  
**Solution:** Ensure jsPDF is loaded

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
```

### Tests Failing

**Issue:** Playwright not installed  
**Solution:** Install browsers

```bash
playwright install chromium
```

**Issue:** Connection refused  
**Solution:** Ensure app is running

```bash
python app.py
```

---

## 🚀 Next Steps

### Enhancements
1. Add more chart types (pie, doughnut, line)
2. Implement real-time data updates via WebSocket
3. Add chart download as image
4. Implement advanced filtering and sorting
5. Add comparison mode for multiple predictions

### Testing
1. Add visual regression tests
2. Implement performance benchmarks
3. Add load testing for API endpoints
4. Create integration test suite
5. Add accessibility (a11y) tests

### Documentation
1. Create API documentation with Swagger
2. Add interactive tutorials
3. Create video walkthroughs
4. Build developer onboarding guide

---

## 📞 Support

For questions or issues:
- Check documentation in `/docs`
- Review test files for usage examples
- Consult Chart.js documentation: https://www.chartjs.org/
- Playwright docs: https://playwright.dev/

---

## ✅ Validation Summary

**Module:** Analytics Visualization, Export & E2E Testing  
**Status:** ✅ Complete  
**Test Coverage:** 16/16 tests implemented  
**Files Created:** 7  
**Files Modified:** 2  

### Deliverables ✓
- ✅ Interactive analytics charts (analytics.js)
- ✅ CSV/PDF export handlers (export.js, export.py)
- ✅ E2E UI test scripts (test_ui_workflow.py)
- ✅ Analytics dashboard page (analytics.html)
- ✅ Test configuration (conftest.py)
- ✅ Comprehensive documentation

---

**Generated:** January 12, 2026  
**EcoPackAI Team**
