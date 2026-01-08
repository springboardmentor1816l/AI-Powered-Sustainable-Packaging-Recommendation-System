# EcoPackAI - Analytics Dashboard Documentation

## Overview

The Analytics Dashboard provides interactive visualizations and insights into packaging material recommendations, including cost analysis, CO₂ impact assessment, and sustainability scoring.

## Features

### 📊 Interactive Charts

#### 1. Cost Comparison Chart
- **Type**: Bar Chart
- **Purpose**: Compare predicted costs across different materials
- **Visualization**: Color gradient (green = lowest cost, red = highest cost)
- **Interaction**: Hover tooltips show exact cost values

#### 2. CO₂ Impact Comparison Chart
- **Type**: Bar Chart
- **Purpose**: Visualize carbon footprint of each material option
- **Visualization**: Color gradient (green = lowest emissions, red = highest emissions)
- **Interaction**: Hover tooltips show exact CO₂ values in kg

#### 3. Sustainability Ranking Chart
- **Type**: Horizontal Bar Chart
- **Purpose**: Display materials ranked by overall sustainability score
- **Visualization**: Color gradient (red = lower score, green = higher score)
- **Interaction**: Hover tooltips show scores out of 100

#### 4. Multi-Metric Comparison Chart
- **Type**: Line Chart
- **Purpose**: Compare all metrics (cost, CO₂, sustainability) on normalized scale
- **Visualization**: Three overlaid lines with different colors
- **Interaction**: Toggle visibility of individual metrics

### 📋 Summary Cards

Four key metric cards displayed at the top of the dashboard:

1. **Best Recommendation Card**
   - Shows top-ranked material
   - Displays its sustainability score
   - Gradient purple background

2. **Average Cost Card**
   - Shows mean cost across all materials
   - Number of materials analyzed
   - Gradient pink background

3. **Average CO₂ Impact Card**
   - Shows mean CO₂ emissions
   - Measured in kg CO₂ equivalent
   - Gradient blue background

4. **Average Sustainability Card**
   - Shows mean sustainability score
   - Scale of 0-100
   - Gradient green background

### 📥 Export Functionality

#### CSV Export
- **Format**: Comma-Separated Values
- **Contents**:
  - Product information header
  - Material recommendations table
  - Summary statistics
  - Timestamp of generation
- **Filename**: `EcoPackAI_Report_[timestamp].csv`
- **Use Case**: Data analysis in Excel/spreadsheet applications

#### PDF Export
- **Format**: Portable Document Format
- **Contents**:
  - Branded header with EcoPackAI logo
  - Product information summary
  - Material recommendations table
  - Summary statistics
  - Best recommendation highlight box
  - Timestamp footer
- **Filename**: `EcoPackAI_Report_[timestamp].pdf`
- **Use Case**: Sharing reports with stakeholders, printing

### 📈 Data Table

Detailed table showing all material recommendations:
- Rank (1 = best recommendation)
- Material name
- Predicted cost (₹)
- CO₂ impact (kg)
- Sustainability score (0-100)

**Styling**: First row (best recommendation) highlighted in green

---

## User Guide

### Accessing the Analytics Dashboard

1. **Generate a Prediction**:
   - Navigate to "Product Input" page
   - Fill in product details
   - Click "Get Recommendations"
   - View results

2. **View Analytics**:
   - Click "Analytics" in navigation menu
   - Dashboard automatically loads with your latest prediction data

### Understanding the Visualizations

#### Cost Analysis
- **Lower is better**: Materials with lower costs are more economical
- **Bar height**: Represents absolute cost in rupees
- **Color coding**: Green bars indicate cost-effective options

#### CO₂ Impact Analysis
- **Lower is better**: Materials with lower emissions are more sustainable
- **Bar height**: Represents CO₂ emissions in kilograms
- **Color coding**: Green bars indicate eco-friendly options

#### Sustainability Scoring
- **Higher is better**: Materials with higher scores are more sustainable overall
- **Score range**: 0-100 (higher = more sustainable)
- **Factors**: Combines cost, CO₂ impact, recyclability, and other metrics

### Exporting Reports

#### To Export as CSV:
1. Click the "📥 Export CSV" button
2. File automatically downloads to your Downloads folder
3. Open with Excel, Google Sheets, or any spreadsheet application

#### To Export as PDF:
1. Click the "📄 Export PDF" button
2. File automatically downloads to your Downloads folder
3. Open with any PDF reader (Adobe Acrobat, Chrome, etc.)

### Data Persistence

- **Storage**: Data stored in browser's localStorage
- **Persistence**: Data persists across page refreshes
- **Limitations**: Data cleared if browser cache is cleared
- **Privacy**: Data stored locally, not sent to servers

---

## Technical Implementation

### Technologies Used

- **Chart.js**: JavaScript library for interactive charts
- **jsPDF**: JavaScript library for PDF generation
- **jsPDF-AutoTable**: Plugin for table generation in PDFs
- **Vanilla JavaScript**: No framework dependencies

### Data Flow

```
Product Input Form
    ↓
Backend API (/predict)
    ↓
Results Page (localStorage)
    ↓
Analytics Dashboard
    ↓
Charts & Visualizations
    ↓
Export (CSV/PDF)
```

### Chart Configuration

#### Color Gradients
- Dynamically generated based on data values
- Smooth transitions between colors
- Automatically adjusts to data range

#### Responsive Design
- Charts resize based on screen width
- Mobile-optimized layouts
- Touch-friendly interactions

### localStorage Schema

```javascript
{
  "predictions": [
    {
      "rank": 1,
      "material": "Material Name",
      "predicted_cost": "XX.XX",
      "co2": "XX.XX",
      "sustainability_score": "XX.XX"
    },
    // ... more predictions
  ],
  "product_info": {
    "product_name": "Product Name",
    "category": "Category",
    "product_weight_kg": X.X,
    "fragility_index": 0.X,
    "shipping_type": "Type"
  }
}
```

---

## API Integration

### Data Source

Analytics dashboard consumes data from the `/predict` API endpoint:

**Endpoint**: `POST http://localhost:5000/predict`

**Request**:
```json
{
  "product_name": "string",
  "category": "string",
  "product_weight_kg": number,
  "fragility_index": number,
  "shipping_type": "string"
}
```

**Response**:
```json
{
  "predictions": [
    {
      "rank": number,
      "material": "string",
      "predicted_cost": "string",
      "co2": "string",
      "sustainability_score": "string"
    }
  ]
}
```

---

## Styling & Design

### Color Scheme

- **Primary Blue**: `#2c7be5` (Navigation, headers)
- **Success Green**: `#28a745` (Export buttons, highlights)
- **Gradient Cards**: Multiple gradients for visual appeal
- **Chart Colors**: Dynamic gradients based on values

### Responsive Breakpoints

- **Desktop**: > 1200px (2-column chart grid)
- **Tablet**: 768px - 1200px (1-column chart grid)
- **Mobile**: < 768px (Stacked layout)

### Accessibility

- High contrast ratios
- Clear hover states
- Keyboard navigation support
- Screen reader friendly labels

---

## Performance Optimization

### Chart Rendering
- Lazy loading of Chart.js library
- Efficient data transformation
- Minimal DOM manipulation

### Data Storage
- Efficient JSON serialization
- Minimal localStorage usage
- No unnecessary data duplication

### Export Performance
- Client-side generation (no server load)
- Efficient PDF rendering
- Optimized file sizes

---

## Browser Compatibility

### Supported Browsers

✅ **Chrome/Edge**: Version 90+
✅ **Firefox**: Version 88+
✅ **Safari**: Version 14+
✅ **Opera**: Version 76+

### Required Features

- ES6 JavaScript support
- localStorage API
- Canvas API (for charts)
- Blob API (for file downloads)

---

## Troubleshooting

### Issue: No Data Available

**Symptom**: Dashboard shows "No Data Available" message

**Causes**:
- No prediction has been generated yet
- localStorage was cleared
- Browser in private/incognito mode

**Solution**:
1. Navigate to Product Input page
2. Generate a new prediction
3. Return to Analytics dashboard

### Issue: Charts Not Displaying

**Symptom**: Chart areas are empty or show errors

**Causes**:
- Chart.js library failed to load
- Network connectivity issues
- Browser compatibility issues

**Solution**:
1. Check browser console for errors
2. Refresh the page
3. Ensure internet connection is stable
4. Try a different browser

### Issue: Export Buttons Disabled

**Symptom**: CSV/PDF export buttons are grayed out

**Causes**:
- No data available in localStorage
- Page loaded before data initialization

**Solution**:
1. Ensure a prediction has been generated
2. Refresh the analytics page
3. Check browser console for errors

### Issue: Export Files Not Downloading

**Symptom**: Click export button but no file downloads

**Causes**:
- Browser blocked download
- Pop-up blocker active
- Insufficient permissions

**Solution**:
1. Check browser's download settings
2. Allow downloads from the site
3. Check Downloads folder
4. Try different browser

---

## Future Enhancements

### Planned Features

1. **Historical Data Tracking**
   - Store multiple predictions
   - Compare predictions over time
   - Trend analysis charts

2. **Advanced Filters**
   - Filter by material type
   - Filter by cost range
   - Filter by sustainability threshold

3. **Comparison Mode**
   - Compare multiple products side-by-side
   - Differential analysis
   - Savings calculator

4. **Customizable Reports**
   - User-selectable metrics
   - Custom branding
   - Template options

5. **Data Sharing**
   - Share via email
   - Generate shareable links
   - Collaborative viewing

---

## Best Practices

### For Users

1. **Generate Fresh Predictions**: Update predictions when product details change
2. **Export Regularly**: Download reports for record-keeping
3. **Review All Metrics**: Consider cost, CO₂, and sustainability together
4. **Use Appropriate Format**: CSV for analysis, PDF for sharing

### For Developers

1. **Validate Data**: Always validate localStorage data before rendering
2. **Handle Errors**: Gracefully handle missing or malformed data
3. **Optimize Performance**: Debounce chart updates, lazy load libraries
4. **Test Thoroughly**: Test across browsers and devices
5. **Document Changes**: Update documentation when adding features

---

## Metrics & Analytics

### Key Performance Indicators

- **Page Load Time**: < 2 seconds
- **Chart Render Time**: < 1 second
- **Export Generation Time**: < 3 seconds
- **Mobile Responsiveness**: All devices supported

### Usage Statistics (Future)

- Number of predictions generated
- Most common product categories
- Average sustainability scores
- Export format preferences

---

## Support & Feedback

For questions, bug reports, or feature requests related to the Analytics Dashboard:

1. Review this documentation
2. Check the E2E Testing Guide
3. Inspect browser console for errors
4. Contact development team

---

## Change Log

### Version 1.0.0 (January 8, 2026)
- ✨ Initial release
- ✅ Four interactive chart types
- ✅ Summary cards with key metrics
- ✅ CSV export functionality
- ✅ PDF export functionality
- ✅ Detailed data table
- ✅ Responsive design
- ✅ Mobile optimization

---

**Last Updated**: January 8, 2026
**Version**: 1.0.0
