"""
clean_and_visualize.py

Cleans the raw NASA Exoplanet Archive pull, merges in habitability labels
from the PHL Habitable Worlds Catalog and produces the visualizations and
two data preview images used on the Cleaning & Prep and EDA tabs. Can also be found in 
the .ipynb in the same git directory.

Inputs:
    exoplanets_raw.csv   from fetch_exoplanet_data.py
    hwc.csv              the "Full Catalog (CSV)" download from
                          phl.upr.edu/hwc/data
    hwc_table_all.csv    the 70-row shortlist table (Table 1 + Table 2)
                          from the same page, saved as CSV

Outputs:
    exoplanets_clean.csv       cleaned + merged dataset (21 columns)
    charts/01_missingness.png ... charts/12_top_esi_table.png
    charts/raw_preview.png, charts/clean_preview.png

Usage (Colab or local):
    pip install pandas matplotlib
    python clean_and_visualize.py
"""
import os
import re
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

os.makedirs("charts", exist_ok=True)

df = pd.read_csv("exoplanets_raw.csv")

# CLEANING
clean = df.copy()
# checking for duplicate planet names
print("Duplicate planet names:", clean["pl_name"].duplicated().sum())

# checking for negative or zero values in the numeric columns, which would be
# physically impossible for these measurements
numeric_cols = ["pl_orbper", "pl_rade", "pl_bmasse", "pl_eqt", "st_teff", "st_rad", "st_mass", "sy_dist"]
for col in numeric_cols:
    n_bad = (clean[col] <= 0).sum()
    print(f"{col}: {n_bad} values <= 0")

# checking how much is missing in each column
print("\nMissing values per column:")
print(clean.isna().sum())

# 157 planets sit above the ~13 Jupiter mass (4131 Earth mass) boundary,
# where "planet" starts overlapping with "brown dwarf" - flagged rather
# than dropped, since they are still confirmed entries in the archive
clean["is_borderline_massive"] = clean["pl_bmasse"] > 4131
print("\nBorderline massive planets flagged:", clean["is_borderline_massive"].sum())

#- Duplicate planet names and no negative/zero physical values were found in any numeric column on inspection, so nothing needed to be dropped on those grounds.
#- Missingness is left as NaN rather than imputed here, since the right way to fill it depends on which model uses that column later.
#- Flag planets above the ~13-Jupiter-mass (4131 Earth-mass)boundary, where "planet" starts overlapping with "brown dwarf" by common convention.
#- Kept (they are confirmed in the archive) but flagged rather than treated as ordinary planets.
#- As for the plots: JUST saving my images and charts in the back instead of plt.show() here.

# Discretizing planet size into standard exoplanet-science size classes.
def size_class(r):
    if pd.isna(r): return np.nan
    if r < 1.25: return "Earth-sized"
    if r < 2.0: return "Super-Earth"
    if r < 6.0: return "Sub-Neptune/Neptune"
    return "Giant"
clean["size_class"] = clean["pl_rade"].apply(size_class)

# Discretizing equilibrium temperature into a rough habitability zone.
# ~200-320 K is the loose range where liquid water is plausible.
def temp_zone(t):
    if pd.isna(t): return np.nan
    if t < 200: return "Too Cold"
    if t <= 320: return "Temperate"
    return "Too Hot"
clean["temp_zone"] = clean["pl_eqt"].apply(temp_zone)

# MERGING WITH PHL HABITABLE WORLDS CATALOG
hwc = pd.read_csv("hwc.csv")
hwc_cols = hwc[["P_NAME", "P_HABITABLE", "P_ESI", "P_TYPE",
                "P_HABZONE_OPT", "P_HABZONE_CON"]].rename(columns={"P_NAME": "pl_name"})

clean = clean.merge(hwc_cols, on="pl_name", how="left")
clean["hwc_habitable_label"] = clean["P_HABITABLE"].map(
    {0: "Not habitable", 1: "Conservative sample", 2: "Optimistic sample"})

clean.to_csv("exoplanets_clean.csv", index=False)
print("Cleaned + merged file saved:", clean.shape)
print(clean["size_class"].value_counts(dropna=False))
print(clean["temp_zone"].value_counts(dropna=False))
print(clean["hwc_habitable_label"].value_counts(dropna=False))

# TO PREVIEW TABLE IMAGES
def save_table_image(d, cols, fname, title):
    sample = d[cols].head(6)
    fig, ax = plt.subplots(figsize=(11, 2.2))
    ax.axis("off")
    ax.set_title(title, loc="left", fontsize=11)
    tbl = ax.table(cellText=sample.round(2).astype(str).values,
                    colLabels=cols, cellLoc="center", loc="center")
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(9)
    tbl.scale(1, 1.5)
    plt.savefig(f"charts/{fname}", dpi=150, bbox_inches="tight")
    plt.close()

save_table_image(df, ["pl_name", "hostname", "discoverymethod", "disc_year", "pl_rade", "pl_bmasse"],
                  "raw_preview.png", "Raw data (as pulled from the API)")
save_table_image(clean, ["pl_name", "pl_rade", "size_class", "pl_eqt", "temp_zone", "is_borderline_massive"],
                  "clean_preview.png", "Cleaned data (derived columns added)")

# VISUALIZATIONS

# 1. Missingness per column
miss = df.isna().mean().sort_values(ascending=False) * 100
plt.figure(figsize=(8, 4.5))
plt.barh(miss.index, miss.values)
plt.xlabel("% missing")
plt.title("Missing data by column")
plt.gca().invert_yaxis()
plt.tight_layout(); plt.savefig("charts/01_missingness.png", dpi=150); plt.close()

# 2. Discovery method counts (log scale)
dm = df["discoverymethod"].value_counts()
plt.figure(figsize=(8, 4.5))
plt.barh(dm.index[::-1], dm.values[::-1])
plt.xscale("log")
plt.xlabel("Number of confirmed planets (log scale)")
plt.title("Confirmed planets by discovery method")
plt.tight_layout(); plt.savefig("charts/02_discovery_method.png", dpi=150); plt.close()

# 3. Discoveries per year
yr = df["disc_year"].value_counts().sort_index()
plt.figure(figsize=(8, 4.5))
plt.plot(yr.index, yr.values, marker="o", markersize=3)
plt.xlabel("Year"); plt.ylabel("Planets confirmed")
plt.title("Confirmed exoplanet discoveries per year")
plt.tight_layout(); plt.savefig("charts/03_discoveries_per_year.png", dpi=150); plt.close()

# 4. Planet radius distribution (log)
plt.figure(figsize=(8, 4.5))
plt.hist(df["pl_rade"].dropna(), bins=40)
plt.xscale("log")
plt.xlabel("Planet radius (Earth radii, log scale)"); plt.ylabel("Count")
plt.title("Distribution of planet radius")
plt.tight_layout(); plt.savefig("charts/04_radius_distribution.png", dpi=150); plt.close()

# 5. Planet mass distribution (log)
plt.figure(figsize=(8, 4.5))
plt.hist(df["pl_bmasse"].dropna(), bins=40)
plt.xscale("log")
plt.xlabel("Planet mass (Earth masses, log scale)"); plt.ylabel("Count")
plt.title("Distribution of planet mass")
plt.tight_layout(); plt.savefig("charts/05_mass_distribution.png", dpi=150); plt.close()

# 6. Mass vs radius scatter
plt.figure(figsize=(7, 6))
plt.scatter(df["pl_rade"], df["pl_bmasse"], s=8, alpha=0.4)
plt.xscale("log"); plt.yscale("log")
plt.xlabel("Radius (Earth radii, log)"); plt.ylabel("Mass (Earth masses, log)")
plt.title("Planet mass vs. radius")
plt.tight_layout(); plt.savefig("charts/06_mass_vs_radius.png", dpi=150); plt.close()

# 7. Orbital period vs equilibrium temperature
plt.figure(figsize=(7, 6))
plt.scatter(df["pl_orbper"], df["pl_eqt"], s=8, alpha=0.4)
plt.xscale("log")
plt.xlabel("Orbital period (days, log scale)"); plt.ylabel("Equilibrium temperature (K)")
plt.title("Orbital period vs. equilibrium temperature")
plt.tight_layout(); plt.savefig("charts/07_period_vs_temp.png", dpi=150); plt.close()

# 8. Host star temperature histogram
plt.figure(figsize=(8, 4.5))
plt.hist(df["st_teff"].dropna(), bins=40)
plt.axvline(5778, linestyle="--", linewidth=1, color="black", label="Sun (5778 K)")
plt.xlabel("Host star effective temperature (K)"); plt.ylabel("Count")
plt.title("Host star temperature")
plt.legend()
plt.tight_layout(); plt.savefig("charts/08_star_temperature.png", dpi=150); plt.close()

# 9. Size class breakdown
sc = clean["size_class"].value_counts()
plt.figure(figsize=(7, 4.5))
plt.bar(sc.index, sc.values)
plt.ylabel("Count")
plt.title("Planets by size class")
plt.tight_layout(); plt.savefig("charts/09_size_class.png", dpi=150); plt.close()

# 10. Temperature zone breakdown
tz = clean["temp_zone"].value_counts().reindex(["Too Cold", "Temperate", "Too Hot"])
plt.figure(figsize=(7, 4.5))
plt.bar(tz.index, tz.values)
plt.ylabel("Count")
plt.title("Planets by equilibrium-temperature zone")
plt.tight_layout(); plt.savefig("charts/10_temp_zone.png", dpi=150); plt.close()

# 11. Official HWC habitability classification
counts = clean["hwc_habitable_label"].value_counts().reindex(
    ["Not habitable", "Conservative sample", "Optimistic sample"]
)
plt.figure(figsize=(7, 4.5))
plt.bar(counts.index, counts.values)
plt.ylabel("Count")
plt.title("Official Habitable Worlds Catalog classification")
for i, v in enumerate(counts.values):
    plt.text(i, v + 40, str(int(v)), ha="center", fontsize=9)
plt.tight_layout(); plt.savefig("charts/11_hwc_habitability.png", dpi=150); plt.close()

# 12. Top 10 most Earth-like worlds by ESI, from the shortlist table
short = pd.read_csv("hwc_table_all.csv")
short.columns = [re.sub(r"<[^>]+>", "", c) for c in short.columns]
short = short.sort_values("ESI", ascending=False).head(10)
short_display = short[["Name", "Type", "ESI"]].round({"ESI": 3})

fig, ax = plt.subplots(figsize=(8, 3.2))
ax.axis("off")
ax.set_title("Top 10 potentially habitable worlds, by Earth Similarity Index",
             loc="left", fontsize=11)
tbl = ax.table(cellText=short_display.values, colLabels=["Name", "Type", "ESI"],
                cellLoc="center", loc="center")
tbl.auto_set_font_size(False); tbl.set_fontsize(9); tbl.scale(1, 1.5)
plt.savefig("charts/12_top_esi_table.png", dpi=150, bbox_inches="tight")
plt.close()

print("All charts saved to charts/")
# All charts saved to charts/ means the charts are saved in the Colab backend as opposed to explicitly being pulled up on the main notebook. 
