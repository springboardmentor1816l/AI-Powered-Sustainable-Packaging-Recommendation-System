# Material Ranking Logic – EcoPackAI

## Overview

The material ranking module is a core component of the EcoPackAI recommendation engine. Its purpose is to convert model predictions and engineered sustainability signals into **actionable, ordered packaging material recommendations** for each product.

Instead of presenting raw cost or CO₂ values, this module computes a **composite ranking score** that balances economic efficiency, environmental impact, and material suitability.

---

## Inputs

The ranking logic operates on an **integrated product–material dataset** that includes:

### 1. Product Attributes

* `product_weight`
* `fragility_score`
* `moisture_sensitivity`
* `thermal_sensitivity`
* `expected_shelf_life_days`

### 2. Material Attributes

* `material_cost_per_kg`
* `co2_emission_per_kg`
* `biodegradability_percent`
* `load_handling_score`
* `recyclability_category`

### 3. Engineered / Derived Features

* `co2_impact_index`
* `cost_efficiency_index`
* `sustainability_score`

### 4. Configuration

* Weight definitions (YAML-based)
* Business constraints (minimum thresholds)

---

## Ranking Criteria

Each material is evaluated using the following dimensions:

| Criterion      | Description                         | Optimization Goal |
| -------------- | ----------------------------------- | ----------------- |
| CO₂ Impact     | Environmental footprint of material | Minimize          |
| Cost           | Packaging cost per unit             | Minimize          |
| Sustainability | Composite sustainability score      | Maximize          |
| Recyclability  | Material recyclability category     | Maximize          |

---

## Normalization Strategy

Because all criteria are on different scales, **min–max normalization** is applied:

* For metrics where **lower is better** (CO₂, cost):

  `normalized = (max - value) / (max - min)`

* For metrics where **higher is better** (sustainability, recyclability):

  `normalized = (value - min) / (max - min)`

This ensures all normalized scores lie in the range **[0, 1]**.

---

## Composite Ranking Score

A weighted sum is used to compute the final ranking score:

```
final_score =
  (w_co2 × normalized_co2) +
  (w_cost × normalized_cost) +
  (w_sustainability × normalized_sustainability) +
  (w_recyclability × normalized_recyclability)
```

Where weights are loaded dynamically from:

```
config/ranking_weights.yaml
```

---

## Ranking Modes

The system supports multiple ranking strategies without changing code:

### 1. Balanced (Default)

Optimizes cost and sustainability equally.

### 2. Sustainability-First

Prioritizes CO₂ reduction and sustainability scores.

### 3. Cost-First

Favors economically efficient materials while respecting constraints.

Switching modes only requires updating the YAML configuration.

---

## Business Constraints

Before ranking, materials that violate business rules are **filtered out**:

* Minimum `load_handling_score`
* Minimum `biodegradability_percent`
* Maximum allowable `material_cost_per_kg`

This ensures only **feasible and compliant materials** are ranked.

---

## Output

The module produces a ranked list of materials **per product**, including:

* `product_id`
* `material_id`
* `rank`
* `final_score`
* Key cost and sustainability metrics

Output file:

```
outputs/material_rankings.csv
```

---

## Key Properties

* Deterministic and reproducible
* Configuration-driven (no hardcoded weights)
* Extensible to new criteria
* Compatible with ML inference pipelines

---

## Role in EcoPackAI Pipeline

This module bridges the gap between **prediction models** and **decision-making**, enabling:

1. ML-driven sustainability optimization
2. Transparent and explainable recommendations
3. Scalable deployment in APIs and dashboards

It represents the **decision intelligence layer** of EcoPackAI.
