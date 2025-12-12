### **Step 1: Load Dataset**

* Convert categorical fields to uppercase
* Convert numeric fields to float

### **Step 2: Handle Missing Values**

* Biodegradation → median
* Recyclability → C
* Durability → 0.5

### **Step 3: Normalize Required Fields**

* CO₂
* biodegradation time
* cost
* load/moisture/thermal resistance values

### **Step 4: Map Categories**

* A/B/C/D → 1.00/0.75/0.50/0.25
* Material type → sustainability weight

### **Step 5: Compute Indexes**

* CO₂ Impact Index
* Cost Efficiency Index
* Material Suitability Score

### **Step 6: Add New Columns to Dataset**

* `cii`
* `cei`
* `mss`
* `recommendation_score` (optional)

---
