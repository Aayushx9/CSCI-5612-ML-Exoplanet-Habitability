# Module 3: Decision Trees on the labeled exoplanet data.
# Input:  train_set.csv, test_set.csv (from prep_train_test.py)
# Output: three tree diagrams, confusion matrices, and a feature importance chart in charts/

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
from matplotlib.colors import LinearSegmentedColormap

BG, PANEL, LINE = "#0b0f1a", "#131a2b", "#232d47"
TEXT, DIM = "#e9e7e1", "#9aa3bd"
GOLD, TEAL, RUST = "#e8a33d", "#4a95a0", "#c1502e"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TEXT, "axes.labelcolor": TEXT, "axes.edgecolor": LINE,
    "xtick.color": DIM, "ytick.color": DIM, "font.size": 11,
    "axes.titlesize": 12, "axes.titlecolor": TEXT})

os.makedirs("charts", exist_ok=True)
train = pd.read_csv("train_set.csv")
test = pd.read_csv("test_set.csv")
features = ["pl_orbper", "pl_rade", "pl_bmasse", "pl_eqt", "st_teff", "st_rad", "st_mass", "sy_dist"]

# trees split on thresholds, so no scaling or log transform is needed
X_train, y_train = train[features], train["habitable"]
X_test, y_test = test[features], test["habitable"]

print("Baseline (always guess 'not habitable') accuracy:", round(1 - y_test.mean(), 4))

# three different trees: two split rules (gini, entropy) and a third that weights the rare class more
specs = [
    ("Tree 1: Gini, max depth 3", DecisionTreeClassifier(criterion="gini", max_depth=3, random_state=42)),
    ("Tree 2: Entropy, max depth 3", DecisionTreeClassifier(criterion="entropy", max_depth=3, random_state=42)),
    ("Tree 3: Gini, max depth 4, balanced class weights",
     DecisionTreeClassifier(criterion="gini", max_depth=4, class_weight="balanced", random_state=42)),
]

def theme_tree(artists):
    # boxes: dark panel; leaves that predict "habitable" are outlined in gold.
    # plot_tree also returns the small True/False edge labels, which have no box,
    # so each artist is judged by its own text instead of its position in the list.
    for a in artists:
        a.set_color(TEXT)
        if a.arrow_patch is not None:
            a.arrow_patch.set_color(DIM)
        patch = a.get_bbox_patch()
        if patch is None:
            continue
        txt = a.get_text()
        is_leaf = "<=" not in txt.split("\n")[0]
        predicts_hab = "class = habitable" in txt
        patch.set_facecolor(PANEL)
        patch.set_edgecolor(GOLD if (is_leaf and predicts_hab) else LINE)
        patch.set_linewidth(2 if (is_leaf and predicts_hab) else 1)

results = []
for i, (name, model) in enumerate(specs, start=1):
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred, labels=[0, 1])
    prec = precision_score(y_test, pred, zero_division=0)
    rec = recall_score(y_test, pred, zero_division=0)
    results.append((name, cm, acc))
    print(f"\n{name}")
    print("accuracy:", round(acc, 4), "precision:", round(prec, 4), "recall:", round(rec, 4))
    print(cm)

    fig, ax = plt.subplots(figsize=(14, 7))
    artists = plot_tree(model, feature_names=features, class_names=["not habitable", "habitable"],
                        filled=False, rounded=True, fontsize=8, ax=ax, impurity=True)
    theme_tree(artists)
    ax.set_title(name)
    plt.tight_layout()
    plt.savefig(f"charts/dt_tree_{i}.png", dpi=150)
    plt.close()

# confusion matrices for all three trees side by side
cmap = LinearSegmentedColormap.from_list("panel_teal", [PANEL, TEAL])
fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
for ax, (name, cm, acc) in zip(axes, results):
    ax.imshow(cm, cmap=cmap)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Not hab.", "Habitable"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Not hab.", "Habitable"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title(f"{name.split(':')[0]} (accuracy {acc*100:.1f}%)", fontsize=11)
    for r in range(2):
        for c in range(2):
            ax.text(c, r, cm[r, c], ha="center", va="center", fontsize=13, color=TEXT)
plt.tight_layout()
plt.savefig("charts/dt_confusion_matrices.png", dpi=150)
plt.close()

# which measurements the first tree actually used
imp = pd.Series(specs[0][1].feature_importances_, index=features).sort_values()
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(imp.index, imp.values, color=TEAL)
ax.set_xlabel("Feature importance")
ax.set_title("Which measurements Tree 1 relies on")
plt.tight_layout()
plt.savefig("charts/dt_feature_importance.png", dpi=150)
plt.close()
print("\nsaved charts")
