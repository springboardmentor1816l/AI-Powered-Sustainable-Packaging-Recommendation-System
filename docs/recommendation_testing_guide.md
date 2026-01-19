# Quick Testing Guide - Recommendations Integration

**Quick setup and testing for the frontend-backend recommendation integration**

---

## 🚀 5-Minute Quick Start

### Step 1: Start Backend (Terminal 1)

```bash
cd d:\EcopackAI
python app.py
```

**Expected Output:**
```
✓ Database initialized
✓ Caching initialized
✓ CORS enabled
✓ ML models loaded successfully
✓ Routes registered
 * Running on http://127.0.0.1:5000
```

### Step 2: Start Frontend (Terminal 2)

```bash
cd d:\EcopackAI\frontend
python -m http.server 8000
```

**Expected Output:**
```
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

### Step 3: Open Browser

Navigate to: **http://localhost:8000/predict.html**

---

## ✅ Quick Tests

### Test 1: Load Sample Data (10 seconds)

1. Press **F12** (open console)
2. Type: `loadSampleData()`
3. Press **Enter**
4. See: "📋 Sample data loaded"
5. Scroll down to verify all 18 fields are filled

✅ **PASS:** All fields populated with test data

---

### Test 2: Get Predictions (15 seconds)

1. Click **"Get Prediction"** button
2. Wait for loading spinner
3. See prediction results appear:
   - Cost: ~$12.45
   - CO₂: ~1.234 kg
   - Model info table

✅ **PASS:** Prediction results displayed

---

### Test 3: View Recommendations (Auto)

**Should happen automatically after Test 2:**

1. Recommendations table appears below results
2. See 5 materials ranked
3. Verify table columns:
   - Rank (1-5 with badges)
   - Material Name
   - Cost
   - CO₂
   - Sustainability (progress bar)
   - Ranking Score
   - Details button

✅ **PASS:** Recommendations table rendered with 5 materials

**Visual Check:**
- Rank #1 has **gold badge** 🥇
- Rank #2 has **silver badge** 🥈
- Rank #3 has **bronze badge** 🥉

---

### Test 4: View Material Details (20 seconds)

1. Click **"View"** button on any recommendation
2. Modal pops up showing:
   - Material name in header
   - 4 metric cards
   - Additional characteristics
   - Explanation text
3. Click **X** or "Close" to dismiss

✅ **PASS:** Modal opens and closes correctly

---

### Test 5: Compare Top 3 (15 seconds)

1. Click **"Compare Top 3"** button
2. Comparison modal opens
3. See 3 cards side by side
4. Each card shows:
   - Rank badge
   - Material name
   - All metrics
5. Click "Close"

✅ **PASS:** Comparison view works

---

### Test 6: Change Ranking Mode (20 seconds)

1. Locate **"Ranking Mode"** dropdown (top right of recommendations)
2. Change from "Balanced" to **"Cost Focused"**
3. Click **refresh icon** button next to dropdown
4. Watch table update
5. Notice different ranking order

✅ **PASS:** Ranking mode changes affect order

**Try all 3 modes:**
- Balanced
- Cost Focused (lowest cost first)
- Eco Focused (highest sustainability first)

---

### Test 7: Export CSV (10 seconds)

1. Click **"Export CSV"** button
2. File downloads automatically
3. Open CSV file
4. Verify contains:
   - Headers
   - All 5 recommendations
   - All metrics

✅ **PASS:** CSV export works

**File name format:** `ecopackai_recommendations_[timestamp].csv`

---

## 🧪 Advanced Tests

### Test 8: Form Validation (30 seconds)

1. Click **"Reset Form"** button
2. Leave all fields empty
3. Click **"Get Prediction"**
4. See error alert
5. See red borders on empty fields
6. Click on first red field
7. Verify scroll and focus

✅ **PASS:** Validation prevents empty submission

---

### Test 9: Invalid Values (30 seconds)

1. Load sample data
2. Change **Recyclability** to `150` (invalid, max is 100)
3. Click **"Get Prediction"**
4. See error: "Value must not exceed 100"
5. Fix to `95`
6. Submit successfully

✅ **PASS:** Range validation works

---

### Test 10: Backend Offline (30 seconds)

1. **Stop backend** (Ctrl+C in Terminal 1)
2. Reload page
3. See warning: "⚠️ Could not connect to API"
4. Try to submit form
5. See error about connection
6. **Restart backend**
7. Reload page
8. See success: "✅ API is healthy"

✅ **PASS:** Error handling for offline backend

---

## 🎯 Expected Behavior Summary

### After Successful Prediction

**You should see (in order):**

1. ✅ Success alert: "Prediction completed"
2. ✅ Results card with cost and CO₂
3. ✅ Success alert: "Recommendations generated"
4. ✅ Recommendations card appears
5. ✅ Table with 5 ranked materials
6. ✅ Smooth scroll to recommendations

### Recommendations Table Structure

```
┌────┬─────────────────────┬──────────┬──────────┬────────────────┬──────────┬─────────┐
│Rank│ Material            │ Cost ($) │ CO₂ (kg) │ Sustainability │  Score   │ Details │
├────┼────────────────────┼──────────┼──────────┼────────────────┼──────────┼─────────┤
│ 🥇 │ Recycled Cardboard  │  $9.96   │  0.864   │ ████████░░ 102%│   92%    │ [View]  │
│ 🥈 │ Molded Fiber        │ $11.12   │  0.987   │ ████████░░  98%│   88%    │ [View]  │
│ 🥉 │ Recycled Paper Pulp │  $8.66   │  0.741   │ █████████░ 110%│   85%    │ [View]  │
│  4 │ Wheat Straw Fiber   │ $11.76   │  0.926   │ ████████░░ 106%│   82%    │ [View]  │
│  5 │ Cornstarch Foam     │ $13.64   │  1.049   │ ████████░░ 102%│   78%    │ [View]  │
└────┴─────────────────────┴──────────┴──────────┴────────────────┴──────────┴─────────┘
```

---

## 🔍 Visual Inspection Checklist

### Navigation Bar
- [ ] Logo visible: "🌿 EcoPackAI"
- [ ] All 4 links work: Home, Predict, Results, Dashboard
- [ ] "Predict" link is highlighted/active

### Form Section
- [ ] 18 input fields visible
- [ ] Organized in 5 sections with icons
- [ ] Help text under each label
- [ ] "Reset Form" and "Get Prediction" buttons at bottom

### Results Section (after submission)
- [ ] Cost metric card with green border
- [ ] CO₂ metric card with blue border
- [ ] Model information table
- [ ] "Save Results" and "New Prediction" buttons

### Recommendations Section
- [ ] Card header with title and mode selector
- [ ] Action buttons: "Compare Top 3", "Export CSV"
- [ ] Stats showing recommendation count
- [ ] Dynamic table with 5 rows
- [ ] Rank badges colored (gold, silver, bronze)
- [ ] Progress bars for sustainability
- [ ] "View" buttons in last column

---

## ⚡ Performance Checks

### Response Times (should be fast)

| Operation | Expected | Check |
|-----------|----------|-------|
| Page Load | < 1 second | ⏱️ |
| Form Validation | Instant | ⏱️ |
| Prediction API | < 2 seconds | ⏱️ |
| Recommendations API | < 3 seconds | ⏱️ |
| Table Render | Instant | ⏱️ |
| Modal Open | Instant | ⏱️ |

**If any operation takes > 5 seconds, there may be an issue.**

---

## 🐛 Common Issues & Fixes

### Issue 1: "Could not connect to API"

**Cause:** Backend not running

**Fix:**
```bash
cd d:\EcopackAI
python app.py
```

---

### Issue 2: "Recommendations module not loaded"

**Cause:** JavaScript file not loaded

**Fix:** Hard refresh page (Ctrl + Shift + R)

---

### Issue 3: Table doesn't appear

**Cause:** API error or validation failure

**Fix:** 
1. Check browser console (F12) for errors
2. Verify all 18 fields have valid values
3. Check backend terminal for error messages

---

### Issue 4: Rank badges not colored

**Cause:** CSS not loaded

**Fix:** 
1. Verify `recommendations.css` loads in Network tab
2. Hard refresh page

---

### Issue 5: Modal doesn't open

**Cause:** JavaScript error

**Fix:**
1. Check console for errors
2. Verify `window.currentRecommendations` is set
3. Reload page and try again

---

## 📊 API Testing (Optional)

### Test Recommendation Endpoint Directly

**Using curl:**
```bash
curl -X POST http://localhost:5000/api/v1/recommend \
  -H "Content-Type: application/json" \
  -d "{\"product_data\": {\"recyclability_percent\": 95, \"recycled_content_percent\": 70, \"reusability_percent\": 50, \"biodegradation_time_days\": 120, \"end_of_life_disposal_percent\": 95, \"carbon_footprint_kg_co2_unit\": 1.8, \"waste_reduction_impact_percent\": 80, \"sustainability_target_progress_percent\": 85, \"load_handling_score\": 8, \"moisture_resistance_score\": 7, \"thermal_resistance_score\": 7, \"annual_usage_units\": 15000, \"total_material_weight_tons\": 7.5, \"supplier_sustainability_compliance_percent\": 90, \"co2_impact_index\": 0.25, \"cost_efficiency_index\": 0.75, \"material_suitability_score\": 70, \"overall_sustainability_score\": 0.85}, \"ranking_mode\": \"balanced\", \"top_n\": 5}"
```

**Expected:** JSON response with 5 recommendations

---

### Test Modes Endpoint

```bash
curl http://localhost:5000/api/v1/recommend/modes
```

**Expected:** JSON with 3 ranking modes

---

### Test Health Endpoint

```bash
curl http://localhost:5000/api/v1/recommend/health
```

**Expected:** `{"status": "healthy", ...}`

---

## ✅ Acceptance Criteria

**All must pass for integration to be considered complete:**

- [ ] ✅ Frontend sends product input to `/predict`
- [ ] ✅ Backend returns ranked recommendation data
- [ ] ✅ Table updates dynamically without page reload
- [ ] ✅ API failures handled with user feedback
- [ ] ✅ Data displayed matches backend predictions
- [ ] ✅ Top 3 materials visually highlighted
- [ ] ✅ Detail modal shows complete information
- [ ] ✅ Ranking mode selector changes results
- [ ] ✅ Comparison view works for top materials
- [ ] ✅ CSV export downloads correctly
- [ ] ✅ Responsive design works on different screens
- [ ] ✅ Error messages are clear and helpful

---

## 🎉 Success!

**If all tests pass, the integration is working correctly!**

**You now have:**
- ✅ Fully functional prediction interface
- ✅ Dynamic recommendation table
- ✅ Multiple ranking strategies
- ✅ Interactive material exploration
- ✅ Export capabilities
- ✅ Comprehensive error handling

---

## 📞 Need Help?

### Check Documentation
- `docs/frontend_backend_integration.md` - Complete integration guide
- `docs/integration_task_summary.md` - Task summary
- `docs/FLASK_API_SUMMARY.md` - API reference

### Debug Steps
1. Check browser console (F12) for JavaScript errors
2. Check backend terminal for Python errors
3. Verify both servers are running
4. Try hard refresh (Ctrl + Shift + R)
5. Test with sample data first

---

**Happy Testing!** 🧪✨

**Last Updated:** January 7, 2026
