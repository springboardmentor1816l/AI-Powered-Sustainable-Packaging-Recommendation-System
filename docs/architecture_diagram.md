# EcoPackAI - Analytics & Testing Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  index.html  │  │ product.html │  │analytics.html│          │
│  │   (Home)     │  │   (Input)    │  │  (Charts)    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│         └──────────────────┴──────────────────┘                  │
│                            │                                      │
│                    ┌───────▼────────┐                           │
│                    │  Navigation     │                           │
│                    │  (nav links)    │                           │
│                    └────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ User Actions
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FRONTEND LOGIC                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ predict.js   │  │ results.js   │  │ analytics.js │          │
│  │              │  │              │  │              │          │
│  │ - Form       │  │ - Display    │  │ - Chart.js   │          │
│  │   validation │  │   table      │  │ - Export CSV │          │
│  │ - API call   │  │ - Highlight  │  │ - Export PDF │          │
│  │ - Data store │  │   best       │  │ - Data viz   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
│         │                  │                  │                   │
│         └──────────────────┴──────────────────┘                  │
│                            │                                      │
│                    ┌───────▼────────┐                           │
│                    │  localStorage   │                           │
│                    │                 │                           │
│                    │  {predictions,  │                           │
│                    │   product_info} │                           │
│                    └────────────────┘                            │
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP POST
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                       BACKEND API                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    Flask Application                      │  │
│  │                       (app.py)                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                            │                                      │
│           ┌────────────────┼────────────────┐                   │
│           │                │                │                   │
│      ┌────▼────┐     ┌────▼────┐     ┌────▼────┐              │
│      │  CORS   │     │  Auth   │     │ Predict │              │
│      │Middleware│     │Middleware│     │  Route │              │
│      └─────────┘     └─────────┘     └────┬────┘              │
│                                            │                     │
│                                       ┌────▼────────┐           │
│                                       │  predict.py │           │
│                                       │             │           │
│                                       │ - Load ML   │           │
│                                       │ - Validate  │           │
│                                       │ - Predict   │           │
│                                       │ - Rank      │           │
│                                       └────┬────────┘           │
│                                            │                     │
│                        ┌───────────────────┼──────────────┐    │
│                        │                   │              │    │
│                   ┌────▼────┐        ┌────▼────┐    ┌────▼───┐│
│                   │RF Model │        │XGB Model│    │Ranking ││
│                   │ (Cost)  │        │ (CO2)   │    │Config  ││
│                   └─────────┘        └─────────┘    └────────┘│
└─────────────────────────────────────────────────────────────────┘
                            │
                            │ JSON Response
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA STORAGE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐               │
│  │ Materials  │  │   Models   │  │   Config   │               │
│  │   CSV      │  │   .joblib  │  │    YAML    │               │
│  └────────────┘  └────────────┘  └────────────┘               │
└─────────────────────────────────────────────────────────────────┘
```

## Analytics Dashboard Flow

```
User Visit analytics.html
         │
         ▼
┌────────────────────┐
│  Load analytics.js │
└────────┬───────────┘
         │
         ▼
┌────────────────────────┐
│ Check localStorage     │
│ for recommendationData │
└────────┬───────────────┘
         │
    ┌────┴────┐
    │         │
No Data    Has Data
    │         │
    ▼         ▼
┌───────┐  ┌──────────────────┐
│ Show  │  │ Render Dashboard │
│ "No   │  └────────┬─────────┘
│ Data" │           │
│Message│      ┌────┴──────────────────────┐
└───────┘      │                           │
               ▼                           ▼
     ┌─────────────────┐         ┌─────────────────┐
     │ Summary Cards   │         │ Interactive     │
     │                 │         │ Charts          │
     │ - Best Rec      │         │                 │
     │ - Avg Cost      │         │ - Cost Chart    │
     │ - Avg CO2       │         │ - CO2 Chart     │
     │ - Avg Sustain   │         │ - Ranking Chart │
     └─────────────────┘         │ - Combined Chart│
                                 └─────────────────┘
               │                           │
               └────────┬──────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  Data Table     │
               │                 │
               │ Rank | Material │
               │ Cost | CO2      │
               │ Score           │
               └────────┬────────┘
                        │
                   User Action
                        │
         ┌──────────────┴──────────────┐
         │                             │
         ▼                             ▼
┌────────────────┐            ┌────────────────┐
│  Export CSV    │            │  Export PDF    │
│                │            │                │
│ - Product info │            │ - Branded      │
│ - Predictions  │            │ - Formatted    │
│ - Statistics   │            │ - Tables       │
│ - Download     │            │ - Download     │
└────────────────┘            └────────────────┘
```

## E2E Testing Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      TEST EXECUTION                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│                    python run_e2e_tests.py                       │
│                              │                                    │
│                              ▼                                    │
│                    ┌──────────────────┐                         │
│                    │ Check Dependencies│                         │
│                    │ - pytest          │                         │
│                    │ - playwright      │                         │
│                    └────────┬──────────┘                         │
│                             │                                     │
│                             ▼                                     │
│                    ┌──────────────────┐                         │
│                    │ Check Servers    │                         │
│                    │ - Frontend :8080 │                         │
│                    │ - Backend  :5000 │                         │
│                    └────────┬──────────┘                         │
│                             │                                     │
│                             ▼                                     │
│                    ┌──────────────────┐                         │
│                    │  Run pytest      │                         │
│                    │  test_e2e_ui.py  │                         │
│                    └────────┬──────────┘                         │
└─────────────────────────────┼─────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│TestEcoPackAIWork-│ │  TestPerformance │ │   Test Fixtures  │
│      flow        │ │                  │ │                  │
│                  │ │  - Page Load     │ │  - Browser       │
│ - Home Load      │ │  - Chart Render  │ │  - Context       │
│ - Navigation     │ └──────────────────┘ │  - Page          │
│ - Form Validate  │                      │  - Screenshots   │
│ - Prediction     │                      │  - Downloads     │
│ - Analytics      │                      └──────────────────┘
│ - Export CSV     │
│ - Export PDF     │
│ - Error Handle   │
│ - Responsive     │
│ - Data Persist   │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│                    PLAYWRIGHT AUTOMATION                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Browser   │  │   Locate   │  │   Assert   │            │
│  │  Launch    │  │  Elements  │  │  Expects   │            │
│  └──────┬─────┘  └──────┬─────┘  └──────┬─────┘            │
│         │                │                │                   │
│         └────────────────┴────────────────┘                  │
│                          │                                    │
│                          ▼                                    │
│              ┌────────────────────┐                          │
│              │  Interact with UI  │                          │
│              │                    │                          │
│              │  - Click           │                          │
│              │  - Fill            │                          │
│              │  - Select          │                          │
│              │  - Wait            │                          │
│              │  - Screenshot      │                          │
│              └────────┬───────────┘                          │
│                       │                                       │
│                       ▼                                       │
│              ┌────────────────────┐                          │
│              │  Capture Results   │                          │
│              │  - Pass/Fail       │                          │
│              │  - Screenshots     │                          │
│              │  - Error Logs      │                          │
│              └────────┬───────────┘                          │
└──────────────────────┼────────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│                   TEST REPORTING                              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌───────────────────────────────────────────────┐          │
│  │          HTML Test Report                     │          │
│  │     (reports/e2e_test_report.html)            │          │
│  │                                                │          │
│  │  - Test Summary                                │          │
│  │  - Pass/Fail Count                             │          │
│  │  - Execution Time                              │          │
│  │  - Error Details                               │          │
│  │  - Screenshots (on failure)                    │          │
│  └───────────────────────────────────────────────┘          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow Diagram

```
┌──────────────┐
│     USER     │
└──────┬───────┘
       │
       │ 1. Fill Product Form
       ▼
┌──────────────────┐
│  product.html    │
│  predict.js      │
└──────┬───────────┘
       │
       │ 2. POST /predict
       ▼
┌──────────────────┐
│  Flask Backend   │
│  predict.py      │
└──────┬───────────┘
       │
       │ 3. ML Predictions
       ▼
┌──────────────────┐
│  JSON Response   │
│  {predictions:[]}│
└──────┬───────────┘
       │
       │ 4. Store + Product Info
       ▼
┌──────────────────┐
│  localStorage    │
│  browser storage │
└──────┬───────────┘
       │
       ├──────────────┬─────────────┐
       │              │             │
       │ 5a. Display  │ 5b. Render  │ 5c. Export
       ▼              ▼             ▼
┌──────────┐   ┌───────────┐  ┌────────────┐
│ results  │   │ analytics │  │ CSV / PDF  │
│ .html    │   │ .html     │  │ Download   │
└──────────┘   └───────────┘  └────────────┘
```

## Technology Stack

```
Frontend Layer
├── HTML5
│   ├── analytics.html (Charts & Export)
│   ├── product.html (Input Form)
│   └── results.html (Table Display)
├── CSS3
│   └── styles.css (Responsive Design)
└── JavaScript (ES6+)
    ├── analytics.js (Charts & Export Logic)
    ├── predict.js (API Integration)
    └── results.js (Display Logic)

External Libraries
├── Chart.js 4.4.0 (Visualization)
├── jsPDF 2.5.1 (PDF Generation)
└── jsPDF-AutoTable 3.5.31 (PDF Tables)

Backend Layer
├── Python 3.8+
├── Flask (Web Framework)
├── Scikit-learn (ML Models)
├── XGBoost (ML Models)
└── Pandas (Data Processing)

Testing Layer
├── Playwright 1.40.0 (Browser Automation)
├── Pytest 7.4.3 (Test Framework)
├── pytest-playwright (Integration)
└── pytest-html (Reporting)

Data Storage
├── localStorage (Browser)
├── CSV Files (Materials Data)
├── YAML (Configuration)
└── Joblib (Serialized Models)
```

## Deployment Architecture

```
Development Environment
┌─────────────────────────────────────────┐
│                                          │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │    │   Backend    │  │
│  │              │    │              │  │
│  │ Port: 8080   │◄──►│ Port: 5000   │  │
│  │ HTTP Server  │    │ Flask Dev    │  │
│  └──────────────┘    └──────────────┘  │
│                                          │
└─────────────────────────────────────────┘

Production Environment (Future)
┌─────────────────────────────────────────┐
│                                          │
│  ┌──────────────┐                       │
│  │     Nginx    │ (Reverse Proxy)       │
│  │   Port: 80   │                       │
│  └──────┬───────┘                       │
│         │                                │
│    ┌────┴─────┐                         │
│    │          │                          │
│    ▼          ▼                          │
│  ┌─────┐  ┌──────┐                     │
│  │Front│  │Backend│                     │
│  │ end │  │ API   │                     │
│  └─────┘  └───┬───┘                     │
│               │                          │
│               ▼                          │
│          ┌────────┐                     │
│          │Database│                     │
│          │(Future)│                     │
│          └────────┘                     │
└─────────────────────────────────────────┘
```

---

**Version**: 1.0.0  
**Last Updated**: January 8, 2026
