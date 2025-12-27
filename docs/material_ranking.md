# Material Ranking Logic – EcoPackAI

## 📌 Module
Recommendation Engine – Material Ranking

## 🎯 Objective
The purpose of the material ranking module is to evaluate and order candidate packaging materials for each product based on predicted cost, predicted CO₂ emissions, and material suitability.  
This enables EcoPackAI to recommend the most optimal and sustainable packaging options in a transparent and configurable manner.

---

## 🧠 Problem Context
After training predictive models for:
- **Cost per unit prediction**
- **CO₂ emission prediction**

the system must convert raw predictions into actionable recommendations.  
Raw predictions alone are insufficient — materials must be **ranked** according to sustainability goals, cost efficiency, and product compatibility.

---

## 🧪 Inputs
The ranking module operates on an **integrated product–material dataset** that includes:

### Model Predictions
- Predicted cost per unit
- Predicted CO₂ emission per unit

### Engineered Features
- Material suitability score
- Load handling score
- Moisture resistance score
- Thermal resistance score
- Supplier sustainability compliance

### Optional Business Constraints
- Minimum recyclability threshold
- Maximum cost ceiling
- Minimum load / protection requirements

---

## ⚙️ Ranking Strategy

### Ranking Criteria
Each material is evaluated using the following dimensions:

| Criterion | Optimization Direction |
|--------|-------------------------|
| Predicted CO₂ Emission | Lower is better |
| Predicted Cost | Lower is better |
| Material Suitability Score | Higher is better |
| Sustainability Compliance | Higher is better |

---

## 🔢 Normalization
Since metrics exist on different scales, normalization is applied before scoring:

- Cost and CO₂ are **min–max normalized** and inverted
- Suitability and sustainability scores are normalized directly

This ensures all criteria contribute fairly to the final score.

---

## 🧮 Composite Ranking Score
A weighted composite score is computed:

