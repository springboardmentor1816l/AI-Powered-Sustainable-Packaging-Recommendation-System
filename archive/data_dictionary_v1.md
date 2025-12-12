         Column          |      Table           |     Type    |   Descrition
  material_id            |      materials       |     INT     |   Unique identifier 
  material_type          |      materials       |     VARCHAR |   Material type 
  strength_mpa           |      materials       |     FLOAT   |   Strength property 
 biodegradability_percent|      materials       |     FLOAT   |   Eco‑friendly score
  cost_per_kg            |      materials       |     FLOAT   |   Pricing
  product_id             |      products        |     INT     |   Product unique ID 
  fragility_index        |      products        |     INT     |   Required handling care 
  shipping_type          |         products     |     VARCHAR |   Shipping mode 
  rec_id                 | recommendation_logs  |     INT     |   Prediction record ID 
  material_rank          | recommendation_logs  |     INT     |   Ranking of recommended material 
  created_at             | recommendation_logs  |    TIMESTAMP|   Timestamp of log entry 