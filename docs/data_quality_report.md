test_01_imputation_logic (__main__.TestPreprocessingLogic.test_01_imputation_logic)
Tests that median imputation works correctly on a missing value. ... ERROR
test_02_feature_engineering_logic (__main__.TestPreprocessingLogic.test_02_feature_engineering_logic)
Tests the exact calculation of a composite index (Cost Efficiency Index). ... ok
test_03_scaling_output_range (__main__.TestPreprocessingLogic.test_03_scaling_output_range)
Tests that MinMaxScaler correctly scales a sample column to [0, 1]. ... ERROR

======================================================================
ERROR: test_01_imputation_logic (__main__.TestPreprocessingLogic.test_01_imputation_logic)
Tests that median imputation works correctly on a missing value.
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\A.L.N. Srinivas\AppData\Local\Temp\ipykernel_5572\66421572.py", line 119, in test_01_imputation_logic
    imputer = SimpleImputer(strategy='median')
              ^^^^^^^^^^^^^
NameError: name 'SimpleImputer' is not defined

======================================================================
ERROR: test_03_scaling_output_range (__main__.TestPreprocessingLogic.test_03_scaling_output_range)
Tests that MinMaxScaler correctly scales a sample column to [0, 1].
----------------------------------------------------------------------
Traceback (most recent call last):
  File "C:\Users\A.L.N. Srinivas\AppData\Local\Temp\ipykernel_5572\66421572.py", line 148, in test_03_scaling_output_range
    scaler = MinMaxScaler()
             ^^^^^^^^^^^^
NameError: name 'MinMaxScaler' is not defined

----------------------------------------------------------------------
Ran 3 tests in 0.204s

FAILED (errors=2)


--- Unit Test Summary ---
Tests Run: 3
Failures: 0
Errors: 2
Overall Unit Test Status: FAILURE
