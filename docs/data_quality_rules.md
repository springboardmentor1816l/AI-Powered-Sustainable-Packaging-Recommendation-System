\# Data Quality Rules – Materials Dataset



\## Mandatory Columns (No Nulls)

\- material\_id

\- material\_name

\- cost\_per\_kg

\- co2\_factor

\- recyclability\_percent

\- biodegradability\_percent

\- CEI

\- CII

\- MSS

\- Eco\_Grade



\## Allowed Null Columns

\- supplier\_notes

\- special\_handling



\## Value Range Rules

\- cost\_per\_kg > 0

\- co2\_factor ≥ 0

\- recyclability\_percent: 0–100

\- biodegradability\_percent: 0–100

\- CEI, CII, MSS: 0–100



\## Categorical Rules

\### Eco Grade

\- A

\- B

\- C

\- D



\## Integrity Rules

\- material\_id must be unique

\- No duplicate rows

\- No infinite or NaN values

