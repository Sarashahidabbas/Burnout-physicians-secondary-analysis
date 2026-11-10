# Burnout Among Physicians: Secondary Analysis of Public Data
## Research Question

Which workplace and personal factors are linked with severe burnout in physicians?

### Data Source

Public dataset of 1,434 Bangladeshi physicians from 62 hospitals, collected between 2019 and 2021.

Dataset citation:

Rizwan, F. (2025). Burnout_Risks_Bangladeshi_Physicians_Survey_2019_2021. Mendeley Data, V3.

DOI: https://doi.org/10.17632/3d7h58d4k3.3

Licence: CC BY 4.0.

Original study:

Rizwan F, et al. Burnout risks in Bangladeshi physicians: a multicenter, cross-sectional study. Heliyon. 2023;9:e22386.

Important Note: I did not collect this data. This project is a secondary analysis of publicly available survey data.

To run the code, download the dataset from the DOI above and place it in the project folder with the following filename:

Raw_Data_DIB__1_.xlsx

## Methods
Outcome: Burnout level (five categories).
Main outcome definition: Severe or very severe burnout versus all lower burnout levels.
Category labels: Follow the data paper (Table 1). Sparse categories were merged for modelling.
Chi-square tests: Used to examine associations between each factor and burnout level.
Multivariable logistic regression: Used to identify factors associated with severe or very severe burnout, reporting adjusted odds ratios.
Ordinal logistic regression: Used as a sensitivity analysis across all five burnout levels.
Tools and Technologies
Python
pandas
SciPy
statsmodels
Key Results
Burnout Prevalence
25.7% of physicians (368 of 1,434) had severe or very severe burnout.
49.8% were at initial risk of burnout.
Only 2.5% showed no signs of burnout.
Factors Associated with Severe Burnout

Multivariable logistic regression identified the following associations:

Conflict with co-workers: Higher odds of severe burnout (OR 1.65, 95% CI 1.19–2.28).
Conflict with both co-workers and family: Higher odds (OR 1.58, 95% CI 1.14–2.19).
Hospital type: Physicians working in non-government hospitals and clinics had higher odds than those in government hospitals (OR 1.57, 95% CI 1.15–2.13).
Perceived professional flexibility: Physicians who felt other professions were more flexible had lower odds of severe burnout (OR 0.67, 95% CI 0.49–0.90).

The reference group for interpersonal conflict was physicians reporting no conflict.

Gender, age, BMI, private practice, vacation, marital status, liabilities, and living with family were not statistically significant after adjustment.

The ordinal logistic regression model showed the same direction of associations for interpersonal conflict, workplace type, and perceived professional flexibility.

## Limitations
The cross-sectional study design means that the findings represent associations and cannot establish causal relationships.
Burnout level was based on a self-scored questionnaire total. Item-level scores were unavailable, so burnout subscale analysis and moderation analysis were not possible.
The model explained relatively little variation (McFadden pseudo R² = 0.04; AUC = 0.64).
Data came mostly from hospitals in Dhaka, limiting the generalisability of findings to other healthcare settings.
Some categories had small sample sizes, making their estimates potentially unstable.
Note on Differences from the Original Paper

Several findings in this secondary analysis differ from those reported in the original publication.

The original paper reports very large odds ratios (for example, above 500) and indicates that government hospital physicians experience greater burnout.

However, in the dataset used for this analysis, severe or very severe burnout was more prevalent among physicians working in non-government hospitals and clinics (approximately 34%) than among those working in government hospitals (approximately 24%). The regression model also showed higher odds of severe burnout in non-government settings.

The extremely large odds ratios reported in the original paper may be related to sparse categories. To improve model stability, sparse categories were merged in this secondary analysis.

Additionally, small differences were identified between the raw dataset and the original paper's tables. For example, the dataset contained 866 male and 568 female physicians, compared with 860 male and 574 female physicians reported in the original paper.

These differences are documented to maintain transparency and reproducibility.

### Project Files
analysis.py – Complete Python analysis code.
table1.csv to table4.csv – Statistical results tables.
fig1.png to fig5.png – Data visualisations and charts.
model_fit.txt – Model fit summaries.
console_output.txt – Analysis console output.
Author

Sara Shahid Abbas, BDS, MSHCM

Secondary analysis of publicly available survey data on physician burnout in Bangladesh.
