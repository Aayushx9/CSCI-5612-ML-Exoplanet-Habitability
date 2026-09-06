# Exoplanet Discovery & Habitability

A semester-long data science project built module by module: gathering, cleaning, exploring, modeling and communicating results using the public record of confirmed exoplanets.

**Live site:** https://aayushx9.github.io/CSCI-5612-ML-Exoplanet-Habitability/

## Project structure

```
index.html               Introduction (landing page), has the central question
data_gathering.html      Sources, API details, raw data etc
cleaning_prep.html       Before/after cleaning steps
eda.html                 Distributions and relationships, 10+ visualizations
clustering.html          Module 2
pca.html                 Module 2
naivebayes.html          Module 3
dectrees.html            Module 3
svms.html                Module 4
regression.html          Module 5
nn.html                  Module 5
conclusions.html         Answers the Introduction's question, in the same words
about_references.html    Bio, cited sources, code link
style.css                Shared site styling
assets/                  Images and diagrams
scripts/                 Data-gathering and analysis code
build.py                 Regenerates the HTML pages from templates
```

## Data sources

**Primary, via API:** [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/), Table Access Protocol (TAP) service, `pscomppars` table. No API key required. See `scripts/fetch_exoplanet_data.py` for the retrieval code and the DataPrep_EDA tab for the exact endpoint and example query.

**Secondary, downloaded:** [PHL Habitable Worlds Catalog](https://phl.upr.edu/hwc), maintained by the Planetary Habitability Laboratory at the University of Puerto Rico at Arecibo. Used for computed habitability indices such as the Earth Similarity Index and habitable-zone classification.

## Running the data pull

```bash
pip install requests pandas
python scripts/fetch_exoplanet_data.py
```

This saves the raw planet and host-star data to `exoplanets_raw.csv`.

## Regenerating the site

Page content lives in `build.py` as templates, so the navigation stays identical across every tab.

```bash
python build.py
```

This overwrites the `.html` files in place with the latest content.

## Course context

Built for a Machine Learning course's semester-long Data Science Lifecycle project. Each module adds new tabs and analysis: clustering and PCA, then supervised methods (Naive Bayes, Decision Trees, SVMs), then regression and neural networks, closing with a non-technical conclusions section.
