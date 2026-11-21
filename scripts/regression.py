# Module 4: linear regression and logistic regression.
# Input:  train_set.csv, test_set.csv (from prep_train_test.py)
# Output: regression charts in charts/

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import (mean_squared_error, mean_absolute_error, r2_score,
                             accuracy_score, confusion_matrix, precision_score, recall_score)
from matplotlib.colors import LinearSegmentedColormap

BG, PANEL, LINE = "#0b0f1a", "#131a2b", "#232d47"
TEXT, DIM = "#e9e7e1", "#9aa3bd"
GOLD, TEAL, RUST = "#e8a33d", "#4a95a0", "#c1502e"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TEXT, "axes.labelcolor": TEXT, "axes.edgecolor": LINE,
    "xtick.color": DIM, "ytick.color": DIM, "font.size": 11,
    "axes.titlesize": 12, "axes.titlecolor": TEXT,
    "legend.facecolor": PANEL, "legend.edgecolor": LINE})

os.makedirs("charts", exist_ok=True)
train = pd.read_csv("train_set.csv")
test = pd.read_csv("test_set.csv")

# ================= LINEAR REGRESSION =================
# target: planet mass (log10 Earth masses), a number. Predictors: the other seven
# measurements, also log10, since these span several orders of magnitude and the
# mass-radius relationship is close to a straight line on log-log axes.
predictors = ["pl_orbper", "pl_rade", "pl_eqt", "st_teff", "st_rad", "st_mass", "sy_dist"]

# Many planets in the archive's composite table have one of mass or radius filled in from
# the other with a published piecewise mass-radius formula (Chen and Kipping style:
# R = 1.008 M^0.279 below 2.04 Earth masses, 0.808 M^0.589 up to 131.6, 17.74 M^-0.044 above).
# A planet within 1% of that curve is flagged, because for it the mass is close to a formula
# of the radius and not an independent measurement.
def on_formula_curve(d):
    M = d["pl_bmasse"]
    r_formula = np.where(M < 2.04, 1.008 * M ** 0.279, np.where(M < 131.6, 0.808 * M ** 0.589, 17.74 * M ** -0.044))
    return (np.abs(d["pl_rade"] - r_formula) / d["pl_rade"] < 0.01).to_numpy()

train["on_curve"] = on_formula_curve(train)
test["on_curve"] = on_formula_curve(test)
print("Within 1% of the formula curve: training", int(train["on_curve"].sum()), "of", len(train),
      "| testing", int(test["on_curve"].sum()), "of", len(test))

def lin_scores(y_true, y_pred):
    return (mean_squared_error(y_true, y_pred) ** 0.5, mean_absolute_error(y_true, y_pred), r2_score(y_true, y_pred))

X_train = np.log10(train[predictors]); X_test = np.log10(test[predictors])
y_train = np.log10(train["pl_bmasse"]); y_test = np.log10(test["pl_bmasse"])

# model A: all training planets
lin = LinearRegression().fit(X_train, y_train)
pred = lin.predict(X_test)
rmse, mae, r2 = lin_scores(y_test, pred)
base_rmse = mean_squared_error(y_test, np.full(len(y_test), y_train.mean())) ** 0.5
print("\nLinear regression, all planets (log10 mass)")
print("RMSE:", round(rmse, 3), "MAE:", round(mae, 3), "R2:", round(r2, 3), "| RMSE of guessing the training mean:", round(base_rmse, 3))
print("typical error as a factor: RMSE", round(10 ** rmse, 2), "x, MAE", round(10 ** mae, 2), "x")
oc = test["on_curve"].to_numpy()
r_on = lin_scores(y_test[oc], pred[oc]); r_off = lin_scores(y_test[~oc], pred[~oc])
print("  model A on formula-curve planets: RMSE %.3f MAE %.3f R2 %.3f" % r_on)
print("  model A on other planets:         RMSE %.3f MAE %.3f R2 %.3f" % r_off)
print("intercept:", round(float(lin.intercept_), 3))
for name, c in zip(predictors, lin.coef_):
    print(f"  {name}: {c:.3f}  (doubling it multiplies predicted mass by {2 ** c:.2f})")

# model B: trained and tested only on planets that are NOT on the formula curve
tr_m, te_m = train[~train["on_curve"]], test[~test["on_curve"]]
lin_m = LinearRegression().fit(np.log10(tr_m[predictors]), np.log10(tr_m["pl_bmasse"]))
pred_m = lin_m.predict(np.log10(te_m[predictors])); y_m = np.log10(te_m["pl_bmasse"])
rmse_m, mae_m, r2_m = lin_scores(y_m, pred_m)
base_m = mean_squared_error(y_m, np.full(len(y_m), np.log10(tr_m["pl_bmasse"]).mean())) ** 0.5
print("\nLinear regression, planets off the formula curve only: train", len(tr_m), "test", len(te_m))
print("RMSE:", round(rmse_m, 3), "MAE:", round(mae_m, 3), "R2:", round(r2_m, 3), "| baseline RMSE:", round(base_m, 3))
print("typical error as a factor: RMSE", round(10 ** rmse_m, 2), "x, MAE", round(10 ** mae_m, 2), "x")
for name, c in zip(predictors, lin_m.coef_):
    print(f"  {name}: {c:.3f}  (doubling it multiplies predicted mass by {2 ** c:.2f})")

# predicted vs actual, colored by whether the planet sits on the formula curve
lo, hi = min(y_test.min(), pred.min()), max(y_test.max(), pred.max())
plt.figure(figsize=(6.8, 6))
plt.scatter(y_test[oc], pred[oc], s=10, alpha=0.4, color=TEAL, label=f"on the formula curve ({oc.sum()})")
plt.scatter(y_test[~oc], pred[~oc], s=12, alpha=0.6, color=GOLD, label=f"off the curve ({(~oc).sum()})")
plt.plot([lo, hi], [lo, hi], color=TEXT, linewidth=1.2, linestyle="--", label="perfect prediction")
plt.xlabel("Actual mass (log10 Earth masses)")
plt.ylabel("Predicted mass (log10 Earth masses)")
plt.title(f"Linear regression: predicted vs actual (R$^2$ = {r2:.2f})")
plt.legend(fontsize=9)
plt.tight_layout(); plt.savefig("charts/lin_pred_vs_actual.png", dpi=150); plt.close()

# coefficients
order = np.argsort(lin.coef_)
plt.figure(figsize=(7, 4.5))
plt.barh(np.array(predictors)[order], lin.coef_[order],
         color=[TEAL if c > 0 else RUST for c in lin.coef_[order]])
plt.axvline(0, color=DIM, linewidth=0.8)
plt.xlabel("Coefficient (change in log10 mass per 1 change in log10 predictor)")
plt.title("Linear regression coefficients")
plt.tight_layout(); plt.savefig("charts/lin_coefficients.png", dpi=150); plt.close()

# ================= LOGISTIC REGRESSION =================
# label: habitable (0 or 1). Predictors: all eight measurements, log10 then
# standardized (scaler fit on the training set only) so coefficients are comparable.
features = ["pl_orbper", "pl_rade", "pl_bmasse", "pl_eqt", "st_teff", "st_rad", "st_mass", "sy_dist"]
scaler = StandardScaler().fit(np.log10(train[features]))
A_train = scaler.transform(np.log10(train[features]))
A_test = scaler.transform(np.log10(test[features]))
yb_train, yb_test = train["habitable"], test["habitable"]
print("\nBaseline (always guess 'not habitable') accuracy:", round(1 - yb_test.mean(), 4))

def scores(pred):
    return (accuracy_score(yb_test, pred), recall_score(yb_test, pred, zero_division=0),
            precision_score(yb_test, pred, zero_division=0))

logit = LogisticRegression(max_iter=2000).fit(A_train, yb_train)
logit_bal = LogisticRegression(max_iter=2000, class_weight="balanced").fit(A_train, yb_train)
results = {}
for name, model in [("Logistic, default", logit), ("Logistic, balanced weights", logit_bal)]:
    p = model.predict(A_test)
    results[name] = (confusion_matrix(yb_test, p, labels=[0, 1]), scores(p))
    a, r, pr = results[name][1]
    print(f"\n{name}: accuracy {a:.4f}, recall {r:.3f}, precision {pr:.3f}")
    print(results[name][0])
print("\nLogistic regression coefficients (log-odds per 1 standard deviation), default model:")
for name, c in zip(features, logit.coef_[0]):
    print(f"  {name}: {c:.2f}  (odds multiply by {np.exp(c):.2f})")

cmap = LinearSegmentedColormap.from_list("panel_teal", [PANEL, TEAL])
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
for ax, (name, (cm, sc)) in zip(axes, results.items()):
    ax.imshow(cm, cmap=cmap)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Not habitable", "Habitable"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Not habitable", "Habitable"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title(f"{name} (accuracy {sc[0]*100:.1f}%)")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=13, color=TEXT)
plt.tight_layout(); plt.savefig("charts/logit_confusion_matrices.png", dpi=150); plt.close()

order = np.argsort(logit.coef_[0])
plt.figure(figsize=(7, 4.5))
plt.barh(np.array(features)[order], logit.coef_[0][order],
         color=[TEAL if c > 0 else RUST for c in logit.coef_[0][order]])
plt.axvline(0, color=DIM, linewidth=0.8)
plt.xlabel("Coefficient (change in log-odds per 1 standard deviation)")
plt.title("Logistic regression coefficients (default model)")
plt.tight_layout(); plt.savefig("charts/logit_coefficients.png", dpi=150); plt.close()

# ================= COMPARISON WITH NAIVE BAYES (Part 3) =================
# same recipe as naive_bayes.py: log10, scale to 0-1, equal prior
Xn_train = np.log10(train[features]); Xn_test = np.log10(test[features])
mm = MinMaxScaler().fit(Xn_train)
nb = MultinomialNB(fit_prior=False).fit(mm.transform(Xn_train), yb_train)
nb_pred = nb.predict(np.clip(mm.transform(Xn_test), 0, 1))
nb_cm = confusion_matrix(yb_test, nb_pred, labels=[0, 1])
nb_scores = scores(nb_pred)
print("\nNaive Bayes (equal prior):", [round(float(s), 3) for s in nb_scores], nb_cm.tolist())

models = [("Naive Bayes,\nequal prior", nb_scores), ("Logistic,\ndefault", results["Logistic, default"][1]),
          ("Logistic,\nbalanced", results["Logistic, balanced weights"][1])]
labels = ["Accuracy", "Recall", "Precision"]
x = np.arange(len(labels)); w = 0.26
fig, ax = plt.subplots(figsize=(8.5, 4.8))
for k, (mname, sc) in enumerate(models):
    bars = ax.bar(x + (k - 1) * w, sc, w, label=mname, color=[DIM, TEAL, GOLD][k])
    for b, v in zip(bars, sc):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.2f}", ha="center", fontsize=8, color=TEXT)
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylim(0, 1.12)
ax.set_title("Logistic regression vs Naive Bayes on the same 1,515 testing planets")
ax.legend(ncol=3, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.1))
plt.tight_layout(); plt.savefig("charts/logit_vs_nb.png", dpi=150); plt.close()
print("saved charts")
