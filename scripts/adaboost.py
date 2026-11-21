# Module 4: AdaBoost on the labeled exoplanet data.
# Input:  train_set.csv, test_set.csv (from prep_train_test.py), exoplanets_clean.csv
# Output: AdaBoost charts in charts/

import os
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_score, recall_score
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

# scikit-learn prints a harmless feature-name warning from inside AdaBoost, hidden to keep the output readable
warnings.filterwarnings("ignore", message="X does not have valid feature names")

os.makedirs("charts", exist_ok=True)
train = pd.read_csv("train_set.csv")
test = pd.read_csv("test_set.csv")
clean = pd.read_csv("exoplanets_clean.csv")
numeric = ["pl_orbper", "pl_rade", "pl_bmasse", "pl_eqt", "st_teff", "st_rad", "st_mass", "sy_dist"]

# ONE-HOT ENCODING
# scikit-learn's AdaBoost needs numbers only. The eight measurements are already numeric, but how a planet was discovered (transit, radial velocity, ...) is a category. Each method becomes its own 0/1 column.
# Columns are built from the training set, and the testing set is lined up to the same columns, so a method that only appears in the testing set is ignored.
method = clean.set_index("pl_name")["discoverymethod"]
train["discoverymethod"] = train["pl_name"].map(method)
test["discoverymethod"] = test["pl_name"].map(method)
dummies_train = pd.get_dummies(train["discoverymethod"], prefix="method").astype(int)
dummies_test = pd.get_dummies(test["discoverymethod"], prefix="method").astype(int)
dummies_test = dummies_test.reindex(columns=dummies_train.columns, fill_value=0)
print("Discovery methods in the training set:")
print(train["discoverymethod"].value_counts())

X_train = pd.concat([train[numeric], dummies_train], axis=1)
X_test = pd.concat([test[numeric], dummies_test], axis=1)
y_train, y_test = train["habitable"], test["habitable"]
print("Predictor columns:", X_train.shape[1], "(8 measurements +", dummies_train.shape[1], "one-hot columns)")

# small preview image of the encoding step: one example planet per discovery method
show = train.groupby("discoverymethod").head(1).head(6)
cols = ["pl_name", "discoverymethod"] + [c for c in ["method_Transit", "method_Radial Velocity",
                                                      "method_Microlensing", "method_Imaging"] if c in dummies_train.columns]
preview = pd.concat([show[["pl_name", "discoverymethod"]], dummies_train.loc[show.index]], axis=1)[cols]
fig, ax = plt.subplots(figsize=(11, 2.3))
ax.axis("off")
ax.set_title("One-hot encoding: discovery method becomes 0/1 columns", loc="left", color=GOLD, fontsize=12, pad=14)
tbl = ax.table(cellText=preview.astype(str).values, colLabels=preview.columns, cellLoc="center", loc="center")
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.5)
for (row, col), cell in tbl.get_celld().items():
    cell.set_edgecolor(LINE)
    if row == 0:
        cell.set_facecolor(PANEL); cell.set_text_props(color=GOLD, weight="bold")
    else:
        cell.set_facecolor(BG); cell.set_text_props(color=TEXT)
plt.savefig("charts/ada_onehot_preview.png", dpi=150, bbox_inches="tight")
plt.close()

def make_model(n, lr):
    # a decision stump is a tree with a single split (max_depth=1)
    return AdaBoostClassifier(estimator=DecisionTreeClassifier(max_depth=1),
                              n_estimators=n, learning_rate=lr, random_state=42)

# TUNING
# the testing set is not touched here. Rounds and learning rate are chosen with 5-fold cross-validation inside the training set: each fold is held out as validation data once.
# staged_predict gives the prediction after every round, so one fit covers all round counts.
rounds = 200
learning_rates = [0.01, 0.1, 0.5, 1.0]
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
acc_curves = {lr: np.zeros(rounds) for lr in learning_rates}
f1_curves = {lr: np.zeros(rounds) for lr in learning_rates}
for lr in learning_rates:
    for fit_idx, val_idx in cv.split(X_train, y_train):
        m = make_model(rounds, lr).fit(X_train.iloc[fit_idx], y_train.iloc[fit_idx])
        for r, p in enumerate(m.staged_predict(X_train.iloc[val_idx])):
            acc_curves[lr][r] += accuracy_score(y_train.iloc[val_idx], p) / 5
            f1_curves[lr][r] += f1_score(y_train.iloc[val_idx], p, zero_division=0) / 5

# accuracy barely moves (98.7% of planets are not habitable), so the choice uses F1 on the habitable class, which does react to finding the rare planets
best_lr, best_n, best_f1 = None, None, -1
for lr in learning_rates:
    r = int(np.argmax(f1_curves[lr]))
    if f1_curves[lr][r] > best_f1:
        best_lr, best_n, best_f1 = lr, r + 1, f1_curves[lr][r]
majority = 1 - y_train.mean()
print("\nBest by validation F1: learning rate", best_lr, "rounds", best_n, "F1", round(best_f1, 3))
print("validation accuracy at that setting:", round(acc_curves[best_lr][best_n - 1], 4), "(always-no accuracy:", round(majority, 4), ")")

palette = [DIM, TEAL, GOLD, RUST]
fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))
for lr, col in zip(learning_rates, palette):
    axes[0].plot(range(1, rounds + 1), acc_curves[lr], color=col, label=f"learning rate {lr}")
    axes[1].plot(range(1, rounds + 1), f1_curves[lr], color=col, label=f"learning rate {lr}")
axes[0].axhline(majority, color=TEXT, linestyle="--", linewidth=0.8, label="always guess not habitable")
axes[0].set_xlabel("Boosting rounds"); axes[0].set_ylabel("Validation accuracy")
axes[0].set_title("Validation accuracy by round"); axes[0].legend(fontsize=8, loc="upper left")
axes[1].set_xlabel("Boosting rounds"); axes[1].set_ylabel("Validation F1 (habitable class)")
axes[1].set_title("Validation F1 by round")
plt.tight_layout(); plt.savefig("charts/ada_tuning.png", dpi=150); plt.close()

# FINAL MODELS ON THE TESTING SET
def evaluate(name, model, Xtr, Xte):
    model.fit(Xtr, y_train)
    p = model.predict(Xte)
    acc = accuracy_score(y_test, p); rec = recall_score(y_test, p, zero_division=0)
    prec = precision_score(y_test, p, zero_division=0); cm = confusion_matrix(y_test, p, labels=[0, 1])
    print(f"\n{name}: accuracy {acc:.4f}, recall {rec:.3f}, precision {prec:.3f}")
    print(cm.tolist())
    return model, cm, (acc, rec, prec)

print("\nBaseline (always guess 'not habitable') accuracy:", round(1 - y_test.mean(), 4))
untuned, cm_untuned, sc_untuned = evaluate("AdaBoost, default settings (50 rounds, learning rate 1.0)", make_model(50, 1.0), X_train, X_test)
final, cm_final, sc_final = evaluate(f"AdaBoost, tuned ({best_n} rounds, learning rate {best_lr})", make_model(best_n, best_lr), X_train, X_test)
_, cm_num, sc_num = evaluate("AdaBoost, tuned settings, measurements only (no one-hot columns)",
                              make_model(best_n, best_lr), X_train[numeric], X_test[numeric])
# the Part 3 decision tree (Tree 1: Gini, depth 3) on the same split
tree = DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)
_, cm_tree, sc_tree = evaluate("Decision tree from Part 3 (Tree 1: Gini, depth 3)", tree, X_train[numeric], X_test[numeric])

cmap = LinearSegmentedColormap.from_list("panel_teal", [PANEL, TEAL])
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
for ax, (title, cm, sc) in zip(axes, [("AdaBoost, default settings", cm_untuned, sc_untuned),
                                       (f"AdaBoost, tuned ({best_n} rounds)", cm_final, sc_final)]):
    ax.imshow(cm, cmap=cmap)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Not habitable", "Habitable"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Not habitable", "Habitable"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title(f"{title} (accuracy {sc[0]*100:.1f}%)", fontsize=11)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=13, color=TEXT)
plt.tight_layout(); plt.savefig("charts/ada_confusion_matrices.png", dpi=150); plt.close()

# alpha (the weight of each stump's vote) for the first rounds of the tuned model
alphas = final.estimator_weights_[:30]
errors = final.estimator_errors_[:30]
print("\nFirst five stump errors:", np.round(errors[:5], 3).tolist())
print("First five alphas:", np.round(alphas[:5], 3).tolist())
print("check, learning rate * ln((1-error)/error) for the first stump:",
      round(best_lr * np.log((1 - errors[0]) / errors[0]), 3))
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.bar(range(1, len(alphas) + 1), alphas, color=TEAL)
ax.set_xlabel("Boosting round"); ax.set_ylabel("Alpha (weight of the stump's vote)")
ax.set_title("Alpha of each stump in the tuned model (first 30 rounds)")
plt.tight_layout(); plt.savefig("charts/ada_alpha_by_round.png", dpi=150); plt.close()

# which predictors the tuned model uses most
imp = pd.Series(final.feature_importances_, index=X_train.columns).sort_values().tail(8)
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(imp.index, imp.values, color=TEAL)
ax.set_xlabel("Feature importance")
ax.set_title("What the tuned AdaBoost model relies on")
plt.tight_layout(); plt.savefig("charts/ada_feature_importance.png", dpi=150); plt.close()
print("\nTop importances:", imp.round(3).to_dict())

# comparison with the Part 3 tree
labels = ["Accuracy", "Recall", "Precision"]
x = np.arange(3); w = 0.26
fig, ax = plt.subplots(figsize=(8.5, 4.8))
for k, (mname, sc) in enumerate([("Decision tree (Part 3)", sc_tree), ("AdaBoost, default", sc_untuned), (f"AdaBoost, tuned", sc_final)]):
    bars = ax.bar(x + (k - 1) * w, sc, w, label=mname, color=[DIM, TEAL, GOLD][k])
    for b, v in zip(bars, sc):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.015, f"{v:.2f}", ha="center", fontsize=8, color=TEXT)
ax.set_xticks(x); ax.set_xticklabels(labels); ax.set_ylim(0, 1.12)
ax.set_title("AdaBoost vs the Part 3 decision tree on the same 1,515 testing planets")
ax.legend(ncol=3, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.1))
plt.tight_layout(); plt.savefig("charts/ada_vs_tree.png", dpi=150); plt.close()
print("saved charts")
