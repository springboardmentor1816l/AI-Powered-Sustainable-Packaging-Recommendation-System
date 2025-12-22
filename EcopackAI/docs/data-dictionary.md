# EcoPackAI Data Dictionary

## Materials Table
- material_id (INT): Unique material identifier
- material_type (VARCHAR): Type of packaging material
- strength_mpa (FLOAT): Material strength
- biodegradability_percent (FLOAT): Biodegradability score
- recyclability_percent (FLOAT): Recycling potential
- cost_per_kg (FLOAT): Material cost
- industry_use_case (VARCHAR): Applicable industries

## Products Table
- product_id (INT): Unique product ID
- product_name (VARCHAR): Product name
- category (VARCHAR): Product category
- product_weight (FLOAT): Weight of product
- fragility_index (INT): Handling requirement
- shipping_type (VARCHAR): Shipping method

## Recommendation Logs
- rec_id (INT): Recommendation ID
- material_rank (INT): Rank of suggested material
- created_at (TIMESTAMP): Time of prediction

## Task Scopes:

1️⃣ Identify all dataset sources required

What I did:

I identified two main datasets required for the EcoPackAI system:

a) Eco-friendly Packaging Materials Dataset

This dataset is required to understand material properties for AI recommendations.

It includes:

Material type (paper, PLA, cardboard, bioplastic, etc.)

Mechanical strength

Weight capacity

Biodegradability percentage

CO₂ emission score

Recyclability percentage

Cost per kg

Industry use cases

📌 Why needed?
These features are used by the ML model to:

Predict sustainability

Compare materials

Rank best packaging options

b) Product Attributes Dataset

This dataset describes products that need packaging.

It includes:

Product name and category

Product weight

Fragility index

Shipping type (Air/Road/Sea)

📌 Why needed?
Product attributes help the AI decide:

Which material is suitable

Strength & protection required

Cost vs sustainability trade-off

2️⃣ Define relational database structure in PostgreSQL

What I did:

I designed a relational database with clear table relationships using PostgreSQL.

Tables designed:

materials → stores packaging materials

products → stores product details

recommendation_logs → stores AI prediction results

📌 Why relational design?

Avoids data duplication

Supports ML training and inference

Enables dashboard analytics (history, trends)

3️⃣ Create schema.sql file

What I did:

I created a file:

backend/db/schema.sql

This file contains:

CREATE TABLE statements

Primary keys

Foreign key relationships

Correct data types (INT, FLOAT, VARCHAR, TIMESTAMP)

📌 Purpose of schema.sql:

Single source of truth for database

Easy to deploy in any environment

Supports scalability and automation

4️⃣ Prepare Data Dictionary

What I did:

I created:

docs/data_dictionary.md

This file explains:

Column name

Table name

Data type

Accepted values

Business meaning of each column

📌 Why data dictionary is important?

Helps ML engineers understand features

Helps dashboard developers understand data

Improves team collaboration and clarity

5️⃣ Validate design for ML & Dashboard requirements

Validation for ML:

Numeric columns (FLOAT, INT) → suitable for ML models

Clear separation of features and targets

Historical predictions stored in recommendation_logs

Validation for Dashboard:

CO₂ prediction and cost available for charts

Time-based logging (created_at)

Product-material relationships supported

📌 Result:
The database design supports:

ML model training

Real-time inference

BI dashboards and reporting