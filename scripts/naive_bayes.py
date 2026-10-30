# Module 3: Naive Bayes (multinomial) on the labeled exoplanet data.
# Input:  train_set.csv, test_set.csv (from prep_train_test.py)
# Output: confusion matrix chart in charts/

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import MinMaxScaler
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

# multinomial NB treats each feature like a count, so every value has to be zero or
# positive. The measurements span several orders of magnitude, so take log10 first,
# then squeeze each column into 0 to 1. The scaler is fit on the training set only,
# and test values that fall outside the training range are clipped to 0 or 1.
X_train = np.log10(train[features])
X_test = np.log10(test[features])
scaler = MinMaxScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = np.clip(scaler.transform(X_test), 0, 1)
y_train, y_test = train["habitable"], test["habitable"]

def report(name, model):
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    cm = confusion_matrix(y_test, pred, labels=[0, 1])
    prec = precision_score(y_test, pred, zero_division=0)
    rec = recall_score(y_test, pred, zero_division=0)
    print(f"\n{name}")
    print("accuracy:", round(acc, 4), "precision:", round(prec, 4), "recall:", round(rec, 4))
    print(cm)
    return cm, acc

print("Baseline (always guess 'not habitable') accuracy:", round(1 - y_test.mean(), 4))

# model 1: default, the class prior is learned from the training set
nb_default = MultinomialNB().fit(X_train, y_train)
cm1, acc1 = report("MultinomialNB, learned prior", nb_default)

# model 2: same model but both classes get an equal prior
nb_equal = MultinomialNB(fit_prior=False).fit(X_train, y_train)
cm2, acc2 = report("MultinomialNB, equal prior", nb_equal)

cmap = LinearSegmentedColormap.from_list("panel_teal", [PANEL, TEAL])
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
for ax, cm, acc, title in [(axes[0], cm1, acc1, "Learned prior"), (axes[1], cm2, acc2, "Equal prior")]:
    ax.imshow(cm, cmap=cmap)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Not habitable", "Habitable"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Not habitable", "Habitable"])
    ax.set_xlabel("Predicted"); ax.set_ylabel("Actual")
    ax.set_title(f"{title} (accuracy {acc*100:.1f}%)")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=13, color=TEXT)
plt.tight_layout()
plt.savefig("charts/nb_confusion_matrices.png", dpi=150)
plt.close()
print("saved charts/nb_confusion_matrices.png")
