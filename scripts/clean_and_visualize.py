"""
clean_and_visualize.py

Cleans the raw NASA Exoplanet Archive pull, merges in habitability labels
from the PHL Habitable Worlds Catalog, and produces the 11 visualizations
and two data-preview images used on the Cleaning & Prep and EDA tabs.

Inputs (place these in the same folder as this script, or update the
paths below):
    exoplanets_raw.csv   from fetch_exoplanet_data.py
    hwc.csv              the "Full Catalog (CSV)" download from
                          phl.upr.edu/hwc/data
    hwc_table_all.csv    the 70-row shortlist table (Table 1 + Table 2)
                          from the same page, saved as CSV

Outputs:
    exoplanets_clean.csv       cleaned + merged dataset (20 columns)
    charts/01_missingness.png ... charts/12_top_esi_table.png
    charts/raw_preview.png, charts/clean_preview.png

Usage (Colab or local):
    pip install pandas matplotlib   # already installed in Colab by default
    python clean_and_visualize.py
"""
import os
import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---- theme, matches the site's CSS variables in style.css ----
BG, PANEL, LINE = "#0b0f1a", "#131a2b", "#232d47"
TEXT, DIM = "#e9e7e1", "#9aa3bd"
GOLD, TEAL, RUST = "#e8a33d", "#4a95a0", "#c1502e"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": TEXT, "axes.labelcolor": TEXT, "axes.edgecolor": LINE,
    "xtick.color": DIM, "ytick.color": DIM, "grid.color": LINE,
    "font.size": 11, "axes.titlesize": 13, "axes.titlecolor": TEXT,
})

os.makedirs("charts", exist_ok=True)

df = pd.read_csv("exoplanets_raw.csv")

# ================= CLEANING =================
clean = df.copy()

# No duplicate planet names and no negative/zero physical values were found
# in any numeric column on inspection, so nothing needed to be dropped on
# those grounds. Missingness is left as NaN rather than imputed here, since
# the right way to fill it depends on which model uses that column later.

# Flag planets above the ~13-Jupiter-mass (4131 Earth-mass) boundary, where
# "planet" starts overlapping with "brown dwarf" by common convention.
# Kept (they are confirmed in the archive) but flagged rather than treated
# as ordinary planets silently.
clean["is_borderline_massive"] = clean["pl_bmasse"] > 4131

# Discretize planet size into standard exoplanet-science size classes.
def size_class(r):
    if pd.isna(r): return np.nan
    if r < 1.25: return "Earth-sized"
    if r < 2.0: return "Super-Earth"
    if r < 6.0: return "Sub-Neptune/Neptune"
    return "Giant"
clean["size_class"] = clean["pl_rade"].apply(size_class)

# Discretize equilibrium temperature into a rough habitability zone.
# ~200-320 K is the loose range where liquid water is plausible.
def temp_zone(t):
    if pd.isna(t): return np.nan
    if t < 200: return "Too Cold"
    if t <= 320: return "Temperate"
    return "Too Hot"
clean["temp_zone"] = clean["pl_eqt"].apply(temp_zone)

# ================= MERGE WITH PHL HABITABLE WORLDS CATALOG =================
hwc = pd.read_csv("hwc.csv")
hwc_cols = hwc[["P_NAME", "P_HABITABLE", "P_ESI", "P_TYPE",
                "P_HABZONE_OPT", "P_HABZONE_CON"]].rename(columns={"P_NAME": "pl_name"})

clean = clean.merge(hwc_cols, on="pl_name", how="left")
clean["hwc_habitable_label"] = clean["P_HABITABLE"].map(
    {0: "Not habitable", 1: "Conservative sample", 2: "Optimistic sample"}
)

clean.to_csv("exoplanets_clean.csv", index=False)
print("Cleaned + merged file saved:", clean.shape)
print(clean["size_class"].value_counts(dropna=False))
print(clean["temp_zone"].value_counts(dropna=False))
print(clean["hwc_habitable_label"].value_counts(dropna=False))

# ================= PREVIEW TABLE IMAGES =================
def save_table_image(d, cols, fname, title):
    sample = d[cols].head(6)
    fig, ax = plt.subplots(figsize=(11, 2.2))
    ax.axis("off")
    ax.set_title(title, loc="left", color=GOLD, fontsize=12, pad=14)
    tbl = ax.table(cellText=sample.round(2).astype(str).values,
                    colLabels=cols, cellLoc="center", loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.6)
    for (row, col), cell in tbl.get_celld().items():
        cell.set_edgecolor(LINE)
        if row == 0:
            cell.set_facecolor(PANEL)
            cell.set_text_props(color=GOLD, weight="bold")
        else:
            cell.set_facecolor(BG)
            cell.set_text_props(color=TEXT)
    plt.savefig(f"charts/{fname}", dpi=150, bbox_inches="tight")
    plt.close()

save_table_image(df, ["pl_name", "hostname", "discoverymethod", "disc_year", "pl_rade", "pl_bmasse"],
                  "raw_preview.png", "Raw data (as pulled from the API)")
save_table_image(clean, ["pl_name", "pl_rade", "size_class", "pl_eqt", "temp_zone", "is_borderline_massive"],
                  "clean_preview.png", "Cleaned data (derived columns added)")

# ================= VISUALIZATIONS =================

# 1. Missingness per column
miss = df.isna().mean().sort_values(ascending=False) * 100
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(miss.index, miss.values, color=TEAL)
ax.set_xlabel("% missing")
ax.set_title("Missing data by column")
ax.invert_yaxis()
plt.tight_layout(); plt.savefig("charts/01_missingness.png", dpi=150); plt.close()

# 2. Discovery method counts (log scale)
dm = df["discoverymethod"].value_counts()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(dm.index[::-1], dm.values[::-1], color=GOLD)
ax.set_xscale("log")
ax.set_xlabel("Number of confirmed planets (log scale)")
ax.set_title("Confirmed planets by discovery method")
plt.tight_layout(); plt.savefig("charts/02_discovery_method.png", dpi=150); plt.close()

# 3. Discoveries per year
yr = df["disc_year"].value_counts().sort_index()
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(yr.index, yr.values, color=RUST, linewidth=2)
ax.fill_between(yr.index, yr.values, color=RUST, alpha=0.15)
ax.set_xlabel("Year"); ax.set_ylabel("Planets confirmed")
ax.set_title("Confirmed exoplanet discoveries per year")
plt.tight_layout(); plt.savefig("charts/03_discoveries_per_year.png", dpi=150); plt.close()

# 4. Planet radius distribution (log)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(df["pl_rade"].dropna(), bins=40, color=TEAL)
ax.set_xscale("log")
ax.set_xlabel("Planet radius (Earth radii, log scale)"); ax.set_ylabel("Count")
ax.set_title("Distribution of planet radius")
plt.tight_layout(); plt.savefig("charts/04_radius_distribution.png", dpi=150); plt.close()

# 5. Planet mass distribution (log)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(df["pl_bmasse"].dropna(), bins=40, color=GOLD)
ax.set_xscale("log")
ax.set_xlabel("Planet mass (Earth masses, log scale)"); ax.set_ylabel("Count")
ax.set_title("Distribution of planet mass")
plt.tight_layout(); plt.savefig("charts/05_mass_distribution.png", dpi=150); plt.close()

# 6. Mass vs radius scatter
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(df["pl_rade"], df["pl_bmasse"], s=8, alpha=0.4, color=TEAL)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Radius (Earth radii, log)"); ax.set_ylabel("Mass (Earth masses, log)")
ax.set_title("Planet mass vs. radius")
plt.tight_layout(); plt.savefig("charts/06_mass_vs_radius.png", dpi=150); plt.close()

# 7. Orbital period vs equilibrium temperature
fig, ax = plt.subplots(figsize=(7, 6))
ax.scatter(df["pl_orbper"], df["pl_eqt"], s=8, alpha=0.4, color=RUST)
ax.set_xscale("log")
ax.set_xlabel("Orbital period (days, log scale)"); ax.set_ylabel("Equilibrium temperature (K)")
ax.set_title("Orbital period vs. equilibrium temperature")
plt.tight_layout(); plt.savefig("charts/07_period_vs_temp.png", dpi=150); plt.close()

# 8. Host star temperature histogram
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(df["st_teff"].dropna(), bins=40, color=GOLD)
ax.axvline(5778, color=TEXT, linestyle="--", linewidth=1, label="Sun (5778 K)")
ax.set_xlabel("Host star effective temperature (K)"); ax.set_ylabel("Count")
ax.set_title("Host star temperature")
ax.legend()
plt.tight_layout(); plt.savefig("charts/08_star_temperature.png", dpi=150); plt.close()

# 9. Size class breakdown
sc = clean["size_class"].value_counts()
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(sc.index, sc.values, color=[TEAL, GOLD, RUST, DIM])
ax.set_ylabel("Count")
ax.set_title("Planets by size class")
plt.tight_layout(); plt.savefig("charts/09_size_class.png", dpi=150); plt.close()

# 10. Temperature zone breakdown
tz = clean["temp_zone"].value_counts().reindex(["Too Cold", "Temperate", "Too Hot"])
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(tz.index, tz.values, color=[TEAL, GOLD, RUST])
ax.set_ylabel("Count")
ax.set_title("Planets by equilibrium-temperature zone")
plt.tight_layout(); plt.savefig("charts/10_temp_zone.png", dpi=150); plt.close()

# 11. Official HWC habitability classification
counts = clean["hwc_habitable_label"].value_counts().reindex(
    ["Not habitable", "Conservative sample", "Optimistic sample"]
)
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(counts.index, counts.values, color=[DIM, TEAL, GOLD])
ax.set_ylabel("Count")
ax.set_title("Official Habitable Worlds Catalog classification")
for i, v in enumerate(counts.values):
    ax.text(i, v + 40, str(int(v)), ha="center", color=TEXT, fontsize=10)
plt.tight_layout(); plt.savefig("charts/11_hwc_habitability.png", dpi=150); plt.close()

# 12. Top 10 most Earth-like worlds by ESI, from the shortlist table
short = pd.read_csv("hwc_table_all.csv")
short.columns = [re.sub(r"<[^>]+>", "", c) for c in short.columns]
short = short.sort_values("ESI", ascending=False).head(10)
short_display = short[["Name", "Type", "ESI"]].round({"ESI": 3})

fig, ax = plt.subplots(figsize=(8, 3.2))
ax.axis("off")
ax.set_title("Top 10 potentially habitable worlds, by Earth Similarity Index",
             loc="left", color=GOLD, fontsize=12, pad=14)
tbl = ax.table(cellText=short_display.values, colLabels=["Name", "Type", "ESI"],
                cellLoc="center", loc="center")
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.5)
for (row, col), cell in tbl.get_celld().items():
    cell.set_edgecolor(LINE)
    if row == 0:
        cell.set_facecolor(PANEL); cell.set_text_props(color=GOLD, weight="bold")
    else:
        cell.set_facecolor(BG); cell.set_text_props(color=TEXT)
plt.savefig("charts/12_top_esi_table.png", dpi=150, bbox_inches="tight")
plt.close()

print("All charts saved to charts/")
