\# Cross Validation Strategy



\## 📌 Objective

To ensure ML model performance is evaluated reliably while avoiding data leakage due to product repetition in the dataset.



---



\## 📌 Cross Validation Approach

We are using:



\### \*\*Group K-Fold Cross Validation\*\*



Groups defined by: product\_id



---



\## 📌 Why GroupKFold?



The integrated dataset contains multiple material rows for the same product.  

If we used traditional KFold:



\- identical product embeddings could appear in both training and validation sets,

\- producing inaccurate metrics and inflated performance.



GroupKFold guarantees:



\- all product rows stay together

\- validation set represents new unseen products

\- prevents recommendation leakage

\- increases scientific reliability



---



\## 📌 Technical Summary



| Parameter | Value |

|----------|-------|

| Method | GroupKFold |

| # Folds | 5 |

| Shuffle | Not required |

| Group Key | product\_id |

| Target | Final\_Recommendation\_Score |



---



\## 📌 Data Flow

1\. Split original dataset into 5 non-overlapping grouped folds.

2\. Each fold:

&nbsp;  - trained on 4/5 product groups

&nbsp;  - validated on 1/5 product groups

3\. average metrics over folds.



---



\## 📌 Expected Benefits

\- unbiased generalisation estimates

\- robustness across product variation

\- prevents overfitting bias

\- industry-grade validation structure

\- reproducible experiments



---



\## 📌 Future Enhancement

For classification tasks, strategy can be extended to:

\- GroupStratifiedKFold (if product categories are added)

\- Repeated GroupKFold (for ensemble learning)



---



\## 📌 Final Notes

Cross-validation strategy aligns with:

\- business constraints

\- academic ML validation standards

\- deployment expectations





