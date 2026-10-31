# Module 3 data prep: building the labeled dataset and split it into training and testing sets.
# Input: exoplanets_clean.csv (from clean_and_visualize.py)
# Output: labeled_sample.csv, train_set.csv, test_set.csv, plus small preview images in charts/

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# keeping the dark bg going :)
BG, PANEL, LINE = "#0b0f1a", "#131a2b", "#232d47"
TEXT, DIM = "#e9e7e1", "#9aa3bd"
GOLD, TEAL, RUST = "#e8a33d", "#4a95a0", "#c1502e"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TEXT, "axes.labelcolor": TEXT, "axes.edgecolor": LINE,
    "xtick.color": DIM, "ytick.color": DIM, "font.size": 11,
    "axes.titlesize": 13, "axes.titlecolor": TEXT})

os.makedirs("charts", exist_ok=True)
df = pd.read_csv("exoplanets_clean.csv")

features = ["pl_orbper", "pl_rade", "pl_bmasse", "pl_eqt", "st_teff", "st_rad", "st_mass", "sy_dist"]

# supervised methods need a label. The label here comes from the PHL Habitable Worlds
# Catalog: P_HABITABLE is 0 (not habitable), 1 (conservative sample) or 2 (optimistic sample).
# Collapsed into one yes/no label: habitable = 1 if the catalog lists the planet in either sample.
# Only planets the catalog has assessed (P_HABITABLE present) and with all 8 measurements are kept.
labeled = df.dropna(subset=features + ["P_HABITABLE"]).copy()
labeled["habitable"] = (labeled["P_HABITABLE"] > 0).astype(int)
labeled = labeled[["pl_name"] + features + ["habitable"]].reset_index(drop=True)
print("Labeled rows:", len(labeled))
print(labeled["habitable"].value_counts())

# 70/30 split. stratify keeps the same share of habitable planets in both sets,
# which matters because there are so few of them. random_state makes it repeatable.
train, test = train_test_split(labeled, test_size=0.30, random_state=42, stratify=labeled["habitable"])

# the two sets must not share a single planet, otherwise the test score would be meaningless
overlap = set(train["pl_name"]) & set(test["pl_name"])
print("Planets in both sets:", len(overlap))
assert len(overlap) == 0

labeled.to_csv("labeled_sample.csv", index=False)
train.to_csv("train_set.csv", index=False)
test.to_csv("test_set.csv", index=False)
print("Train:", len(train), "habitable:", train["habitable"].sum())
print("Test:", len(test), "habitable:", test["habitable"].sum())

def save_table_image(d, fname, title):
    sample = d.head(6).copy()
    for c in features:
        sample[c] = sample[c].map(lambda v: f"{v:.3g}")
    fig, ax = plt.subplots(figsize=(11, 2.3))
    ax.axis("off")
    ax.set_title(title, loc="left", color=GOLD, fontsize=12, pad=14)
    tbl = ax.table(cellText=sample.values, colLabels=sample.columns, cellLoc="center", loc="center")
    tbl.auto_set_font_size(False); tbl.set_fontsize(8); tbl.scale(1, 1.5)
    for (row, col), cell in tbl.get_celld().items():
        cell.set_edgecolor(LINE)
        if row == 0:
            cell.set_facecolor(PANEL); cell.set_text_props(color=GOLD, weight="bold")
        else:
            cell.set_facecolor(BG); cell.set_text_props(color=TEXT)
    plt.savefig(f"charts/{fname}", dpi=150, bbox_inches="tight")
    plt.close()

save_table_image(labeled, "labeled_preview.png", f"Labeled sample ({len(labeled)} planets, {labeled['habitable'].sum()} habitable)")
save_table_image(train, "train_preview.png", f"Training set ({len(train)} planets, {train['habitable'].sum()} habitable)")
save_table_image(test, "test_preview.png", f"Testing set ({len(test)} planets, {test['habitable'].sum()} habitable)")
print("done")
