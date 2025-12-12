##  1. Structural Validation

All required columns were found in the dataset.

**Checks performed:**

* Presence of mandatory fields (Material ID, Recyclability %, Cost, Scores, etc.)
* No unexpected missing columns
* Dataset contains all encoded feature columns

**Result:** ✔ Passed

---

##  2. Cleanliness & Integrity Checks

These ensure that core dataset quality conditions are met.

**Checks performed:**

* No null values in mandatory fields
* No duplicate `Material ID`
* No duplicate rows

**Result:** ✔ Passed

---

##  3. Numeric Range Validation

All continuous numeric fields were validated for correctness.

**Checks performed:**

* No negative values in any numeric column
* Biodegradation time, cost, carbon data validated
* Material performance scores within allowed ranges (scaled 0–1)

**Result:** ✔ Passed

---

##  4. Categorical / One-Hot Encoding Consistency

All categorical encodings were checked for accuracy.

**Checks performed:**

* All one-hot encoded columns contain only 0s and 1s
* Exactly **one** Material Type selected per row
* Exactly **one** Recyclability Category selected
* Exactly **one** Supplier Region selected

**Result:** ✔ Passed

---

##  5. Engineered Feature Validation

This validates downstream ML-ready features.

**Checks performed:**

* CII, CEI, MSS, and recommendation scores (if present) checked for range 0–100
* Ensured no NaN, infinity, or invalid scores

**Result:** ✔ Passed

---

## 📈 Summary Table

| Category                   | Status   |
| -------------------------- | -------- |
| Structural Checks          | ✅ Passed |
| Null Value Checks          | ✅ Passed |
| Duplicate Checks           | ✅ Passed |
| Numeric Range Checks       | ✅ Passed |
| One-Hot Encoding Checks    | ✅ Passed |
| Feature Engineering Checks | ✅ Passed |

---