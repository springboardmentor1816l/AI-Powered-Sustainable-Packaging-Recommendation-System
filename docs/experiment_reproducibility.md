Experiment Reproducibility Report



EcoPackAI – Sustainable Packaging Recommendation System



📌 Purpose of This Document



This document ensures that anyone in the future (engineers, auditors, researchers, new hires) can reproduce every ML experiment exactly — same results, same splits, same pipeline, same metrics.



No hidden randomness.

No unclear processing steps.

100% traceable \& repeatable.



1️⃣ Dataset Versioning

Dataset Used



Integrated Product–Material dataset



Version: v1.0



Size: 123,607 rows × 73 columns



Source:

/data/model\_ready/integrated\_dataset.csv



Dataset State Guarantee



All missing values processed



Feature engineering applied (CII, CEI, MSS)



Encoded product \& material attributes included



No duplicate product–material pairs



2️⃣ Train/Test Split Setup



Split configuration:



Method: GroupShuffleSplit



Train ratio: 80%



Test ratio: 20%



Grouping key: product\_id



Seed: 42



Why grouping?

→ To prevent information leakage from the same product appearing in both sets.



3️⃣ Cross-Validation Configuration



Method: GroupKFold



Parameter	Value

K-fold size	5

Shuffle	No

Group key	product\_id



Reason:



Avoid leakage between folds



Validate model robustness using different product groups



4️⃣ Randomisation \& Seeds



Reproducibility requires full seed locking.



Seeds used:



Component	Seed

NumPy RNG	42

Train/test split	42

Model random\_state	42

5️⃣ Pipeline Versioning



Preprocessing pipeline version: v1.0



Pipeline includes:



numeric imputation



scaling (MinMax)



one-hot categorical encoding



column transformer structure



Saved artifact:

/models/preprocessing/preprocessing\_pipeline.pkl



NOTE: Entire pipeline must be used during inference.

Manual preprocessing is forbidden.



6️⃣ Environment Dependencies



To reproduce experiments exactly, environment details are fixed:



Python



3.10.x



Core Libraries

pandas == 2.1.x

scikit-learn == 1.4.x

numpy == 1.26.x

joblib == 1.4.x

matplotlib == 3.7.x





Pinned requirements file:

requirements.txt



7️⃣ Hardware Dependencies



Training environment:



CPU-based execution



RAM >= 16GB recommended



No GPU dependency in this stage



8️⃣ Model Repeatability Rules



To ensure someone else can replicate results:



1️⃣ Use exact same dataset version

2️⃣ Use saved pipeline objects

3️⃣ Use same seeds and split strategy

4️⃣ Do not shuffle rows manually

5️⃣ Always run preprocessing before model fit

6️⃣ Never train on processed test rows

7️⃣ Record model hyperparameters



9️⃣ Output Determinism



Model outputs are deterministic because:



random\_state fixed everywhere



predefined scoring methods



no stochastic training algorithms (yet)



🔟 Risk Areas \& Controls

Risk	Impact	Control

Dataset modified	mismatched results	dataset version freeze

Re-running split	new train/test groups	seed lock + group key

Updated scikit-learn version	pipeline mismatch	version pinning

engineer forgets group split	leakage	code comments + docs

wrong encoded form input	inference failure	pipeline enforcement

11️⃣ Reproduction Test Procedure



Any engineer can verify reproducibility by:



1️⃣ Load dataset \& pipeline

2️⃣ Rerun train/test split

3️⃣ Ensure:



metrics\_original == metrics\_rerun





If mismatch occurs → environment drift.



12️⃣ Future Reproducibility Enhancements



MLflow experiment tracking



DVC dataset versioning



model registry system



dockerization



These will improve transparency and rollback ability.



✔️ Conclusion



This project’s ML workflow is reproducible because:



dataset version locked



preprocessing serialized



train/test split deterministic



CV folds deterministic



seeds controlled



environment frozen



Anyone can reproduce results with confidence — even years later.

