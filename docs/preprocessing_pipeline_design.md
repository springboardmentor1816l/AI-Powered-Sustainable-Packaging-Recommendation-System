# Preprocessing Pipeline Design

This document explains the design decisions behind the EcoPackAI preprocessing pipeline.

The pipeline is built using `sklearn.pipeline.Pipeline` and `ColumnTransformer` to ensure reproducibility, consistency, and deployment safety.

---

## 🎯 Design Goals

- Ensure identical preprocessing during training and inference
- Prevent feature leakage and manual errors
- Support production deployment (FastAPI, batch inference)
- Enable modular ML development

---

## 🧩 Pipeline Architecture

