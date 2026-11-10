"""
Burnout among Bangladeshi physicians: secondary analysis of public data.
Data: Rizwan F. (2025). Burnout_Risks_Bangladeshi_Physicians_Survey_2019_2021.
Mendeley Data, V3. DOI 10.17632/3d7h58d4k3.3 (CC BY 4.0).
Code book follows the category order in Rizwan et al., Heliyon 2023, Table 1.
"""
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, spearmanr
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.miscmodels.ordinal_model import OrderedModel

DATA = "Raw_Data_DIB__1_.xlsx"
d = pd.read_excel(DATA)
d.columns = [c.strip().replace(" ", "_") for c in d.columns]
n = len(d)

burn_lbl = {1: "No sign", 2: "Little sign", 3: "Initial risk", 4: "Severe risk", 5: "Very severe risk"}
d["Burn_label"] = d["Burn_Out"].map(burn_lbl)
d["High_burnout"] = (d["Burn_Out"] >= 4).astype(int)   # severe or very severe

# ---- labels (order as in Table 1 of the data paper) ----
lab = {
 "Gender": {1: "Male", 2: "Female"},
 "Age_code": {1: "20-29", 2: "30-39", 3: "40-49", 4: "50-59", 5: "60-69"},
 "BMI": {1: "Underweight", 2: "Normal", 3: "Overweight", 4: "Obese"},
 "Working_Place": {1: "Government hospital", 2: "Non-government hospital", 3: "Clinic"},
 "Duration": {1: "<1 y", 2: "1-3 y", 3: "3-5 y", 4: "5-10 y", 5: ">10 y"},
 "Private_Practice": {1: "Inside city", 2: "Outside city", 3: "None", 4: "Inside and outside city"},
 "Working_Hour": {1: "Up to 6 h", 2: "Up to 8 h", 3: "Up to 10 h", 4: "Up to 12 h", 5: "Up to 14 h", 6: ">14 h"},
 "Weekly_Vacation": {1: "Yes", 2: "No"},
 "Marital_Status": {1: "Single", 2: "Married", 3: "Divorced", 4: "Widowed"},
 "Liabilities": {1: "Yes", 2: "No"},
 "Staying_with_Family": {1: "Yes", 2: "No"},
 "Conflict": {1: "Co-workers", 2: "Family", 3: "Both", 4: "None"},
 "Politics": {1: "Worried", 2: "Not worried"},
 "Flexibility": {1: "Others more flexible", 2: "Not"},
 "Dissatisfaction": {1: "Anxiety", 2: "Fatigue", 3: "Insomnia", 4: "Agitation", 5: "Depression",
                     6: "Anxiety+depression", 7: "Fatigue+insomnia", 8: "None"},
}

# ---- Table 1: descriptives ----
rows = []
for v, m in lab.items():
    vc = d[v].map(m).value_counts()
    for k in m.values():
        c = int(vc.get(k, 0))
        rows.append([v, k, c, round(100 * c / n, 1)])
pd.DataFrame(rows, columns=["Variable", "Category", "n", "%"]).to_csv("results/table1_descriptives.csv", index=False)

# ---- Burnout distribution ----
bd = d["Burn_label"].value_counts().reindex(list(burn_lbl.values()))
pd.DataFrame({"n": bd, "%": (100 * bd / n).round(1)}).to_csv("results/burnout_distribution.csv")

# ---- Table 2: bivariate (chi-square) vs burnout level; and % high burnout ----
biv = []
for v in list(lab) + ["Designation", "Specialization", "Income", "Family_members", "Family_Functions",
                      "Vacation_with_Family", "Disappointing_Thing", "Feelings", "Mental_Disturbances"]:
    ct = pd.crosstab(d[v], d["Burn_Out"])
    chi2, p, dof, _ = chi2_contingency(ct)
    ct2 = pd.crosstab(d[v], d["High_burnout"])
    p_hi = chi2_contingency(ct2)[1]
    rho, p_rho = spearmanr(d[v], d["Burn_Out"])
    biv.append([v, round(chi2, 1), dof, p, p_hi])
biv = pd.DataFrame(biv, columns=["Variable", "chi2", "df", "p_chi2_5levels", "p_chi2_high_vs_not"])
biv["p_chi2_5levels"] = biv["p_chi2_5levels"].round(4)
biv["p_chi2_high_vs_not"] = biv["p_chi2_high_vs_not"].round(4)
biv.to_csv("results/table2_bivariate.csv", index=False)

# ---- Modelling data: collapsed categories (sparse cells merged) ----
m = pd.DataFrame({"high": d["High_burnout"], "burn": d["Burn_Out"]})
m["female"] = (d["Gender"] == 2).astype(int)
m["age"] = d["Age_code"].map({1: "20-29", 2: "30-39", 3: "40-49", 4: "50+", 5: "50+"})
m["bmi"] = d["BMI"].map({1: "Normal/under", 2: "Normal/under", 3: "Overweight", 4: "Obese"})
m["nongovt"] = (d["Working_Place"] != 1).astype(int)
m["private_practice"] = d["Private_Practice"].map({1: "Inside/outside only", 2: "Inside/outside only", 3: "None", 4: "Both"})
m["hours"] = d["Working_Hour"].map({1: "<=6", 2: "8", 3: "10", 4: "12+", 5: "12+", 6: "12+"})
m["no_vacation"] = (d["Weekly_Vacation"] == 2).astype(int)
m["married"] = (d["Marital_Status"] == 2).astype(int)
m["liabilities"] = (d["Liabilities"] == 1).astype(int)
m["not_with_family"] = (d["Staying_with_Family"] == 2).astype(int)
m["conflict"] = d["Conflict"].map({1: "Co-workers", 2: "Family", 3: "Both", 4: "None"})
m["politics_worry"] = (d["Politics"] == 1).astype(int)
m["others_flexible"] = (d["Flexibility"] == 1).astype(int)

formula = ("high ~ female + C(age, Treatment('20-29')) + C(bmi, Treatment('Normal/under')) + nongovt"
           " + C(private_practice, Treatment('None')) + C(hours, Treatment('<=6')) + no_vacation + married"
           " + liabilities + not_with_family + C(conflict, Treatment('None')) + politics_worry + others_flexible")
logit = smf.logit(formula, data=m).fit(disp=0)

def or_table(res):
    ci = res.conf_int()
    t = pd.DataFrame({"OR": np.exp(res.params), "CI_low": np.exp(ci[0]), "CI_high": np.exp(ci[1]), "p": res.pvalues})
    t = t.drop("Intercept", errors="ignore").round(3)
    import re
    t.index = [re.sub(r"C\((\w+), Treatment\('([^']*)'\)\)\[T\.([^\]]*)\]", r"\1: \3 (vs \2)", i) for i in t.index]
    return t
tab = or_table(logit)
tab.to_csv("results/table3_logistic_high_burnout.csv")

# ---- Sensitivity: ordinal (proportional-odds) logistic regression on 5 levels ----
X = pd.get_dummies(m.drop(columns=["high", "burn"]), drop_first=False).astype(float)
for col in ["age_20-29", "bmi_Normal/under", "private_practice_None", "hours_<=6", "conflict_None"]:
    X = X.drop(columns=col)
om = OrderedModel(m["burn"], X, distr="logit").fit(method="bfgs", disp=0, maxiter=500)
k = X.shape[1]
ci = om.conf_int().iloc[:k]
ordt = pd.DataFrame({"OR": np.exp(om.params.iloc[:k]), "CI_low": np.exp(ci[0]), "CI_high": np.exp(ci[1]), "p": om.pvalues.iloc[:k]}).round(3)
ordt.to_csv("results/table4_ordinal_sensitivity.csv")

# ---- Fit stats ----
from sklearn.metrics import roc_auc_score
auc = roc_auc_score(m["high"], logit.predict(m))
with open("results/model_fit.txt", "w") as f:
    f.write(f"N = {n}\nHigh burnout (severe or very severe) = {int(m['high'].sum())} ({100*m['high'].mean():.1f}%)\n")
    f.write(f"Logistic model: pseudo R2 (McFadden) = {logit.prsquared:.3f}, AIC = {logit.aic:.1f}, AUC = {auc:.3f}\n")

# ---- Figures ----
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig, ax = plt.subplots(figsize=(6.5, 3.6))
pct = 100 * bd / n
ax.bar(pct.index, pct.values, color="#4C78A8")
for i, v in enumerate(pct.values): ax.text(i, v + 0.8, f"{v:.0f}%", ha="center")
ax.set_ylabel("Physicians (%)"); ax.set_title(f"Burnout level (N = {n})")
plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig("figures/fig1_burnout_distribution.png", dpi=200); plt.close()

def hi_rate(col, mapping, title, fname, order=None):
    s = d.assign(g=d[col].map(mapping)).groupby("g")["High_burnout"].agg(["mean", "size"])
    if order: s = s.reindex(order)
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    ax.bar(s.index, 100 * s["mean"], color="#F58518")
    for i, (v, c) in enumerate(zip(s["mean"], s["size"])): ax.text(i, 100 * v + 0.8, f"{100*v:.0f}%\n(n={c})", ha="center", fontsize=8)
    ax.set_ylabel("Severe/very severe burnout (%)"); ax.set_title(title)
    ax.set_ylim(0, max(100 * s["mean"]) + 12)
    plt.xticks(rotation=20, ha="right"); plt.tight_layout(); plt.savefig(f"figures/{fname}", dpi=200); plt.close()

hi_rate("Working_Place", lab["Working_Place"], "High burnout by workplace", "fig2_workplace.png")
hi_rate("Working_Hour", {1: "<=6 h", 2: "8 h", 3: "10 h", 4: "12 h", 5: "14 h", 6: ">14 h"}, "High burnout by daily working hours", "fig3_hours.png",
        ["<=6 h", "8 h", "10 h", "12 h", "14 h", ">14 h"])
hi_rate("Conflict", lab["Conflict"], "High burnout by interpersonal conflict", "fig4_conflict.png", ["None", "Co-workers", "Family", "Both"])

# forest plot of logistic ORs
t = tab.copy().sort_values("OR")
fig, ax = plt.subplots(figsize=(7, 6.5))
ax.errorbar(t["OR"], range(len(t)), xerr=[t["OR"] - t["CI_low"], t["CI_high"] - t["OR"]], fmt="o", color="#333", ecolor="#999", capsize=2)
ax.axvline(1, color="red", lw=1, ls="--"); ax.set_xscale("log")
ax.set_yticks(range(len(t))); ax.set_yticklabels(t.index, fontsize=7)
ax.set_xlabel("Adjusted odds ratio (log scale, 95% CI)"); ax.set_title("Factors linked with severe/very severe burnout")
plt.tight_layout(); plt.savefig("figures/fig5_forest_plot.png", dpi=200); plt.close()

print(open("results/model_fit.txt").read())
print(pd.read_csv("results/burnout_distribution.csv").to_string(index=False))
print("\nBIVARIATE\n", biv.sort_values("p_chi2_high_vs_not").to_string(index=False))
print("\nLOGISTIC (high burnout)\n", tab.to_string())
print("\nORDINAL\n", ordt.to_string())
