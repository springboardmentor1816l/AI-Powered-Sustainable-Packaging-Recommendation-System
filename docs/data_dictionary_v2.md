\# Materials Dataset – Data Dictionary v2



\## Dataset Summary

\- Purpose: ML-ready sustainability recommendation system

\- Format: Parquet

\- Status: Production Ready



\## Columns



| Column | Type | Description | Range | Used in ML |

|------|------|-------------|-------|------------|

| material\_id | int | Unique material ID | >0 | Yes |

| cost\_per\_kg | float | Cost per kg | >0 | Yes |

| co2\_factor | float | CO₂ emissions per kg | ≥0 | Yes |

| recyclability\_percent | float | Recyclability score | 0–100 | Yes |

| biodegradability\_percent | float | Biodegradability score | 0–100 | Yes |

| CEI | float | Carbon Efficiency Index | 0–100 | Yes |

| CII | float | Cost Impact Index | 0–100 | Yes |

| MSS | float | Material Sustainability Score | 0–100 | Yes |

| Eco\_Grade | category | Sustainability grade | A–D | Yes |



