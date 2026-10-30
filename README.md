# Exoplanet Discovery & Habitability

A semester-long data science project built module by module: gathering, cleaning, exploring, modeling, and communicating results using the public record of confirmed exoplanets. The central question: which of the thousands of confirmed exoplanets look most like they could support life, and what measurable properties set those planets apart from the rest?

**Live site:** https://aayushx9.github.io/CSCI-5612-ML-Exoplanet-Habitability/

## Progress

| Tab | Module | Status |
|---|---|---|
| Introduction, Data Gathering, Cleaning & Prep, EDA | 1 | Complete |
| Clustering, PCA | 2 | Complete |
| Naive Bayes, Decision Trees | 3 | Complete |
| SVMs | 4 | Not started |
| Regression, NN, Conclusions | 5 | Not started |

## Project structure

```
index.html              Introduction (landing page) with the central question
data_gathering.html     Sources, API details, raw data
cleaning_prep.html      Before/after cleaning steps
eda.html                Distributions and relationships
clustering.html         K-means and hierarchical clustering
pca.html                Principal component analysis
naivebayes.html         Multinomial Naive Bayes
dectrees.html           Decision trees
svms.html               Module 4
regression.html         Module 5
nn.html                 Module 5
conclusions.html        Module 5
about_references.html   Bio, cited sources, code link
style.css               Shared site styling
build.py                Regenerates the HTML pages from templates
assets/                 Images (eda/, m2/, m3/) and the transit diagram
data/                   CSV files (raw, cleaned, labeled, train, test, PHL catalog)
scripts/                Python code for every analysis step
```

## Data sources

**Primary, via API:** [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/), Table Access Protocol (TAP) service, `pscomppars` table. No API key required. The endpoint and an example request are on the Data Gathering tab.

**Secondary, downloaded:** [PHL Habitable Worlds Catalog](https://phl.upr.edu/hwc/data), maintained by the Planetary Habitability Laboratory at the University of Puerto Rico at Arecibo. It supplies the habitability labels and Earth Similarity Index used from the cleaning step onward.

## Licensing and attribution

NASA Exoplanet Archive data are freely available. Standard acknowledgment: this research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.

PHL Habitable Worlds Catalog content is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported](https://phl.upr.edu/phl-website-content-license). Credit: The Planetary Habitability Laboratory @ UPR Arecibo (phl.upr.edu). `data/hwc_full.csv` is a direct copy of PHL data, and every file derived from it (`exoplanets_clean.csv`, `labeled_sample.csv`, `train_set.csv`, `test_set.csv`) carries the same terms: attribution required, non-commercial use only, share-alike if redistributed. See `data/README.md` for details.

## Running the code

```bash
pip install pandas numpy requests scikit-learn scipy matplotlib
```

Each script reads its inputs from the folder it is run in and writes charts to a `charts/` folder there. Run them in this order:

| Order | Script | Needs | Produces |
|---|---|---|---|
| 1 | `scripts/fetch_exoplanet_data.py` | internet connection | `exoplanets_raw.csv` |
| 2 | `scripts/clean_and_visualize.py` | `exoplanets_raw.csv`, `hwc_full.csv`, `hwc_table_all.csv` (the 70-row shortlist table from the PHL data page) | `exoplanets_clean.csv`, EDA charts |
| 3 | `scripts/clustering_pca.py` | `exoplanets_clean.csv` | clustering and PCA charts |
| 4 | `scripts/prep_train_test.py` | `exoplanets_clean.csv` | `labeled_sample.csv`, `train_set.csv`, `test_set.csv` |
| 5 | `scripts/naive_bayes.py` | `train_set.csv`, `test_set.csv` | Naive Bayes confusion matrices |
| 6 | `scripts/decision_trees.py` | `train_set.csv`, `test_set.csv` | three trees, confusion matrices, feature importance |

## Regenerating the site

Page content lives in `build.py`, so the navigation stays identical across every tab. Running it rewrites every `.html` file, so any edits made directly to the HTML files will be overwritten.

```bash
python build.py
```

## Course context

Built for CSCI 5612 (Machine Learning) at the University of Colorado Boulder. Each module adds tabs and analysis, closing with a conclusions section that answers the opening question in plain language.
