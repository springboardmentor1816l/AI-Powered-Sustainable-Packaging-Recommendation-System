\# Train/Test Split Summary



\## 📌 Dataset Used

Integrated product–material dataset generated after:

\- product preprocessing

\- material preprocessing

\- engineered sustainability features (CII, CEI, MSS)

\- full integration using product × material matching rules



Total Rows: \*\*123,607\*\*  

Total Columns: \*\*73\*\*



---



\## 📌 Split Method

Train/test split performed using \*\*GroupShuffleSplit\*\* to ensure no product leakage.



\- Group column used: `product\_id`

\- Train size: `80%`

\- Test size: `20%`

\- Random seed: `42`

\- # of products leaking across splits: `0`



---



\## 📌 Split Results

| Dataset | Rows | Percentage |

|--------|------|------------|

| Train  | 98,885 | 80% |

| Test   | 24,722 | 20% |



---



\## 📌 Leakage Validation

We verified that \*\*no product\_id appears in both partitions\*\*:





This confirms leakage safety.



---



\## 📌 Target Variable

`Final\_Recommendation\_Score`



Forecast goal:

predict sustainability recommendation score for any product–material pair.



---



\## 📌 Feature Count After Cleaning

\- Total usable ML features: \*\*70\*\*

\- Removed before modeling:

&nbsp; - product\_id

&nbsp; - material\_id

&nbsp; - target column



---



\## 📌 Why This Split is Correct

\- prevents identity leakage  

\- maintains data diversity  

\- avoids same product distribution in both sets  

\- supports fair model evaluation  



---



\## 📌 Next Steps

1\. Apply preprocessing pipeline (ColumnTransformer)

2\. Train baseline models using GroupKFold

3\. Evaluate error distribution and bias

4\. Tune model complexity



