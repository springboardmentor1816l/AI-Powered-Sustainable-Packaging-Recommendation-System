# 🌱 EcoPackAI – AI-Powered Sustainable Packaging Recommendation System

EcoPackAI is an **AI-driven decision support system** that recommends the most **sustainable and cost-effective packaging materials** based on product characteristics such as **weight, fragility, shipping type, and industry category**.

The system is designed to help organizations **reduce environmental impact** while maintaining **product safety, durability, and cost efficiency**.

---

## 🚀 Key Features

- 🤖 AI-powered packaging material recommendation  
- 🥇 Rank-wise comparison of top packaging materials  
- 🌍 CO₂ footprint analysis  
- 💰 Cost estimation and comparison  
- ♻ Sustainability score (0–100 scale)  
- 📊 Business Intelligence (BI) analytics dashboard  
- 📈 Industry-wise sustainability insights  
- 📄 CSV and PDF export for reports  
- 🔍 Explainable and transparent scoring logic  

---

## 🧠 How EcoPackAI Works

1. **User Inputs Product Details**
   - Product category
   - Weight capacity
   - Fragility index
   - Shipping type

2. **AI-Based Evaluation**
   - Multiple packaging materials are evaluated
   - Cost, strength, recyclability, biodegradability, CO₂ impact, and fragility handling are analyzed

3. **Rank-Wise Recommendation**
   - Materials are scored on a sustainability scale (0–100)
   - Top 2–3 best-suited materials are ranked and returned

4. **Visualization and Analytics**
   - Ranked comparison table
   - Cost and sustainability charts
   - Industry-level BI dashboard using historical data

---

## 🧮 Sustainability Scoring Factors

Each packaging material is evaluated using a **weighted multi-factor model**:

| Factor | Description |
|------|------------|
| Cost Efficiency | Lower cost results in higher score |
| Strength Adequacy | Ability to safely support product weight |
| Recyclability | Percentage of recyclable material |
| Biodegradability | Percentage of biodegradable content |
| Fragility Handling | Suitability for fragile products |
| CO₂ Impact | Lower emissions produce higher score |

The final sustainability score is calculated on a **0–100 scale**, ensuring transparency and explainability.

---

## 🏗 System Architecture

Frontend (HTML, Bootstrap, Chart.js)
↓
Flask REST API
↓
Explainable AI Scoring Engine
↓
Material Ranking Logic
↓
LocalStorage / PostgreSQL (design-ready)
↓
BI Analytics Dashboard

yaml
Copy code

### Architecture Highlights
- Predictor scores **one material at a time**
- Ranking handled at the **API layer**
- Frontend dynamically adapts to ranked results
- Clean separation of concerns

---

## 🖥 Technology Stack

### Frontend
- HTML5  
- CSS3  
- Bootstrap 5  
- JavaScript (Vanilla)  
- Chart.js  

### Backend
- Python  
- Flask  
- REST APIs  

### AI / Data
- Explainable scoring model  
- Pandas  
- NumPy  
- Joblib  

### Database & Analytics
- PostgreSQL (future-ready)  
- Browser LocalStorage (analytics aggregation)

---

## 📊 Analytics Dashboard

The Industry Analytics dashboard provides:

- Total number of predictions  
- Industry-wise usage distribution  
- Average sustainability score  
- Average cost and CO₂ impact  
- Exportable CSV analytics reports  

This enables **business intelligence–driven sustainability reporting**.

---

## 📁 Project Structure

EcoPackAI/
│
├── backend/
│ ├── app.py
│ ├── routes/
│ │ └── predict.py
│ ├── inference/
│ │ └── predictor.py
│ └── models/
│
├── frontend/
│ ├── index.html
│ ├── predict.html
│ ├── results.html
│ ├── analytics.html
│ └── js/
│
├── README.md
└── requirements.txt

yaml
Copy code

---

## ▶️ How to Run the Project

### 1️⃣ Backend Setup
```bash
pip install -r requirements.txt
python app.py
Backend runs on:

cpp
Copy code
http://127.0.0.1:5001
2️⃣ Frontend
Open the frontend directly in a browser:

bash
Copy code
frontend/index.html
🧪 Example Use Case
Product: Washing Machine
Category: Electronics
Weight: 15 kg
Fragility: Low
Shipping: Local

Output:

Rank 1: Corrugated Cardboard (Heavy Duty)

Rank 2: Styrofoam (EPS)

Ranked comparison table and charts

Exportable sustainability report

🎓 Academic & Evaluation Alignment
EcoPackAI satisfies key academic and project evaluation criteria:

AI-based decision making

Data preprocessing and feature engineering

Backend–frontend integration

Sustainability analytics and BI dashboard

Explainable scoring logic

Professional documentation

🔮 Future Enhancements
Full PostgreSQL integration

Lifecycle Assessment (LCA) modeling

User authentication and role-based dashboards

Cloud deployment (AWS / Render / Heroku)

Advanced explainability visualizations

👤 Author
Ravikant Raj
AI-Powered Sustainable Systems Project
2026

📜 License
This project is developed for academic and learning purposes.
Free to extend with proper attribution.

✅ Final Note
EcoPackAI is a decision-grade, explainable AI system designed to support
sustainable engineering and responsible packaging decisions.