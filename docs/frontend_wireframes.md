# EcoPackAI Frontend Wireframes & UI Design

**Date:** January 7, 2026  
**Module:** Frontend UI – User Interaction & Validation Layer  
**Status:** ✅ COMPLETE

---

## 📋 Overview

This document outlines the wireframes, user interface design, and navigation flow for the EcoPackAI application. The design follows modern web design principles with a focus on usability, accessibility, and visual excellence.

---

## 🎨 Design System

### Color Palette
- **Primary Green:** `#10b981` - Represents sustainability and eco-friendliness
- **Secondary Blue:** `#3b82f6` - Technology and innovation
- **Gradients:** Linear gradients combining green and blue for premium feel
- **Neutral Grays:** Range from `#f9fafb` to `#111827` for proper contrast

### Typography
- **Font Family:** Inter (Google Fonts) - Modern, readable, professional
- **Headings:** 700-800 weight, tight letter-spacing
- **Body:** 400 weight, 1.6 line-height for readability

### Spacing & Layout
- **Container Max Width:** 1200px (1400px for dashboard)
- **Grid System:** CSS Grid with auto-fit/minmax for responsiveness
- **Spacing Scale:** 0.5rem to 3rem following consistent rhythm

### Visual Effects
- **Shadows:** Multi-level shadow system (sm, md, lg, xl)
- **Border Radius:** Consistent rounded corners (0.375rem to 1rem)
- **Animations:** Smooth transitions (150ms-350ms) and micro-interactions
- **Glassmorphism:** Navbar with backdrop-filter blur

---

## 📱 Wireframes

### 1. Home / Overview Page (`index.html`)

**Purpose:** Landing page showcasing EcoPackAI capabilities and features

#### Layout Structure
```
┌─────────────────────────────────────┐
│          NAVIGATION BAR              │
├─────────────────────────────────────┤
│                                     │
│         HERO SECTION                │
│   - Title & Tagline                 │
│   - CTA Buttons                     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│      FEATURES SECTION (3 cols)      │
│   [Cost]  [CO2]  [Speed]           │
│                                     │
├─────────────────────────────────────┤
│                                     │
│       STATS SECTION (4 metrics)     │
│   [99.7%] [99.4%] [18] [<200ms]   │
│                                     │
├─────────────────────────────────────┤
│                                     │
│     HOW IT WORKS (3 steps)          │
│   [Input] [Analysis] [Results]     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│         CTA SECTION                 │
│                                     │
├─────────────────────────────────────┤
│                                     │
│      API ENDPOINTS LIST             │
│                                     │
├─────────────────────────────────────┤
│            FOOTER                    │
└─────────────────────────────────────┘
```

#### Key Components
- **Hero:** Gradient background with pattern overlay, white text
- **Feature Cards:** Hover effect with lift animation
- **Stats:** Gradient text with numbered metrics
- **CTA:** Prominent button leading to prediction page

---

### 2. Product Input Page (`predict.html`)

**Purpose:** Main interaction page for entering material specifications

#### Layout Structure
```
┌─────────────────────────────────────┐
│          NAVIGATION BAR              │
├─────────────────────────────────────┤
│         PAGE HEADER                  │
├─────────────────────────────────────┤
│                                     │
│       ALERT CONTAINER               │
│                                     │
├─────────────────────────────────────┤
│                                     │
│    MATERIAL SPECIFICATIONS CARD     │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ ♻️ Sustainability Metrics     │ │
│  │  [Field] [Field] [Field]      │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 🌍 Environmental Impact       │ │
│  │  [Field] [Field] [Field]      │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 📦 Material Properties        │ │
│  │  [Field] [Field] [Field]      │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 📊 Usage & Supply Chain       │ │
│  │  [Field] [Field] [Field]      │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 🎯 Composite Scores           │ │
│  │  [Field] [Field] [Field]      │ │
│  └───────────────────────────────┘ │
│                                     │
│     [Reset]  [Get Prediction]      │
│                                     │
├─────────────────────────────────────┤
│                                     │
│      RESULTS CONTAINER              │
│   (Hidden until prediction made)    │
│                                     │
│   ┌─────────────┬──────────────┐  │
│   │  Cost Card  │  CO2 Card    │  │
│   └─────────────┴──────────────┘  │
│                                     │
│   Model Information Table          │
│                                     │
│   [Save Results] [New Prediction]  │
│                                     │
├─────────────────────────────────────┤
│            FOOTER                    │
└─────────────────────────────────────┘
```

#### Form Sections (18 Fields Total)

**Section 1: Sustainability Metrics (6 fields)**
- Recyclability % (0-100)
- Recycled Content % (0-100)
- Reusability % (0-100)
- Biodegradation Time (0-3650 days)
- End of Life Disposal % (0-100)
- Waste Reduction Impact % (0-100)

**Section 2: Environmental Impact (3 fields)**
- Carbon Footprint (0-50 kg CO₂)
- Sustainability Target Progress % (0-100)
- CO₂ Impact Index (0-1)

**Section 3: Material Properties (3 fields)**
- Load Handling Score (1-10)
- Moisture Resistance Score (1-10)
- Thermal Resistance Score (1-10)

**Section 4: Usage & Supply Chain (3 fields)**
- Annual Usage Units (0+)
- Total Material Weight (tons)
- Supplier Sustainability Compliance % (0-100)

**Section 5: Composite Scores (3 fields)**
- Cost Efficiency Index (0-1)
- Material Suitability Score (0-100)
- Overall Sustainability Score (0-1)

#### Field Design
- **Input Type:** Number inputs with min/max constraints
- **Labels:** Bold with required asterisk, help text below
- **Input Groups:** Value input + unit label
- **Validation:** Real-time on blur, error states with red border
- **Feedback:** Invalid/valid feedback messages below each field

---

### 3. Recommendation Results Page (`results.html`)

**Purpose:** View historical predictions and compare materials

#### Layout Structure
```
┌─────────────────────────────────────┐
│          NAVIGATION BAR              │
├─────────────────────────────────────┤
│         PAGE HEADER                  │
├─────────────────────────────────────┤
│                                     │
│    RECENT PREDICTIONS CARD          │
│                                     │
│  Empty State OR                     │
│                                     │
│  ┌─────────────────────────────┐   │
│  │ Prediction #001             │   │
│  │ Date/Time                   │   │
│  │ [Cost Result] [CO2 Result]  │   │
│  └─────────────────────────────┘   │
│                                     │
├─────────────────────────────────────┤
│                                     │
│    COMPARISON TOOL CARD             │
│  (Placeholder for multi-select)     │
│                                     │
├─────────────────────────────────────┤
│                                     │
│       INSIGHTS GRID (3 cols)        │
│  [Cost]  [Environment]  [Model]    │
│                                     │
├─────────────────────────────────────┤
│            FOOTER                    │
└─────────────────────────────────────┘
```

#### Components
- **Empty State:** Icon + message + CTA when no data
- **Result Cards:** Clickable cards with cost/CO₂ summary
- **Comparison:** Multi-select interface (placeholder)
- **Insights:** Aggregated statistics from predictions

---

### 4. Analytics Dashboard (`dashboard.html`)

**Purpose:** Monitor predictions, trends, and system health

#### Layout Structure
```
┌─────────────────────────────────────┐
│          NAVIGATION BAR              │
├─────────────────────────────────────┤
│         PAGE HEADER                  │
├─────────────────────────────────────┤
│                                     │
│      KPI CARDS (4 metrics)          │
│  [Predictions] [Cost] [CO2] [Score] │
│                                     │
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────┬────────────────┐│
│  │ Trends Chart  │ Model Accuracy ││
│  │  (Large 2/3)  │   (Small 1/3)  ││
│  └───────────────┴────────────────┘│
│                                     │
├─────────────────────────────────────┤
│                                     │
│     CHARTS ROW 2 (3 equal cols)     │
│  [Cost Dist] [Impact] [Materials]  │
│                                     │
├─────────────────────────────────────┤
│                                     │
│       API STATUS CARD               │
│  [Health] [Predict] [Response Time] │
│                                     │
├─────────────────────────────────────┤
│            FOOTER                    │
└─────────────────────────────────────┘
```

#### Dashboard Elements
- **KPI Cards:** Gradient backgrounds with white text
- **Charts:** Placeholder divs ready for Chart.js/D3.js
- **Model Accuracy:** Progress bars showing 99.7% and 99.4%
- **API Status:** Real-time health indicators

---

## 🔄 User Flow

### Primary User Journey

```
┌─────────────┐
│  Land on    │
│  Homepage   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Read About │
│  Features   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Click "Get  │
│  Started"   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Navigate   │
│  to Predict │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Fill Input  │
│    Form     │
└──────┬──────┘
       │
       ▼
┌─────────────┐     NO     ┌──────────────┐
│  Validate?  ├───────────►│ Show Errors  │
└──────┬──────┘            └──────┬───────┘
       │ YES                      │
       │                          │
       │◄─────────────────────────┘
       ▼
┌─────────────┐
│   Submit    │
│   to API    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Display   │
│   Results   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Save/Export │
│    or New   │
└─────────────┘
```

### Navigation Flow

```
Home ←→ Predict ←→ Results ←→ Dashboard
 │        │          │           │
 └────────┴──────────┴───────────┘
       (Always accessible via navbar)
```

---

## 🖼️ Component Details

### Navigation Bar
- **Position:** Sticky top, always visible
- **Background:** White with blur, subtle shadow
- **Brand:** Gradient text with emoji icon
- **Links:** Hover underline animation
- **Active State:** Green underline for current page

### Cards
- **Base:** White background, rounded corners, shadow
- **Hover:** Lift effect (translateY -4px)
- **Header:** Title + subtitle with bottom border
- **Content:** Padded, structured content

### Buttons
- **Primary:** Gradient background, white text, icon + text
- **Secondary:** White with colored border
- **Hover:** Lift + shadow glow effect
- **Loading:** Spinner icon replaces text

### Form Fields
- **Label:** Bold, required asterisk, help text
- **Input:** Border, focus state with green ring
- **Validation:** Real-time, colored border (red/green)
- **Feedback:** Error/success message below field

### Alerts
- **Types:** Success, error, warning, info
- **Design:** Colored left border, light background
- **Animation:** Slide down entrance, fade out exit
- **Auto-dismiss:** Configurable timeout

### Metrics/Stats
- **Value:** Large, gradient text, bold font
- **Label:** Small, uppercase, muted color
- **Card:** Light gradient background, hover lift

---

## 📐 Responsive Design

### Breakpoints
- **Desktop:** > 1024px - Full multi-column layouts
- **Tablet:** 768px - 1024px - 2-column grids
- **Mobile:** < 768px - Single column stacks

### Responsive Adjustments
- **Grid:** `repeat(auto-fit, minmax(250px, 1fr))` for flex wrapping
- **Typography:** Reduced font sizes on mobile
- **Hero:** Smaller heading (3rem → 2rem)
- **Cards:** Reduced padding (2rem → 1.5rem)
- **Navigation:** Maintains horizontal layout (could add hamburger in v2)

---

## ♿ Accessibility Features

### Implemented
- ✅ Semantic HTML5 elements
- ✅ Proper heading hierarchy (h1 → h2 → h3)
- ✅ Alt text for decorative elements (empty alt)
- ✅ Color contrast meeting WCAG AA standards
- ✅ Focus states on interactive elements
- ✅ Keyboard navigation support
- ✅ Form labels properly associated with inputs
- ✅ Required field indicators

### Future Enhancements
- ⏭️ ARIA labels for complex interactions
- ⏭️ Screen reader announcements for dynamic content
- ⏭️ Skip navigation links
- ⏭️ High contrast mode

---

## 🎯 Design Principles Applied

### 1. Visual Hierarchy
- Clear distinction between primary and secondary actions
- Larger, bolder elements for important content
- Strategic use of color to draw attention

### 2. Consistency
- Reusable component system
- Consistent spacing and sizing
- Unified color and typography system

### 3. Feedback
- Loading states for async operations
- Success/error messages for user actions
- Real-time validation feedback

### 4. Simplicity
- Clean, uncluttered interfaces
- Grouped related fields
- Progressive disclosure (results shown after submission)

### 5. Delight
- Smooth animations and transitions
- Hover effects for interactivity
- Gradient accents for premium feel
- Micro-interactions (button ripples, card lifts)

---

## 📊 Wireframe Annotations

### Home Page Highlights
- **Hero CTA:** Primary action to "Get Started" prominently displayed
- **Features:** Icon + title + description format for scanability
- **Stats:** Eye-catching metrics to build trust
- **API List:** Technical details for developer audience

### Predict Page Highlights
- **Form Organization:** 5 logical sections with icons
- **Help Text:** Every field has usage guidance
- **Real-time Validation:** Immediate feedback prevents errors
- **Results Inline:** No page navigation required

### Results Page Highlights
- **Empty State:** Clear CTA when no data exists
- **Result Cards:** Clickable, scannable summaries
- **Comparison Tool:** Foundation for future feature

### Dashboard Highlights
- **KPI First:** Most important metrics at top
- **Chart Placeholders:** Ready for visualization libraries
- **API Health:** System status transparency

---

## 🎨 Visual Design References

### Color Psychology
- **Green:** Sustainability, eco-friendliness, growth
- **Blue:** Trust, technology, professionalism
- **Gradient:** Modern, premium, dynamic

### Typography Choices
- **Inter:** Geometric, modern, excellent readability
- **Weight Variation:** Creates hierarchy (300-800)
- **Letter Spacing:** Tighter for headings, normal for body

### Shadow Strategy
- **Elevation Levels:** sm (1px) → xl (25px)
- **Usage:** Cards at rest (md), hover (xl), navbar (md)
- **Glow:** Special effect for primary buttons

---

## 📱 Mobile Considerations

### Touch Targets
- Minimum 44x44px for buttons
- Adequate spacing between clickable elements
- Large, easy-to-tap form controls

### Mobile Optimizations
- Larger font sizes (min 16px to prevent zoom)
- Simplified navigation
- Stacked layouts for readability
- Reduced motion for performance

---

## 🔍 UI Pattern Library

All wireframes use these consistent patterns:

| Pattern | Usage | Examples |
|---------|-------|----------|
| Hero Section | Page headers | All pages |
| Card Container | Content grouping | Features, results, charts |
| Metric Display | Statistics | Homepage stats, dashboard KPIs |
| Form Group | Input collections | Prediction form sections |
| Button Group | Actions | Reset + Submit, Save + New |
| Empty State | No data scenarios | Results, dashboard |
| Alert Banner | User feedback | Validation errors, API status |
| Badge | Status indicators | API health, model types |

---

## ✅ Wireframe Validation

### Design Review Checklist
- [x] All pages have consistent navigation
- [x] Visual hierarchy is clear
- [x] Color palette is applied consistently
- [x] Typography scale is followed
- [x] Spacing rhythm is maintained
- [x] Interactive elements have hover states
- [x] Forms have proper validation feedback
- [x] Empty states are designed
- [x] Loading states are indicated
- [x] Mobile responsiveness considered

---

## 📦 Deliverables Summary

### Wireframe Documents
- ✅ This wireframe specification (markdown)
- ✅ High-fidelity HTML implementations
- ✅ Component pattern documentation

### Design Assets
- ✅ Complete CSS design system (`style.css`)
- ✅ Color tokens and variables
- ✅ Typography definitions
- ✅ Animation specifications

### Static Pages
- ✅ `index.html` - Home/Overview
- ✅ `predict.html` - Product Input Form
- ✅ `results.html` - Results Display
- ✅ `dashboard.html` - Analytics Dashboard

---

**Last Updated:** January 7, 2026  
**Design Version:** 1.0  
**Status:** ✅ Ready for Development
