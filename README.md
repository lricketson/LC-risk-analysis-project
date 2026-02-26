# LendingClub Credit Risk Optimisation & Statistical Inference

## Executive Summary

This project is an end-to-end quantitative risk pipeline and statistical analysis designed to optimise a consumer credit portfolio. Using a dataset of over 1.3 million historical LendingClub loans, the project combines rigorous statistical inference with machine learning to identify high-risk borrowers.

By engineering financial ratios and training a Gradient Boosting Classifier, the model mathematically optimises the loan approval threshold. Against a baseline portfolio where all loans are approved, this model generates an additional **$43.04 Million in simulated net profit**.

---

## 1. Data Inspection & Preprocessing

- **Initial Inspection:** The raw dataset consists of 1,345,310 observations and over 140 variables, encompassing continuous (e.g., `loan_amnt`, `annual_inc`), categorical (e.g., `grade`, `verification_status`), and binary (e.g., `term`) types.
- **Missing Values Handling:** Missingness was quantified across all features. Variables were classified as structurally missing, potentially informative, or noise. Features with extreme missingness lacking predictive value were dropped, while informative missingness in core financial metrics was handled via median imputation to preserve the sample size without distorting the distribution.
- **Leakage & Availability Filtering:** A strict chronological filter was applied to remove "future-looking" variables that would not be available at loan origination (e.g., `total_pymnt`, `recoveries`, `last_fico_range`). Retaining these would cause severe data leakage and artificially inflate model performance.

## 2. Exploratory Data Analysis (EDA)

Before modelling, the underlying distributions of the portfolio were analysed:

- **Descriptive Statistics:** Computed means, medians, and standard deviations for core continuous variables, revealing the impact of extreme outliers (e.g., $0 annual income entries), which were subsequently filtered.
- **Overall Default Rate:** Established the baseline class imbalance of the dataset.
- **Group Comparisons:** Visualised and compared the distributions of loan grades and FICO scores between defaulted and non-defaulted loans, proving that traditional risk strata exhibit significant overlap.
- **Expected Value of a Borrower:** Calculated the expected profit from a full-paying borrower to be $3,014, and LGD of a defaulter to be $7,065

## 3. Statistical Inference

To establish a rigorous mathematical foundation for the predictive models, formal statistical testing was conducted:

- **Hypothesis Testing:**
  - _T-Test (Mean Comparison):_ Conducted a two-sample t-test comparing the mean annual income of defaulted vs. non-defaulted loans, interpreting the p-value and test statistic to prove a statistically significant difference.
  - _Chi-Square Test (Association):_ Examined the dependence between LendingClub assigned `grade` and actual default rates.
  - _Robustness Test:_ Tested a different variable to validate findings on associative relationships between variables.
- **Confidence Intervals:** Constructed frequentist confidence intervals for specific sub-populations, quantifying the uncertainty around default rates within specific loan grades and the difference in mean interest rates between the two target classes.
- **Selection Bias (Booked vs. Through-the-Door):** This analysis acknowledges that all estimated probabilities are conditional on initial approval. Because LendingClub's proprietary filter already removed the highest-risk applicants, the observed relationships in this dataset suffer from survivorship bias. Therefore, model coefficients represent risk _within a pre-screened population_, not causal population-level effects.

## 4. Predictive Modelling

The machine learning architecture was built to evaluate both linear and non-linear risk topologies.

- **Model Specification:**
  - **Logistic Regression:** Used as an interpretable baseline. Coefficients were estimated via Maximum Likelihood Estimation (MLE). Analysed feature importance through log-odds and odds ratios, confirming the plausibility of MLE assumptions post-outlier removal.
  - **Non-Linear Models:** Trained Random Forest and Gradient Boosting classifiers to capture complex, non-linear interactions (e.g., `loan_to_income` ratios).
- **Validation Strategy:** Implemented a rigorous train/test split to ensure out-of-sample validity and prevent overfitting.
- **Evaluation Metrics:** Models were evaluated holistically, not just on ranking ability:
  - _ROC-AUC:_ To measure pure discriminative power.
  - _Precision, Recall, & F1 Score:_ To measure performance on the imbalanced default class.
  - _Calibration (Brier Score):_ To ensure predicted probabilities aligned with real-world default frequencies.

## 5. Financial Profit Simulation (Results)

Given the portfolio's average loan metrics, the mathematical breakeven threshold was calculated at **29.9%** (Expected Value = 0).

- **Baseline (Approve All):** $113.2M Profit
- **Logistic Regression:** $138.3M Profit (at 71.0% threshold)
- **Random Forest:** $144.8M Profit (at 34.0% threshold)
- **Gradient Boosting:** $156.2M Profit (at 34.0% threshold)

**Conclusion:** The Gradient Boosting model empirically converged near the theoretical mathematical breakeven, demonstrating the highest financial utility and calibration.

## 6. Tech Stack & Libraries

- **Language:** Python 3.10.6
- **Data Engineering & Manipulation:** Pandas, NumPy
- **Machine Learning:** Scikit-Learn
- **Statistical Inference:** SciPy, Statsmodels
- **Data Visualisation:** Matplotlib, Seaborn
- **Compute Environment:** Jupyter Notebooks, parallelised tree-building optimised for local hardware.
