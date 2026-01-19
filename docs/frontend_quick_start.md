# EcoPackAI Frontend Quick Start Guide

**Quick setup and testing guide for the EcoPackAI frontend**

---

## 🚀 Quick Start (5 Minutes)

### Step 1: Start Backend API

```bash
cd d:\EcopackAI
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Running on http://localhost:5000
```

### Step 2: Serve Frontend

**Option A - Python HTTP Server:**
```bash
cd d:\EcopackAI\frontend
python -m http.server 8000
```

**Option B - VS Code Live Server:**
1. Open `d:\EcopackAI\frontend\index.html` in VS Code
2. Right-click → "Open with Live Server"

### Step 3: Open in Browser

Navigate to: `http://localhost:8000`

---

## 🧪 Testing the Application

### Test 1: Navigation
1. Click through all navigation links
2. Verify active page indicator updates
3. Check all pages load correctly

### Test 2: Form Validation
1. Go to **Predict** page
2. Leave all fields empty, click "Get Prediction"
3. ✅ Should show error alert
4. ✅ Should highlight invalid fields in red
5. ✅ Should scroll to first invalid field

### Test 3: Sample Data
1. On Predict page, open browser console (F12)
2. Type: `loadSampleData()`
3. ✅ Form should fill with valid data
4. Click "Get Prediction"
5. ✅ Should show loading state
6. ✅ Should display results

### Test 4: Manual Entry
1. Fill in all 18 fields with these values:

```
Recyclability: 95
Recycled Content: 70
Reusability: 50
Biodegradation Time: 120
End of Life Disposal: 95
Carbon Footprint: 1.8
Waste Reduction Impact: 80
Sustainability Target Progress: 85
Load Handling Score: 8
Moisture Resistance: 7
Thermal Resistance: 7
Annual Usage: 15000
Total Material Weight: 7.5
Supplier Sustainability: 90
CO2 Impact Index: 0.25
Cost Efficiency Index: 0.75
Material Suitability: 70
Overall Sustainability: 0.85
```

2. Click "Get Prediction"
3. ✅ Results should appear below form

---

## ✅ Validation Testing

### Test Invalid Inputs

**Negative Numbers:**
- Enter `-5` in Recyclability
- ✅ Should show "Value must be at least 0"

**Out of Range:**
- Enter `150` in any percentage field
- ✅ Should show "Value must not exceed 100"

**Non-Numeric:**
- Enter `abc` in any field
- ✅ Should show "Please enter a valid number"

**Decimals in Integer Fields:**
- Enter `15000.5` in Annual Usage
- ✅ Should show "Value must be a whole number"

---

## 📊 Expected Results

### Successful Prediction Shows:

1. **Cost Metric Card**
   - Predicted cost value (e.g., $12.45)
   - Confidence percentage (e.g., 85.0%)

2. **CO₂ Metric Card**
   - Predicted CO₂ value (e.g., 1.234 kg)
   - Model name (XGBoost)

3. **Model Information**
   - Cost Model: Random Forest
   - CO₂ Model: XGBoost
   - Cost R²: 0.997
   - CO₂ R²: 0.994

4. **Action Buttons**
   - Save Results (downloads JSON)
   - New Prediction (resets form)

---

## 🔧 Troubleshooting

### Problem: API Connection Error

**Symptom:** Warning alert about API not available

**Solution:**
1. Ensure backend is running: `python app.py`
2. Check backend is on port 5000
3. Verify `http://localhost:5000/health` returns JSON

### Problem: CORS Error

**Symptom:** Browser console shows CORS error

**Solution:**
- Backend already has CORS enabled
- Clear browser cache
- Try incognito/private window

### Problem: Form Doesn't Submit

**Symptom:** Button stays disabled or nothing happens

**Solution:**
1. Check browser console (F12) for errors
2. Ensure all 18 fields have values
3. Verify fields have green borders (valid)

### Problem: Results Don't Appear

**Symptom:** No results container after submission

**Solution:**
1. Check browser console for JavaScript errors
2. Verify API response in Network tab (F12)
3. Ensure response has `results` object

---

## 📁 File Locations

```
d:\EcopackAI\frontend\
├── index.html              # Start here
├── predict.html            # Main form
├── results.html            # History page
├── dashboard.html          # Analytics
└── static/
    ├── css/
    │   └── style.css       # All styles
    └── js/
        └── predict.js      # Validation logic
```

---

## 🎯 Quick Validation Checklist

Use this to verify everything works:

- [ ] Backend running on port 5000
- [ ] Frontend accessible on port 8000
- [ ] Home page loads with features
- [ ] Predict page shows form with 18 fields
- [ ] Results page shows empty state
- [ ] Dashboard shows placeholder charts
- [ ] Navigation links work
- [ ] Form validation shows errors
- [ ] Sample data loads successfully
- [ ] Prediction returns results
- [ ] Results display correctly
- [ ] Save Results downloads JSON
- [ ] Reset Form clears all fields

---

## 💡 Tips

1. **Use Sample Data:** Fastest way to test - just run `loadSampleData()` in console

2. **Monitor Console:** Keep browser DevTools open to catch any errors

3. **Check Network:** Use Network tab to see API requests/responses

4. **Test Validation:** Try invalid values to ensure validation works

5. **Mobile View:** Use DevTools responsive mode to test mobile layout

---

## 📞 Need Help?

1. **Check Documentation:**
   - `docs/frontend_wireframes.md`
   - `docs/frontend_validation_behavior.md`
   - `docs/frontend_implementation_summary.md`

2. **Verify Backend:**
   - Visit `http://localhost:5000/health`
   - Should return: `{"status": "healthy", ...}`

3. **Check Browser:**
   - Use modern browser (Chrome, Firefox, Edge, Safari)
   - Enable JavaScript
   - Clear cache if issues persist

---

**Ready to Start!** 🎉

Just run the backend, serve the frontend, and navigate to `http://localhost:8000`
