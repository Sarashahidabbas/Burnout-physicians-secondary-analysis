# Burnout Among Physicians: Secondary Analysis of Public Data

## Research question
Which workplace and personal factors are linked with severe burnout in physicians?

## Data source
Public dataset of 1,434 Bangladeshi physicians from 62 hospitals, collected 2019 to 2021.
Rizwan F. (2025). Burnout_Risks_Bangladeshi_Physicians_Survey_2019_2021. Mendeley Data, V3.
DOI: 10.17632/3d7h58d4k3.3. Licence: CC BY 4.0.
Original study: Rizwan F, et al. Burnout risks in Bangladeshi physicians: a multicenter, cross-sectional study. Heliyon 2023;9:e22386.

I did not collect this data. This is a secondary analysis. To run the code, download the data file from the DOI above and place it in this folder as `Raw_Data_DIB__1_.xlsx`.

## Methods
- Outcome: burnout level (5 levels). For the main model, severe or very severe burnout versus all lower levels.
- Category labels follow the data paper (Table 1). Sparse categories were merged for modelling.
- Chi-square tests for each factor against burnout level.
- Multivariable logistic regression for severe or very severe burnout (adjusted odds ratios).
- Ordinal logistic regression on all 5 levels as a sensitivity check.
- Tools: Python, pandas, scipy, statsmodels.

## Key results
- 25.7% of physicians (368 of 1,434) had severe or very severe burnout. About half (49.8%) were at initial risk, and only 2.5% showed no sign.
- Interpersonal conflict was linked with higher odds of severe burnout. Conflict with co-workers: OR 1.65 (95% CI 1.19 to 2.28). Conflict with both co-workers and family: OR 1.58 (1.14 to 2.19). The reference group was no conflict.
- Physicians in non-government hospitals and clinics had higher odds than those in government hospitals: OR 1.57 (1.15 to 2.13).
- Physicians who felt other professions are more flexible had lower odds: OR 0.67 (0.49 to 0.90).
- Gender, age, BMI, private practice, vacation, marital status, liabilities and living with family were not significant after adjustment.
- The ordinal model gave the same direction for conflict, workplace and flexibility.

## Limitations
- Cross-sectional data, so these are associations and not causes.
- The burnout level comes from a self-scored questionnaire total. Item-level scores are not in the file, so burnout subscales and moderation analysis were not possible.
- The model explains little of the variation (McFadden pseudo R2 0.04, AUC 0.64).
- Data come mostly from hospitals in Dhaka, so results may not apply to other settings.
- Some categories are small, so estimates for them are unstable.
- Several results differ from the original paper. See the note below.

## Note on differences from the original paper
The paper reports very large odds ratios (for example above 500) and says government hospital doctors are more burnt out. In the data, severe burnout is higher in non-government hospitals (about 29% versus 19% in government hospitals), and my model agrees with the data. The very large odds ratios in the paper are likely due to sparse categories. I merged sparse categories to avoid this. The raw file also has small count differences from the paper's tables, for example 866 male and 568 female physicians against 860 and 574 in the paper.

## Files
- `analysis.py`: full analysis code
- `results/`: tables as CSV files
- `figures/`: charts

## Author
Sara Shahid Abbas, BDS, MSHCM
