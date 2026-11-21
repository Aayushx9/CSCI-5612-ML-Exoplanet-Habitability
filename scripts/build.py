"""
Generates the static HTML pages for the exoplanet project site from
a shared template. Run this locally whenever page content changes;
it is a build helper and is not itself part of the published site.

Tab structure and reading order follow the professor's Week 3 pipeline:
Introduction (landing page) -> Data Gathering -> Cleaning & Prep -> EDA
-> one tab per model -> Conclusions -> About / References

Every page gets both the top tab bar (jump anywhere) and a bottom
Previous/Next pair (follow the pipeline in order, one click at a time).
"""
import os

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} - Exoplanet Discovery &amp; Habitability</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Spectral:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>
"""

FOOT = """
<footer>
  Exoplanet Discovery &amp; Habitability. A semester project for a Machine Learning course, built module by module.
</footer>
</body>
</html>
"""

# Order here IS the pipeline reading order: top nav highlights the current
# tab, and pipeline_nav() below turns this same list into Previous/Next links.
NAV_LINKS = [
    ("index.html", "Introduction"),
    ("data_gathering.html", "Data Gathering"),
    ("cleaning_prep.html", "Cleaning &amp; Prep"),
    ("eda.html", "EDA"),
    ("clustering.html", "Clustering"),
    ("pca.html", "PCA"),
    ("naivebayes.html", "NaiveBayes"),
    ("dectrees.html", "DecTrees"),
    ("regression.html", "Regression"),
    ("adaboost.html", "AdaBoost"),
    ("gradientboosting.html", "GradientBoosting"),
    ("xgboost.html", "XGBoost"),
    ("conclusions.html", "Conclusions"),
    ("about_references.html", "About / References"),
]

CENTRAL_QUESTION = (
    "Which of the thousands of confirmed exoplanets look most like they "
    "could support life, and what measurable properties set those planets "
    "apart from the rest?"
)


def nav(active_href):
    items = []
    for href, label in NAV_LINKS:
        cls = ' class="active"' if href == active_href else ""
        items.append(f'<a href="{href}"{cls}>{label}</a>')
    return (
        '<nav class="topnav">'
        '<span class="brand">Exoplanet Discovery &amp; Habitability</span>'
        + "".join(items)
        + "</nav>"
    )


def pipeline_nav(active_href):
    """Bottom-of-page Previous/Next links that walk the pipeline in order,
    the in-content links the story-arc diagram calls for, distinct from the
    jump-anywhere top tab bar."""
    hrefs = [h for h, _ in NAV_LINKS]
    labels = dict(NAV_LINKS)
    i = hrefs.index(active_href)

    if i > 0:
        prev_href = hrefs[i - 1]
        prev_html = f'<a class="prev" href="{prev_href}">&larr; {labels[prev_href]}</a>'
    else:
        prev_html = "<span></span>"

    if i < len(hrefs) - 1:
        next_href = hrefs[i + 1]
        next_html = f'<a class="next" href="{next_href}">{labels[next_href]} &rarr;</a>'
    else:
        first_href = hrefs[0]
        next_html = f'<a class="next" href="{first_href}">Back to {labels[first_href]} &rarr;</a>'

    return f'<div class="pipeline-nav">{prev_html}{next_html}</div>'


def page(slug, title, inner_html):
    full = (
        HEAD.format(title=title)
        + nav(f"{slug}.html")
        + "<main>"
        + inner_html
        + pipeline_nav(f"{slug}.html")
        + "</main>"
        + FOOT
    )
    with open(f"{slug}.html", "w") as f:
        f.write(full)


def model_stub(slug, title, module_note):
    inner = f"""
  <p class="eyebrow">{title}</p>
  <h1>{title}</h1>
  <div class="stub">
    <span class="module-tag">{module_note}</span>
    <p style="margin:0 0 1em">This tab will walk through {title} in four parts, tied back to the
    project's central question:</p>
    <p style="margin:0 0 0.4em"><strong>Overview.</strong> What the method does and why it fits this question.</p>
    <p style="margin:0 0 0.4em"><strong>Data.</strong> The prepared dataset used for this method, with links to raw and cleaned data.</p>
    <p style="margin:0 0 0.4em"><strong>Code.</strong> A link to the code, with the language and core packages noted.</p>
    <p style="margin:0"><strong>Results.</strong> What the output shows, and what it means for the question above, not just the metric.</p>
  </div>
"""
    page(slug, title, inner)



def build():
    # --- Introduction (landing page) ---
    intro_inner = f"""
  <p class="eyebrow">Introduction</p>
  <h1>Exoplanet Discovery &amp; Habitability</h1>

  <div class="callout">
    <strong>The question:</strong> {CENTRAL_QUESTION}
  </div>

  <p>For most of human history, the planets orbiting other stars existed only as speculation. That changed within the last three decades, as advances in telescope sensitivity turned the search for exoplanets into one of the most active fields in astronomy. Missions such as NASA's Kepler Space Telescope and its successor, the Transiting Exoplanet Survey Satellite (TESS), have monitored hundreds of thousands of stars, watching for the tiny, periodic dimming that occurs when a planet passes directly in front of its star. Ground-based observatories have complemented this work by detecting the subtle gravitational wobble a planet induces in the star it orbits. Together, these efforts have confirmed thousands of worlds beyond the Solar System, ranging from scorched gas giants that circle their stars faster than Mercury circles the Sun to small, rocky planets that may resemble Earth in size. Each discovery adds to a growing public catalog, the NASA Exoplanet Archive, which records the physical and orbital properties of every confirmed planet, including its radius, mass, orbital period, and the characteristics of its host star. This catalog has become the primary reference point for astronomers and educators alike, and it is updated continuously as new missions and instruments refine existing measurements or discover new worlds. What began as a search to answer a single question, whether stars other than the Sun have planets, has grown into a broader effort to catalog an entire population of worlds and understand how common planetary systems are throughout the galaxy. The scale of that population, now numbering in the thousands and growing every year, is the starting point for the story of modern exoplanet science.</p>

  <figure>
    <img src="assets/transit-diagram.svg" alt="Diagram of a planet transiting its star and the resulting dip in the star's observed brightness">
    <figcaption>The transit method: a planet crossing its star produces a small, periodic dip in the star's measured brightness.</figcaption>
  </figure>

  <p>Among the thousands of confirmed exoplanets, a smaller and more carefully studied group has drawn particular attention: those that might be capable of supporting life. The question of habitability extends beyond simple existence, asking instead whether a planet's size, temperature, and position around its star place it within the conditions thought necessary for liquid water and a stable climate. The Planetary Habitability Laboratory at the University of Puerto Rico at Arecibo has maintained a running catalog of these candidates for over a decade, ranking known planets according to indices such as the Earth Similarity Index and their position within a star's habitable zone. Interest in this question extends well beyond academic astronomy: educators use potentially habitable worlds to illustrate scientific concepts to students, science communicators and the public follow new candidates with the same curiosity once reserved for missions to Mars, and space agencies weigh habitability findings when prioritizing future telescopes and instruments designed to analyze distant atmospheres for signs of biological activity. At the same time, the criteria used to judge habitability remain incomplete and are still debated among scientists, since every assessment is built from a handful of measurable properties rather than direct observation of a planet's surface or atmosphere. Some planets once considered promising candidates have since been reclassified as measurements improved, and the definition of what counts as an Earth-like world continues to be refined. This tension, between the desire to identify worlds that could host life and the limitations of what can currently be measured from light-years away, sits at the center of exoplanet habitability research today.</p>

  <p>The diversity among confirmed exoplanets has itself become a central problem for the field. Unlike the Solar System, where planets fall into clear categories of small rocky worlds and large gas giants with little in between, many confirmed exoplanets have no local counterpart at all. Chief among these is the sub-Neptune, a planet larger than Earth but smaller than Neptune, a size range entirely absent from the Sun's own planetary system yet common enough among confirmed exoplanets to be considered one of the most frequent outcomes of planet formation. Making sense of this unfamiliar diversity requires moving beyond individual case studies and instead looking for structure across the population as a whole: do planets naturally separate into a handful of recognizable groups, or do they form more of a continuum with no sharp boundaries at all? Answering that question has consequences well beyond bookkeeping. How planets are grouped shapes which worlds get prioritized for further observation, which theories of planet formation gain or lose support, and which planets look like reasonable candidates for hosting life in the first place. A population this large and this varied cannot be understood one planet at a time, and the search for structure within it is now as central to exoplanet science as the search for new planets themselves.</p>

  <figure>
    <img src="assets/m2/intro_size_comparison.png" alt="Simple size comparison of Earth, Super-Earth, Sub-Neptune, Neptune, and Jupiter">
    <figcaption>The sub-Neptune, larger than Earth but smaller than Neptune, has no counterpart anywhere in the Solar System, despite being common among confirmed exoplanets.</figcaption>
  </figure>

  <p>A habitable label is a judgment made from incomplete evidence, and understanding how that judgment is reached matters as much as the list of planets it produces. No telescope has yet seen the surface of a distant rocky planet, so a planet is called potentially habitable when its size, the energy it receives from its star, and its distance from that star fall inside ranges that would allow liquid water on a world like Earth. Those ranges rest on assumptions about atmospheres and climate that cannot yet be checked, which is why different research groups draw the boundaries in slightly different places and why candidate lists differ from one catalog to another. The result is a very short list: among thousands of confirmed planets, only about seventy are flagged, and most of them orbit small, cool stars rather than stars like the Sun. Small, cool stars are the most common kind in the galaxy and make planets easier to detect, but they also tend to be active, and their flares may strip the atmospheres of nearby worlds, so a place on the list does not guarantee that a planet could hold onto the air and water that life would need. The label also carries practical consequences, because flagged planets are the ones most likely to be chosen for scarce observing time on the largest telescopes, and a planet that falls just outside the boundaries may wait years for a closer look. Since the boundaries depend on measurements that are missing or uncertain for many planets, there is real value in asking how much of the label could be anticipated from a handful of basic measurements, and where that guess goes wrong. Planets that look like candidates on paper but are not on the list, and listed planets that look unremarkable, point to where current criteria may be too strict, too generous, or missing something. Each of those cases is a reminder that habitability is a hypothesis to be tested, not a fact to be read off a table.</p>

  <p>Mass is one of the hardest properties of a distant planet to measure, and its absence quietly limits what can be said about a world. A planet's size comes from how much starlight it blocks when it crosses its star, which survey telescopes record for thousands of stars at once. Its mass comes from the tiny tug it exerts on that star, a wobble so small for Earth-sized planets that it takes many nights on the most precise instruments to detect. As a result, many known planets have a measured size but no measured mass, and some have the reverse. This matters because size and mass together reveal density, and density is the clue that separates a rocky world from a swollen, gas-rich one of the same width. Astronomers have long filled the gap with empirical rules of thumb that link size to mass, built from the planets where both are known, and those rules quietly shape which worlds are described as rocky and therefore worth a closer look for habitability. The rules work best on average and can fail for individual planets, since two planets of the same size can have very different compositions. Every missing measurement adds uncertainty to the habitability judgment described above, and every new measurement can change a planet's standing on the list. For people outside astronomy, the practical lesson is that the catalog of potentially habitable worlds is a set of best estimates that is revised as the data improves, not a finished map. Understanding which measurements carry the most weight in these judgments, and how far basic ones can stand in for the harder ones, is part of reading that map honestly.</p>

  <h2>Related questions this project explores</h2>
  <ol class="questions">
    <li>How many confirmed exoplanets exist, and how has the discovery rate changed since Kepler and TESS began operating?</li>
    <li>Which detection methods (transit, radial velocity, direct imaging, microlensing) have contributed the most confirmed discoveries, and how does that shape the population of planets currently known?</li>
    <li>What ranges of planetary radius and mass are most common among confirmed exoplanets, and how do these compare to the planets of the Solar System?</li>
    <li>How does a planet's orbital distance from its host star relate to its equilibrium temperature and its position within the star's habitable zone?</li>
    <li>What stellar properties, such as temperature, mass, and metallicity, are most associated with hosting potentially habitable planets?</li>
    <li>Do planets separate into natural groups based on measurable physical properties, and do those groups align with existing categories such as super-Earths, mini-Neptunes, and gas giants?</li>
    <li>Which combination of planetary and stellar features best distinguishes planets in the optimistic habitable zone from those in the conservative one?</li>
    <li>How well can a planet's mass be estimated from its radius and orbital period alone, and where do those estimates break down?</li>
    <li>Are potentially habitable planets more common around particular types of stars, such as M dwarfs, than around Sun-like stars, and what would that imply for the search for life?</li>
    <li>How has the field's understanding of habitability evolved over time, and what limitations remain in judging a planet's suitability for life from remote observations alone?</li>
  </ol>
"""
    page("index", "Introduction", intro_inner)

    # --- Data Gathering ---
    gathering_inner = """
  <p class="eyebrow">Data Gathering</p>
  <h1>Data Gathering</h1>

  <div class="section-card">
    <h3>Primary source: NASA Exoplanet Archive API</h3>
    <p style="margin-bottom:0.6em">Website: <a href="https://exoplanetarchive.ipac.caltech.edu/">exoplanetarchive.ipac.caltech.edu</a></p>
    <p style="margin-bottom:0.6em">Core endpoint (Table Access Protocol, synchronous query):</p>
    <pre>https://exoplanetarchive.ipac.caltech.edu/TAP/sync</pre>
    <p style="margin-bottom:0.6em">Example GET request pulling key planet and host-star columns from the Planetary Systems Composite Parameters table:</p>
    <pre>https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,discoverymethod,disc_year,pl_orbper,pl_rade,pl_bmasse,pl_eqt,st_teff,st_rad,st_mass,sy_dist+from+pscomppars&amp;format=csv</pre>
    <p style="margin:0">Retrieval code: <a href="scripts/fetch_exoplanet_data.py">fetch_exoplanet_data.py</a> (Python, uses <code>requests</code> and <code>pandas</code>).</p>
  </div>

  <div class="section-card">
    <h3>Secondary source: PHL Habitable Worlds Catalog</h3>
    <p style="margin-bottom:0.6em">Website: <a href="https://phl.upr.edu/hwc/data">phl.upr.edu/hwc/data</a>, maintained by the Planetary Habitability Laboratory, University of Puerto Rico at Arecibo. Downloaded directly as a CSV, not via API.</p>
    <p style="margin:0">Matched against the NASA Exoplanet Archive pull by planet name: 5,565 of 6,366 planets found a match. The remaining 801 are planets confirmed after the catalog's last update and have not yet been assessed by it. Each matched planet carries an official habitability classification (not habitable, conservative sample, or optimistic sample) and an Earth Similarity Index score.</p>
  </div>

  <p style="margin:0 0 1.6em">Full secondary source file: <a href="data/hwc_full.csv">hwc_full.csv</a> (5,599 rows, 118 columns).</p>

  <figure>
    <img src="assets/eda/raw_preview.png" alt="Preview of the first rows of raw exoplanet data pulled from the API">
    <figcaption>A sample of the 6,366 confirmed planets pulled directly from the NASA Exoplanet Archive, before any cleaning.</figcaption>
  </figure>

  <p>Full raw file: <a href="data/exoplanets_raw.csv">exoplanets_raw.csv</a> (6,366 rows, 12 columns).</p>
"""
    page("data_gathering", "Data Gathering", gathering_inner)

    # --- Cleaning & Prep ---
    cleaning_inner = """
  <p class="eyebrow">Cleaning &amp; Prep</p>
  <h1>Cleaning &amp; Prep</h1>

  <p>The raw pull from the NASA Exoplanet Archive contained 6,366 confirmed planets across 12 columns. Checking it directly turned up no duplicate planet names and no negative or physically impossible values in any numeric column, so nothing needed to be discarded on those grounds. What it did contain was real missingness: several hundred planets are missing an equilibrium temperature, a stellar radius, or an orbital period, because not every confirmed planet has had every follow-up measurement taken. Rather than filling those gaps with estimated values this early, they were left as missing and documented, since the right way to handle them depends on which model uses that column later.</p>

  <figure>
    <img src="assets/eda/01_missingness.png" alt="Bar chart showing the percentage of missing values in each column">
    <figcaption>Equilibrium temperature and stellar radius are missing most often, since a full follow-up characterization is not run for every confirmed planet.</figcaption>
  </figure>

  <p>One judgment call was made explicit rather than hidden: 157 planets have an estimated mass above roughly 13 Jupiter masses, the rough boundary where the literature starts calling an object a brown dwarf instead of a planet. These are still confirmed entries in the archive, so they were kept rather than deleted, but flagged with a new column, <code>is_borderline_massive</code>, so later analysis can include or exclude them deliberately instead of by accident.</p>

  <p>Two new columns were also added by discretizing existing measurements, since several of the models coming up in later modules work better with categories than raw numbers. <code>size_class</code> groups each planet into Earth-sized, Super-Earth, Sub-Neptune/Neptune, or Giant based on radius. <code>temp_zone</code> groups each planet into Too Cold, Temperate, or Too Hot based on estimated equilibrium temperature, using roughly 200 to 320 Kelvin as the range where liquid water is plausible. Both are simple, transparent rules meant as a starting point, not a final answer.</p>

  <p>The cleaned NASA data was then merged with the PHL Habitable Worlds Catalog by planet name. Of 6,366 planets, 5,565 matched, and each matched planet now carries the catalog's own habitability classification (not habitable, conservative sample, or optimistic sample) and its Earth Similarity Index. The 801 planets without a match were confirmed after the catalog's last update and simply have not been assessed by it yet, a gap in coverage rather than a data error. This merge matters more than the rough <code>temp_zone</code> estimate above, since it is a published, expert-reviewed classification rather than a simple temperature cutoff, and the two can now be compared directly.</p>

  <figure>
    <img src="assets/eda/clean_preview.png" alt="Preview of the cleaned data with new size_class and temp_zone columns">
    <figcaption>The same planets after cleaning, now carrying a size class, a temperature zone, and a flag for borderline-massive objects.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/12_top_esi_table.png" alt="Table of the 10 planets with the highest Earth Similarity Index">
    <figcaption>The ten planets the Habitable Worlds Catalog currently rates most Earth-like, led by Teegarden's Star b and TOI-700 d, several of which now appear in every later analysis on this site.</figcaption>
  </figure>

  <p>A later check, made while preparing the regression analysis, found that many planets have a mass and radius that fall within 1% of a published mass-radius formula (2,550 of the 3,532 planets in the training set), which suggests the archive's composite table filled in one of the two values from the other for those planets. The values were kept, since they are what the archive reports, but results that depend on mass and radius together should be read with this in mind, and the Regression tab reports its results both with and without these planets.</p>

  <p>Full cleaned and merged file: <a href="data/exoplanets_clean.csv">exoplanets_clean.csv</a> (6,366 rows, 21 columns). Cleaning and merging code: <a href="scripts/clean_and_visualize.py">clean_and_visualize.py</a> (Python, uses <code>pandas</code>).</p>
"""
    page("cleaning_prep", "Cleaning & Prep", cleaning_inner)

    # --- EDA ---
    eda_inner = """
  <p class="eyebrow">EDA</p>
  <h1>Exploratory Data Analysis</h1>
  <p>Eleven views into the cleaned, merged dataset of 6,366 confirmed exoplanets, covering how the data was collected, what kinds of planets and stars show up most, and where the temperate, potentially habitable candidates sit within that population. Visualization code: <a href="scripts/clean_and_visualize.py">clean_and_visualize.py</a> (Python, uses <code>matplotlib</code>).</p>

  <figure>
    <img src="assets/eda/11_hwc_habitability.png" alt="Bar chart of official Habitable Worlds Catalog classification counts">
    <figcaption>Only 70 of the 5,565 matched planets carry any official habitable classification at all, underscoring just how rare a strong habitability candidate still is, even after thousands of confirmed discoveries.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/02_discovery_method.png" alt="Bar chart of confirmed planets by discovery method">
    <figcaption>The transit method accounts for the large majority of confirmed planets, which biases the known population toward planets that happen to cross in front of their star as seen from Earth.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/03_discoveries_per_year.png" alt="Line chart of confirmed exoplanet discoveries per year">
    <figcaption>Confirmed discoveries jump sharply after 2009 and again after 2014, tracking the Kepler and K2/TESS missions rather than any change in how many planets actually exist.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/04_radius_distribution.png" alt="Histogram of planet radius in Earth radii">
    <figcaption>Most confirmed planets are smaller than Neptune, with a large cluster only a few times Earth's radius.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/05_mass_distribution.png" alt="Histogram of planet mass in Earth masses">
    <figcaption>Planet mass spans more than five orders of magnitude, from bodies lighter than Mercury to objects bordering on brown dwarfs.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/06_mass_vs_radius.png" alt="Scatter plot of planet mass versus radius, log-log scale">
    <figcaption>Mass and radius track closely for smaller planets but scatter widely above roughly ten Earth radii, where gas giants of very different densities overlap.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/07_period_vs_temp.png" alt="Scatter plot of orbital period versus equilibrium temperature">
    <figcaption>Equilibrium temperature falls off sharply as orbital period increases, consistent with planets further from their star receiving less energy from it.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/08_star_temperature.png" alt="Histogram of host star effective temperature, with the Sun marked for reference">
    <figcaption>Most confirmed planets orbit stars cooler than the Sun, reflecting both how common cooler stars are and which stars current methods find planets around most easily.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/01_missingness.png" alt="Bar chart showing percentage of missing values per column">
    <figcaption>Equilibrium temperature and stellar radius are the columns most often missing, a gap carried over from Data Gathering and documented rather than filled in.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/09_size_class.png" alt="Bar chart of planets grouped into size classes">
    <figcaption>Sub-Neptune and Neptune-sized planets, a size class with no counterpart in the Solar System, form the single largest group of confirmed exoplanets.</figcaption>
  </figure>

  <figure>
    <img src="assets/eda/10_temp_zone.png" alt="Bar chart of planets grouped by equilibrium temperature zone">
    <figcaption>The great majority of confirmed planets are too hot for liquid water under this simple estimate, and only a small fraction fall in the temperate zone this project is most interested in.</figcaption>
  </figure>
"""
    page("eda", "EDA", eda_inner)

    # --- Clustering ---
    clustering_inner = """
  <p class="eyebrow">Clustering</p>
  <h1>Clustering</h1>

  <h2>Overview</h2>
  <p>Clustering is an unsupervised method: it looks for structure in data that has no labels to begin with, grouping observations that are similar to each other and separating ones that are not. Two broad families of clustering were used here. Partitional clustering, specifically k-means, picks a fixed number of groups ahead of time and assigns every point to whichever group center it is closest to, adjusting the centers until the assignment stabilizes. Hierarchical clustering takes a different approach: it starts with every point as its own group and repeatedly merges the two closest groups, building a nested tree of merges rather than a single flat partition. Both families need a notion of distance between points, and the choice of distance measure matters. Euclidean distance measures straight-line distance between two points and is sensitive to the overall scale of each value. Cosine distance instead measures the angle between two points treated as vectors, ignoring their magnitude entirely, which makes it a natural fit when the direction of a pattern matters more than its size.</p>

  <figure>
    <img src="assets/m2/concept_partitional_vs_hierarchical.png" alt="Side-by-side illustration of partitional clustering versus hierarchical clustering">
    <figcaption>Partitional clustering assigns points to a fixed number of flat groups; hierarchical clustering instead builds a nested tree of merges.</figcaption>
  </figure>

  <figure>
    <img src="assets/m2/concept_distance_metrics.png" alt="Diagram comparing Euclidean distance and cosine distance between two points">
    <figcaption>Euclidean distance is the straight-line gap between two points; cosine distance is the angle between them, regardless of how far out each point sits.</figcaption>
  </figure>

  <p>Here, clustering is used for discovery rather than prediction: the goal is to see whether confirmed exoplanets naturally separate into a handful of recognizable physical types, or whether they instead form a continuum with no sharp boundaries, directly picking up the question raised in the Introduction about the sub-Neptune and other planets with no Solar System counterpart.</p>

  <h2>Data Prep</h2>
  <p>Clustering requires only unlabeled numeric data, so the categorical columns (planet name, discovery method, size class label, and so on) were dropped entirely for this step. Eight numeric columns were used: orbital period, planet radius, planet mass, equilibrium temperature, host star temperature, host star radius, host star mass, and system distance. Rows missing any of these eight values were excluded, leaving 5,676 of the original 6,366 planets. Because these properties span several orders of magnitude (orbital period alone ranges from a fraction of a day to over a million years), each column was log-transformed and then standardized to zero mean and unit variance before clustering, so that no single feature dominates the distance calculation purely because of its raw scale.</p>

  <figure>
    <img src="assets/m2/cluster_data_preview.png" alt="Preview of the log-transformed numeric data used for clustering">
    <figcaption>A sample of the eight log-transformed numeric features that both k-means and hierarchical clustering were run on (standardized just before fitting).</figcaption>
  </figure>

  <p>Full prepared data: <a href="data/exoplanets_clean.csv">exoplanets_clean.csv</a> (the raw and cleaned files behind it are linked from Data Gathering and Cleaning &amp; Prep).</p>

  <h2>Code</h2>
  <p>K-means and hierarchical clustering code: <a href="scripts/clustering_pca.py">clustering_pca.py</a> (Python, uses <code>scikit-learn</code> and <code>scipy</code>).</p>

  <h2>Results</h2>
  <p>K-means was run at four values of k (2, 3, 4, and 5), and the average silhouette score, a measure of how well-separated the resulting clusters are, was computed for each. The scores were close across the board (0.33 to 0.36), with k=3 and k=5 essentially tied for the best score and k=4 slightly behind both. This is itself informative: there is no single value of k that stands out sharply, which suggests the underlying population does not split into perfectly crisp groups.</p>

  <figure>
    <img src="assets/m2/silhouette_by_k.png" alt="Line chart of average silhouette score across different values of k">
    <figcaption>Silhouette scores for k = 2 through 7. The curve is relatively flat between k=3 and k=5, with no single value standing out as a clearly correct choice.</figcaption>
  </figure>

  <figure>
    <img src="assets/m2/kmeans_clusters_pca.png" alt="Scatter plot of k-means clusters shown in PC1/PC2 space">
    <figcaption>K-means clusters at k=5, the best-scoring value, shown in the same PC1/PC2 space used on the PCA tab. The clusters sit closer to overlapping regions than to sharply separated islands.</figcaption>
  </figure>

  <p>Hierarchical clustering was run using cosine distance with average linkage (cosine distance cannot be combined with Ward or centroid linkage, so average linkage was used instead). The resulting dendrogram shows one especially large jump in merge distance right at the final merge, a common heuristic for reading how many clusters a dendrogram actually supports, and that jump points to just 2 clusters as the most defensible cut.</p>

  <figure>
    <img src="assets/m2/dendrogram.png" alt="Dendrogram of hierarchical clustering with cosine distance, truncated to the last 30 merges">
    <figcaption>The large jump in height at the very top of the tree, going from 2 clusters to 1, is much bigger than any other merge nearby, which is why the dendrogram points to 2 clusters.</figcaption>
  </figure>

  <p>Comparing the two methods directly: cutting the hierarchical tree at k=5 (to match k-means) and measuring agreement with the Adjusted Rand Index gives a score of 0.41, out of a maximum of 1.0 for perfect agreement. That is a moderate but incomplete overlap, the two methods agree there is more than one group, but settle on different boundaries.</p>

  <figure>
    <img src="assets/m2/kmeans_vs_hclust.png" alt="Heatmap showing how k-means and hierarchical clustering assignments overlap">
    <figcaption>Where the two methods agree, nearly all of one k-means cluster falls inside a single hierarchical cluster; where they disagree, a k-means cluster is split across several hierarchical branches.</figcaption>
  </figure>

  <h2>Conclusions</h2>
  <p>Neither method found sharply separated groups of exoplanets, and that is itself a finding that matters for the topic. The flat silhouette curve, the moderate agreement between k-means and hierarchical clustering, and the dendrogram's preference for a small number of clusters together suggest that exoplanet physical properties form more of a continuum than a set of distinct categories, echoing the sub-Neptune problem raised in the Introduction: common size and mass ranges really do blur together rather than falling into tidy bins. That has a direct bearing on the central question. A population of planets this continuous means that any attempt to flag "potentially habitable" worlds based on physical properties alone, including the rough temperature-zone rule used in Cleaning &amp; Prep, is drawing a somewhat arbitrary line across what is actually a gradient, not a boundary nature has clearly drawn.</p>
"""
    page("clustering", "Clustering", clustering_inner)

    # --- PCA ---
    pca_inner = """
  <p class="eyebrow">PCA</p>
  <h1>PCA</h1>

  <h2>Overview</h2>
  <p>Principal Component Analysis (PCA) is a dimensionality reduction technique: it takes data described by many correlated numeric variables and re-expresses it using a smaller number of new variables, called principal components, that capture as much of the original variation as possible. Each principal component is a direction in the original feature space, found from the eigenvectors of the data's covariance matrix. The eigenvector points in the direction of a pattern of variation, and its paired eigenvalue measures how much of the data's total variance lies along that direction. The first principal component is the eigenvector with the largest eigenvalue, the direction along which the data spreads out the most; each following component captures the next largest share of remaining variance, at a right angle to all the ones before it.</p>

  <figure>
    <img src="assets/m2/concept_eigenvectors.png" alt="Illustration of eigenvectors pointing along the directions of greatest spread in a 2D dataset">
    <figcaption>Eigenvectors point along the directions a dataset spreads out the most; eigenvalues measure how much variance lies along each direction.</figcaption>
  </figure>

  <p>High-dimensional data is difficult to explore directly: a dataset with eight numeric columns, as used here, cannot be plotted on a single chart, and many pairs of those columns are correlated with each other in ways that are hard to see from any one scatter plot alone. Reducing many correlated variables down to two or three principal components makes it possible to visualize the overall shape of the data, spot outliers, and see which original variables move together, all without inspecting every pairwise combination by hand.</p>

  <figure>
    <img src="assets/m2/concept_dim_reduction.png" alt="Illustration of 2D data projected onto a single line representing the first principal component">
    <figcaption>Dimensionality reduction projects correlated data onto a smaller number of axes, each one a direction chosen to preserve as much of the original spread as possible.</figcaption>
  </figure>

  <h2>Data Prep</h2>
  <p>PCA requires numeric data on a common scale, the same requirement as clustering. The same eight log-transformed, standardized features and the same 5,676 complete rows used for clustering were used here as well, so the two analyses are directly comparable.</p>

  <figure>
    <img src="assets/m2/cluster_data_preview.png" alt="Preview of the log-transformed numeric data used for PCA">
    <figcaption>The same prepared feature set used for clustering: eight log-transformed numeric columns, standardized just before PCA.</figcaption>
  </figure>

  <p>Full prepared data: <a href="data/exoplanets_clean.csv">exoplanets_clean.csv</a>.</p>

  <h2>Code</h2>
  <p>PCA code: <a href="scripts/clustering_pca.py">clustering_pca.py</a> (Python, uses <code>scikit-learn</code>).</p>

  <h2>Results</h2>
  <p>The first two principal components together explain about 72% of the total variance in the eight original features, and the first three explain about 85%. Looking at which original features load most heavily onto each component gives the components physical meaning rather than leaving them as abstract numbers: PC1 loads positively on planet radius, planet mass, stellar radius, and stellar mass, reading roughly as an overall "how big is this planet and its star" axis. PC2 loads positively on equilibrium temperature and system distance but negatively on orbital period, reading roughly as a "how close-in and hot is this planet" axis.</p>

  <figure>
    <img src="assets/m2/pca_scree.png" alt="Scree plot showing the proportion of variance explained by each principal component">
    <figcaption>PC1 and PC2 together account for about 72% of the total variance; the remaining six components each add comparatively little.</figcaption>
  </figure>

  <figure>
    <img src="assets/m2/pca_pc1_pc2.png" alt="Scatter plot of exoplanets projected onto the first two principal components">
    <figcaption>Every planet reduced from eight dimensions to two. The same lack of sharp separation seen in clustering shows up here too, as one continuous cloud rather than distinct islands.</figcaption>
  </figure>

  <figure>
    <img src="assets/m2/pca_loadings.png" alt="Biplot showing which original features drive PC1 and PC2">
    <figcaption>Planet radius and mass point one direction, equilibrium temperature and system distance point another, which is what gives PC1 and PC2 their physical meaning.</figcaption>
  </figure>

  <h2>Conclusions</h2>
  <p>PCA reinforces what clustering already suggested: the eight physical properties measured for each confirmed exoplanet are not independent of each other, planet size and mass move together, and orbital distance and temperature move together, which is exactly why two components can summarize 72% of eight columns' worth of information. But the projection onto PC1 and PC2 shows one continuous cloud of points rather than separated groups, the same conclusion clustering reached by a completely different method. Taken together, the two analyses point toward the same answer to the project's central question: the properties that would distinguish a potentially habitable planet from the rest of the population do not form a separate, easily isolated cluster, they sit along the same continuum as everything else, which is part of why only a small number of planets end up confidently labeled as habitability candidates at all.</p>
"""
    page("pca", "PCA", pca_inner)


    # --- Naive Bayes ---
    nb_inner = """
  <p class="eyebrow">Naive Bayes</p>
  <h1>Naive Bayes</h1>

  <h2>Overview</h2>
  <p>Naive Bayes is a supervised classification method: it learns from planets whose class is already known and then predicts the class of planets it has not seen. It applies Bayes' rule, which combines how common each class is overall (the prior) with how typical each measurement is for that class (the likelihood), and it makes one deliberately simple assumption: that once the class is known, the measurements are independent of one another. That assumption is rarely exactly true, since a planet's radius and mass are clearly related, which is where the word naive comes from, but the method often works well anyway, trains almost instantly, and needs relatively little data. It is widely used for sorting text, such as spam filtering and document topics, and as a quick baseline classifier on tabular data.</p>

  <figure>
    <img src="assets/m3/nb_bayes_rule.png" alt="The Naive Bayes rule written as prior times the product of per-measurement likelihoods">
    <figcaption>The class with the highest combined score wins: the prior belief about the class, multiplied by the evidence from each measurement taken separately.</figcaption>
  </figure>

  <p>Two common versions differ in how they treat a measurement. Multinomial Naive Bayes treats each feature as a count, such as how many times a word appears in a document, and learns for each class how large each count tends to be. Because it works with counts, every feature value must be zero or positive. Bernoulli Naive Bayes treats each feature as present or absent, a simple yes or no, so it uses only whether something occurs and not how often, and it also counts the absence of a feature as evidence, which suits short texts and yes/no tags. Here the standard multinomial version is used, applied to planet measurements rescaled to a 0 to 1 range, to predict whether the Habitable Worlds Catalog lists a planet as potentially habitable from its eight physical measurements.</p>

  <h2>Data Prep</h2>
  <p>Supervised methods can only learn from labeled data, so every planet used here needs a known answer. The label comes from the PHL Habitable Worlds Catalog and was collapsed into a single yes/no value: a planet counts as habitable if the catalog lists it in either its conservative or its optimistic sample. Only planets the catalog has assessed, and that have all eight measurements, were kept, leaving 5,047 labeled planets. Of those, 66 are habitable (1.3%) and 4,981 are not.</p>

  <figure>
    <img src="assets/m3/labeled_preview.png" alt="Preview of the labeled data with eight measurements and a habitable label">
    <figcaption>A sample of the labeled data: eight measurements per planet and a habitable label, where 1 means the catalog lists the planet as potentially habitable.</figcaption>
  </figure>

  <p>The labeled data was then split at random into a training set (70%) and a testing set (30%). The training set is what the model learns from, and the testing set is held back to measure how well it does on planets it has never seen. The two sets must be disjoint, with no planet in both, because a model scored on planets it already learned from would look better than it really is. The split was stratified, which keeps the same small share of habitable planets in both sets, and a check in the code confirmed that zero planets appear in both. The training set has 3,532 planets (46 habitable) and the testing set has 1,515 planets (20 habitable).</p>

  <figure>
    <img src="assets/m3/train_preview.png" alt="Preview of the training set">
    <figcaption>A sample of the training set, 3,532 planets (46 habitable), used to build the model.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/test_preview.png" alt="Preview of the testing set">
    <figcaption>A sample of the testing set, 1,515 planets (20 habitable), kept aside to score the model.</figcaption>
  </figure>

  <p>Multinomial Naive Bayes needs non-negative numbers, so each measurement was log-transformed, for the same reason as in the clustering step, and then rescaled to run from 0 to 1 using the training set's minimum and maximum. Testing-set planets that fall outside the training range were clipped to 0 or 1. Data files: <a href="data/labeled_sample.csv">labeled_sample.csv</a>, <a href="data/train_set.csv">train_set.csv</a>, and <a href="data/test_set.csv">test_set.csv</a>. The raw and cleaned files behind them are linked from Data Gathering and Cleaning &amp; Prep.</p>

  <h2>Code</h2>
  <p>Data split: <a href="scripts/prep_train_test.py">prep_train_test.py</a>. Naive Bayes: <a href="scripts/naive_bayes.py">naive_bayes.py</a>. Both are written in Python and use <code>pandas</code>, <code>scikit-learn</code>, and <code>matplotlib</code>.</p>

  <h2>Results</h2>
  <p>Because the habitable class is so rare, two versions of the model were fit. The first learns its prior from the training set, where 98.7% of planets are not habitable. It predicted not habitable for all 1,515 testing planets, which gives an accuracy of 98.7%, exactly the score of a model that always guesses no, and it found none of the 20 habitable planets. The second version gives both classes an equal prior. Its accuracy fell to 83.2%, but it found 19 of the 20 habitable planets, a recall of 95%. The price was 253 non-habitable planets wrongly flagged, so only 19 of the 272 planets it flagged, about 7%, are actually habitable.</p>

  <figure>
    <img src="assets/m3/nb_confusion_matrices.png" alt="Confusion matrices for Naive Bayes with a learned prior and with an equal prior">
    <figcaption>Left, the learned prior never predicts habitable. Right, the equal prior catches 19 of 20 habitable planets but also flags 253 that are not.</figcaption>
  </figure>

  <h2>Conclusions</h2>
  <p>The first lesson is about the topic itself: habitable planets are so rare that a model can score 98.7% by saying no to everything, so accuracy alone says almost nothing about whether the model is useful for finding them. The second is that a planet's basic measurements narrow the field without picking winners. With equal priors the model catches nearly every habitable planet in the testing set, but it produces a long list of false alarms, which fits the earlier finding that planet properties form a continuum and not sharply separated groups. The independence assumption is also a poor match for these measurements, since size, mass, temperature, and orbit are closely linked, and that may contribute to the false alarms, though this was not tested directly. Two cautions apply. The catalog's own habitable criteria are built from quantities closely related to these same measurements, so part of what the model learns is the catalog's rule of thumb. And with only 20 habitable planets in the testing set, a single planet changes the recall by five percentage points, so these numbers are rough.</p>
"""
    page("naivebayes", "Naive Bayes", nb_inner)

    # --- Decision Trees ---
    dt_inner = """
  <p class="eyebrow">Decision Trees</p>
  <h1>Decision Trees</h1>

  <h2>Overview</h2>
  <p>A decision tree is a supervised method that classifies by asking a chain of yes/no questions about the measurements. Each question splits the planets into two groups, and the questions continue until the groups are mostly a single class. Read from top to bottom, a tree is a set of plain rules, which makes it one of the easiest models to explain. Trees are used to classify, to predict numbers, and to show which measurements matter most, since every split names the measurement it used.</p>

  <figure>
    <img src="assets/m3/dt_concept_tree.png" alt="A small hypothetical decision tree for habitability">
    <figcaption>A hypothetical tree: each question sends a planet down one branch until it reaches a final answer at the bottom.</figcaption>
  </figure>

  <p>To choose a question, a tree tries many possible splits, each a measurement plus a cutoff value, and keeps the one that leaves the purest groups. Purity is measured in two common ways. Gini impurity is 1 minus the sum of the squared class shares, so it is 0 for a group of a single class and 0.5 at most for two classes. Entropy is the negative sum of each class share times the base 2 logarithm of that share, so it is 0 for a pure group and 1 at most for two classes. Both reward splits that make groups more one-sided and usually pick similar questions. Information gain is the impurity of the group before a split minus the weighted average impurity of the two groups after it, with each group weighted by its size, and the split with the largest gain is chosen. When Gini is used in place of entropy, the same subtraction is often called the Gini reduction.</p>

  <figure>
    <img src="assets/m3/dt_impurity_curves.png" alt="Gini impurity and entropy plotted against the share of one class">
    <figcaption>Both measures are zero for a pure group and highest for an even mix, so both push a tree toward cleaner groups.</figcaption>
  </figure>

  <p>A small example shows the arithmetic. Take 10 hypothetical planets, 5 habitable and 5 not, which gives a Gini of 0.500 and an entropy of 1.000. Splitting on whether the radius is under 1.6 Earth radii sends 6 planets left (4 habitable, 2 not) and 4 planets right (1 habitable, 3 not). The left group has a Gini of 1 - (4/6)<sup>2</sup> - (2/6)<sup>2</sup> = 0.444 and an entropy of 0.918. The right group has a Gini of 0.375 and an entropy of 0.811. Weighting by group size (6/10 and 4/10) gives a Gini of 0.417 and an entropy of 0.875 after the split. The Gini reduction is 0.500 - 0.417 = 0.083 and the information gain is 1.000 - 0.875 = 0.125. Both are positive, so the split made the groups purer, and a tree would compare this gain against every other candidate split before committing to one.</p>

  <figure>
    <img src="assets/m3/dt_split_example.png" alt="Worked example of Gini and information gain for one split of 10 hypothetical planets">
    <figcaption>The same arithmetic as above, laid out as a tree: the weighted impurity after the split is lower than before, and the drop is the gain.</figcaption>
  </figure>

  <p>It is generally possible to build an infinite number of trees from the same data. A cutoff on a continuous measurement such as radius can be any number between two neighboring planets, and every one of those numbers separates the planets in the same way while still counting as a different tree. Beyond that, the choice of which measurement to split on first, the order of the questions, whether a measurement is reused lower down, how deep the tree grows, and when it stops can all be changed, and many different combinations fit the same data about equally well. In practice a tree is pinned down by a rule for choosing splits, a depth limit, and a stopping rule, and changing any of them gives a different tree, as the three trees below show.</p>

  <h2>Data Prep</h2>
  <p>Decision trees use the same labeled data and the same training and testing split as Naive Bayes: 5,047 labeled planets, of which 66 are labeled habitable by the Habitable Worlds Catalog, split into 3,532 training planets (46 habitable) and 1,515 testing planets (20 habitable). Supervised methods need labels so the model has correct answers to learn from, and the training and testing sets must be disjoint so that the score reflects planets the tree never saw. The code confirmed that no planet appears in both. Trees only compare a measurement to a cutoff, so no log transform or rescaling is needed, and the raw measurements were used as they are.</p>

  <figure>
    <img src="assets/m3/labeled_preview.png" alt="Preview of the labeled data">
    <figcaption>A sample of the labeled data: eight measurements per planet and a habitable label.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/train_preview.png" alt="Preview of the training set">
    <figcaption>A sample of the training set, 3,532 planets (46 habitable), which the trees were grown on.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/test_preview.png" alt="Preview of the testing set">
    <figcaption>A sample of the testing set, 1,515 planets (20 habitable), used only to score the trees.</figcaption>
  </figure>

  <p>Data files: <a href="data/labeled_sample.csv">labeled_sample.csv</a>, <a href="data/train_set.csv">train_set.csv</a>, and <a href="data/test_set.csv">test_set.csv</a>.</p>

  <h2>Code</h2>
  <p>Data split: <a href="scripts/prep_train_test.py">prep_train_test.py</a>. Decision trees: <a href="scripts/decision_trees.py">decision_trees.py</a>. Both are written in Python and use <code>pandas</code>, <code>scikit-learn</code>, and <code>matplotlib</code>.</p>

  <h2>Results</h2>
  <p>Three different trees were grown, and each was scored on the 1,515 testing planets, where always guessing not habitable would score 98.7%. Tree 1 uses the Gini rule with a depth limit of 3. It reached 99.1% accuracy, found 18 of the 20 habitable planets, and wrongly flagged 12 others, so 60% of the planets it flagged are habitable. Its first question is about the host star's temperature, with a cutoff of 3,098 K that singles out very cool stars, followed by questions about the planet's equilibrium temperature, radius, and orbital period. Tree 2 swaps in the entropy rule and keeps the depth limit of 3. It reached 98.9%, again found 18 of 20, and raised 15 false alarms. It opens with the planet's equilibrium temperature, with a cutoff near 337 K, and then asks about radius, with a cutoff near 3.1 Earth radii. Tree 3 goes back to Gini, allows a depth of 4, and gives the rare habitable class extra weight while growing. It reached 97.7%, which is below the always-no baseline, and it found the same number of habitable planets, 18 of 20, but raised 33 false alarms. Because non-habitable planets vastly outnumber habitable ones, every extra false alarm costs accuracy, which is why the tree with the most false alarms has the lowest score.</p>

  <figure>
    <img src="assets/m3/dt_tree_1.png" alt="Tree 1, grown with the Gini rule to a depth of 3">
    <figcaption>Tree 1 (Gini, depth 3). Boxes outlined in gold are final answers that predict habitable.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/dt_tree_2.png" alt="Tree 2, grown with the entropy rule to a depth of 3">
    <figcaption>Tree 2 (entropy, depth 3) asks a different first question than Tree 1 but arrives at a similar rule.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/dt_tree_3.png" alt="Tree 3, grown with the Gini rule to a depth of 4 with balanced class weights">
    <figcaption>Tree 3 (Gini, depth 4, balanced class weights) is allowed one more level and weights the habitable class more heavily.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/dt_confusion_matrices.png" alt="Confusion matrices for the three trees">
    <figcaption>All three trees miss 2 of the 20 habitable planets and differ mainly in how many non-habitable planets they wrongly flag.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/dt_feature_importance.png" alt="Bar chart of which measurements Tree 1 relies on">
    <figcaption>Tree 1 leans most on planet radius (about 54%), then equilibrium temperature (about 21%) and host star temperature (about 18%).</figcaption>
  </figure>

  <h2>Conclusions</h2>
  <p>The trees point to a simple profile for a planet the catalog lists as habitable. In the labeled data, those planets have radii between 0.8 and 3.0 Earth radii and a median equilibrium temperature of 266 K, and the trees keep returning to the same few measurements to find them: a moderate equilibrium temperature, a small to medium size, and in Tree 1 a very cool host star. Tree 3 relies on equilibrium temperature for about 82% of its importance and radius for the remaining 18%. This is a much better balance than Naive Bayes reached, since all three trees found 18 of the 20 habitable planets in the testing set while raising between 12 and 33 false alarms, against 253 for Naive Bayes with equal priors. The result also supports the earlier clustering finding: there is no sharp wall around habitable planets, but there is a recognizable region of measurement space where most of them sit. Two cautions apply. The catalog's habitable criteria are built from quantities closely related to these same measurements, so the trees are partly rediscovering the catalog's own rules. And with only 20 habitable planets in the testing set, each planet is worth five points of recall, and the trees used simple depth limits and were not tuned, so the exact numbers should be read as rough.</p>
"""
    page("dectrees", "Decision Trees", dt_inner)


    # --- Regression ---
    reg_inner = """
  <p class="eyebrow">Regression</p>
  <h1>Regression</h1>

  <h2>Overview</h2>
  <p>Linear regression predicts a number, such as a planet's mass, by finding the straight line (or, with several predictors, the flat surface) that keeps the total squared error between its predictions and the actual values as small as possible. Each predictor gets a coefficient that says how much the prediction changes when that predictor rises by one unit and the others stay fixed. Logistic regression predicts a category instead, here habitable or not habitable. It still builds a linear score from the predictors, but passes that score z through the sigmoid, p = 1 / (1 + e<sup>-z</sup>), which squeezes any number into a probability between 0 and 1. The probability becomes a class by comparing it to a threshold, usually 0.5, so a positive score means class 1 and a negative score means class 0. A straight line fitted to yes/no labels would predict values below 0 and above 1, which is why logistic regression is used for classification.</p>

  <figure>
    <img src="assets/m4/lin_reg_concept.png" alt="Linear regression best-fit line with the errors it tries to minimize">
    <figcaption>Linear regression chooses the line that makes the total of the squared vertical gaps as small as possible (hypothetical data).</figcaption>
  </figure>

  <figure>
    <img src="assets/m4/lin_vs_logit.png" alt="A straight line and a logistic curve fitted to yes/no data">
    <figcaption>On yes/no data a straight line drifts outside the 0 to 1 range, while the logistic curve stays between them.</figcaption>
  </figure>

  <figure>
    <img src="assets/m4/sigmoid_curve.png" alt="The sigmoid function with the 0.5 threshold marked">
    <figcaption>The sigmoid maps any linear score to a probability, and the 0.5 threshold turns that probability into a class.</figcaption>
  </figure>

  <p>The two methods also differ in what their coefficients mean. In linear regression a coefficient is a change in the predicted number. In logistic regression the linear score is the log of the odds, ln(p / (1 - p)), so a coefficient b means the odds are multiplied by e<sup>b</sup> for each one-unit increase in that predictor. Logistic regression is fitted by maximizing the likelihood of the observed labels, not by minimizing squared error. Both assume the relationship is a straight line after transformation, which is a real limit: a habitable window in temperature, neither too hot nor too cold, cannot be written as a single straight-line effect.</p>

  <h2>Data Prep</h2>
  <p>Regression uses the same labeled data and the same split as Naive Bayes and Decision Trees: 5,047 planets divided at random into a training set of 3,532 planets (46 habitable) and a testing set of 1,515 planets (20 habitable), with no planet in both. The sets must be disjoint so that the scores describe planets the model never saw. For linear regression the target is a number, planet mass (<code>pl_bmasse</code>), and the predictors are the other seven measurements: orbital period, radius, equilibrium temperature, host star temperature, host star radius, host star mass, and system distance. All were log-transformed, since they span several orders of magnitude and mass against radius is close to a straight line on log-log axes. For logistic regression the label is <code>habitable</code>, 0 or 1, and the predictors are all eight measurements, log-transformed and then standardized with a scaler fit on the training set only, so that coefficients are comparable.</p>

  <figure>
    <img src="assets/m3/labeled_preview.png" alt="Preview of the labeled data">
    <figcaption>A sample of the labeled data: eight measurements per planet and the habitable label.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/train_preview.png" alt="Preview of the training set">
    <figcaption>A sample of the training set, 3,532 planets (46 habitable), used to fit both models.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/test_preview.png" alt="Preview of the testing set">
    <figcaption>A sample of the testing set, 1,515 planets (20 habitable), used only to score them.</figcaption>
  </figure>

  <p>One property of the data matters here. 2,550 of the training planets and 1,133 of the testing planets have a mass and radius within 1% of a published mass-radius formula, which suggests one of the two values was estimated from the other and not measured. Results below are therefore reported for all planets and also for the planets that are off that curve. Data files: <a href="data/labeled_sample.csv">labeled_sample.csv</a>, <a href="data/train_set.csv">train_set.csv</a>, and <a href="data/test_set.csv">test_set.csv</a>.</p>

  <h2>Code</h2>
  <p>Data split: <a href="scripts/prep_train_test.py">prep_train_test.py</a>. Linear and logistic regression: <a href="scripts/regression.py">regression.py</a>. Both are written in Python and use <code>pandas</code>, <code>scikit-learn</code>, and <code>matplotlib</code>.</p>

  <h2>Results</h2>
  <p>Linear regression, fitted on all training planets, predicts log10 mass on the testing set with an RMSE of 0.395, an MAE of 0.240, and an R<sup>2</sup> of 0.84. In plain terms the typical error is a factor of about 2.5 (RMSE) or 1.7 (MAE) in mass, compared with an RMSE of 1.00 for always guessing the training average. That headline number is flattered by the formula-based planets. On the 1,133 testing planets that sit on the mass-radius curve the R<sup>2</sup> is 0.93, because for them mass is nearly a formula of radius, while on the other 382 planets it falls to 0.53. A second model trained and tested only on planets off the curve (982 training and 382 testing planets) reaches an R<sup>2</sup> of 0.62, an RMSE of 0.576, and an MAE of 0.408, a typical error of a factor of about 3.8 (RMSE) or 2.6 (MAE), against a baseline RMSE of 0.94. That is the fairer measure of predicting a mass that was actually measured.</p>

  <figure>
    <img src="assets/m4/lin_pred_vs_actual.png" alt="Predicted versus actual log mass, colored by whether the planet sits on the mass-radius formula curve">
    <figcaption>Planets on the formula curve (teal) hug the diagonal, while planets off it (gold) scatter widely around it.</figcaption>
  </figure>

  <p>Two coefficients can be read in plain words. The radius coefficient is 2.09 in the all-planets model, so doubling a planet's radius multiplies its predicted mass by about 4.3 (2 raised to the power 2.09) with the other measurements held fixed. In the model on measured planets it is 1.68, a factor of about 3.2 per doubling. The orbital period coefficient is 0.29 (0.35 in the measured-only model), so doubling the period raises the predicted mass by about 22% (27%). The temperature and host star coefficients should not be read this way, because they change a great deal between the two models: those measurements move together, which makes their individual effects unstable.</p>

  <figure>
    <img src="assets/m4/lin_coefficients.png" alt="Bar chart of the linear regression coefficients">
    <figcaption>Planet radius dominates the all-planets model, which is the mass-radius relationship showing through.</figcaption>
  </figure>

  <p>Logistic regression was fitted two ways, because the habitable class is so rare. With default settings it reached 98.9% accuracy on the testing set, above the 98.7% of always guessing not habitable, found 6 of the 20 habitable planets, and raised 2 false alarms, so 75% of its flags were correct. With balanced class weights it found all 20 habitable planets, but accuracy fell to 94.9% because it raised 78 false alarms, so about 20% of its flags were correct. For the odds, take the default model's radius coefficient of -2.16 on the standardized scale: a planet one standard deviation larger in log radius has its odds of being habitable multiplied by e<sup>-2.16</sup>, about 0.11, so roughly nine times lower, with the other measurements fixed. The orbital period coefficient of +1.62 multiplies the odds by about 5.1 per standard deviation.</p>

  <figure>
    <img src="assets/m4/logit_confusion_matrices.png" alt="Confusion matrices for logistic regression with default and balanced settings">
    <figcaption>The default model is precise but misses most habitable planets, while the balanced model misses none and flags 78 extra planets.</figcaption>
  </figure>

  <figure>
    <img src="assets/m4/logit_coefficients.png" alt="Bar chart of logistic regression coefficients">
    <figcaption>Larger planets and hotter planets and stars lower the odds of habitable, and longer orbital periods raise them.</figcaption>
  </figure>

  <p>Compared with Naive Bayes on the same 1,515 testing planets, logistic regression does better on both counts. Naive Bayes with a learned prior never predicted habitable (98.7%, none found), and with equal priors it found 19 of 20 but raised 253 false alarms (83.2% accuracy, 7% of flags correct). Default logistic regression has higher accuracy than either Naive Bayes model, and balanced logistic regression found all 20 with 78 false alarms, about three times fewer false alarms than Naive Bayes needed for one fewer planet found. A likely reason, not tested here, is that logistic regression weighs the correlated measurements together, while Naive Bayes treats each as independent evidence.</p>

  <figure>
    <img src="assets/m4/logit_vs_nb.png" alt="Accuracy, recall, and precision for Naive Bayes and logistic regression">
    <figcaption>Logistic regression reaches the same or better recall with far higher precision than Naive Bayes on the same testing planets.</figcaption>
  </figure>

  <h2>Conclusions</h2>
  <p>Mass can be estimated from a planet's other measurements, but the estimate is much rougher than the headline score suggests. Across all planets the typical error is about a factor of 2.5, yet much of that accuracy comes from the archive having already filled in many masses from a radius formula, and for planets where mass was measured the typical error is nearer a factor of 4. For the central question, logistic regression is a more efficient shortlist builder than Naive Bayes. The balanced version flagged 98 of 1,515 planets and caught all 20 habitable ones, which cuts a large catalog down to a list short enough to follow up. It also carries a clear limit: a straight-line score cannot describe a habitable window in temperature, and the Part 3 trees, which can, found 18 of 20 with only 12 false alarms. Three cautions apply. All 20 habitable planets in the testing set sit on the mass-radius curve, so their masses and radii are partly estimates. With only 20 positive planets, one planet moves recall by five percentage points. And the habitable label itself is built from quantities closely related to these same measurements, so some of what the models learn is the catalog's own rule.</p>
"""
    page("regression", "Regression", reg_inner)

    # --- AdaBoost ---
    ada_inner = """
  <p class="eyebrow">AdaBoost</p>
  <h1>AdaBoost</h1>

  <h2>Overview</h2>
  <p>Boosting builds one strong classifier out of many weak ones that are trained one after another, each aimed at the mistakes of the models before it. That is the key difference from bagging, as in a random forest, where many trees are grown independently on random resamples of the data and then averaged. Bagging mainly reduces how much a single tree's answer jumps around, while boosting mainly reduces the systematic errors of a simple model by keeping attention on the cases it keeps getting wrong.</p>

  <figure>
    <img src="assets/m4/boosting_vs_bagging.png" alt="Schematic comparing bagging, with independent trees, to boosting, with sequential stumps">
    <figcaption>Bagging builds independent trees side by side, while boosting builds stumps in sequence and reweights the data between them.</figcaption>
  </figure>

  <p>AdaBoost, short for adaptive boosting, usually uses decision stumps as its weak learners: trees with a single split, a barely better-than-guessing rule such as one question about one measurement. Every row of training data starts with the same weight, 1/n. In each round a stump is fitted to the weighted rows, so a row with a larger weight counts for more. The stump's weighted error is the total weight of the rows it gets wrong, and its vote weight is alpha = 1/2 ln((1 - error) / error). Alpha is large when the error is small, zero when the stump is no better than a coin flip, and negative if it is worse. The rows are then reweighted: wrongly classified rows are multiplied by e<sup>alpha</sup> and correctly classified rows by e<sup>-alpha</sup>, and the weights are rescaled to sum to 1, so the next stump is pushed toward the rows that have been hardest. After all rounds, each stump votes for a class, its vote is multiplied by its alpha, and the class with the larger total wins. The scikit-learn version of the formula drops the factor of one half, which doubles every alpha but changes neither the relative reweighting nor the winner of the vote.</p>

  <figure>
    <img src="assets/m4/ada_rounds_toy.png" alt="Three rounds of AdaBoost on a toy dataset with point size showing weight, and the final weighted vote">
    <figcaption>On a toy dataset, mistakes in each round get larger weights, and the three stumps together, voting by alpha, follow the diagonal boundary that no single stump can.</figcaption>
  </figure>

  <figure>
    <img src="assets/m4/ada_alpha_curve.png" alt="Alpha as a function of stump error, and an example of a weighted vote">
    <figcaption>A stump with a low error earns a large alpha, and the final class is the sign of the alpha-weighted sum of the votes.</figcaption>
  </figure>

  <h2>Data Prep</h2>
  <p>AdaBoost uses the same labeled data and split as the earlier supervised models: 5,047 planets, split at random into a training set of 3,532 (46 habitable) and a testing set of 1,515 (20 habitable), with no planet in both, so the testing set measures performance on planets the model never saw. The eight measurements are already numeric, but scikit-learn's AdaBoost needs numbers only, so a categorical column was added and encoded: how the planet was discovered. One-hot encoding turns each of the 8 discovery methods found in the training set into its own 0/1 column, which gives 8 measurements plus 8 method columns. The columns were built from the training set and the testing set was lined up to the same columns, so a method that appears only in the testing set is ignored. Rounds and learning rate were tuned with five-fold cross-validation inside the training set, which keeps the testing set untouched until the end.</p>

  <figure>
    <img src="assets/m4/ada_onehot_preview.png" alt="One-hot encoding of discovery method into 0/1 columns">
    <figcaption>The one-hot step: one example planet per discovery method, with the method turned into 0/1 columns.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/train_preview.png" alt="Preview of the training set">
    <figcaption>A sample of the training set, 3,532 planets (46 habitable), the planets AdaBoost was fitted on.</figcaption>
  </figure>

  <figure>
    <img src="assets/m3/test_preview.png" alt="Preview of the testing set">
    <figcaption>A sample of the testing set, 1,515 planets (20 habitable), used only to score the final models.</figcaption>
  </figure>

  <p>Data files: <a href="data/labeled_sample.csv">labeled_sample.csv</a>, <a href="data/train_set.csv">train_set.csv</a>, and <a href="data/test_set.csv">test_set.csv</a>, with the discovery method taken from <a href="data/exoplanets_clean.csv">exoplanets_clean.csv</a>.</p>

  <h2>Code</h2>
  <p>Data split: <a href="scripts/prep_train_test.py">prep_train_test.py</a>. AdaBoost: <a href="scripts/adaboost.py">adaboost.py</a>. Both are written in Python and use <code>pandas</code>, <code>scikit-learn</code>, and <code>matplotlib</code>.</p>

  <h2>Results</h2>
  <p>Validation accuracy was tracked as boosting rounds were added, for four learning rates. A learning rate of 0.01 never rose above the 98.7% of always guessing not habitable in 200 rounds, and 0.1 only began to improve after about 130 rounds. Rates of 0.5 and 1.0 climbed within the first 25 to 50 rounds, and the rate of 1.0 leveled off near 99.3% to 99.4% after about 90 rounds, though the curve is noisy. Because accuracy has a floor of 98.7%, the settings were chosen by F1 on the habitable class instead, which does react to finding the rare planets. The best setting was a learning rate of 1.0 with 151 rounds, at a validation F1 of 0.75 and a validation accuracy of 99.4%. That setting sits at the top edge of the learning rates tried and the curve is noisy, so nearby settings would likely do about as well.</p>

  <figure>
    <img src="assets/m4/ada_tuning.png" alt="Validation accuracy and F1 as boosting rounds are added, for four learning rates">
    <figcaption>Higher learning rates reach good performance in far fewer rounds, and accuracy barely moves compared with F1 because habitable planets are so rare.</figcaption>
  </figure>

  <p>On the 1,515 testing planets, AdaBoost with default settings (50 rounds, learning rate 1.0) reached 99.3% accuracy, found 13 of the 20 habitable planets, and raised 4 false alarms. The tuned model (151 rounds) reached 99.3%, found the same 13, and raised 3 false alarms, so 81% of its flags were correct. Adding the one-hot discovery-method columns made no difference to the test result, and the tuned model leans mostly on equilibrium temperature (about 43% of the importance), then planet radius (19%), host star temperature (14%), and orbital period (14%). The alpha values show the mechanism at work: the first stump has an error of 0.013, equal to the share of habitable planets in the training set, so it essentially votes not habitable for every planet and earns a very large alpha of 4.3. Later stumps, forced by the growing weights to focus on the rare habitable planets, have larger errors (0.058, then 0.19) and smaller alphas (2.8, then 1.4).</p>

  <figure>
    <img src="assets/m4/ada_confusion_matrices.png" alt="Confusion matrices for AdaBoost with default and tuned settings">
    <figcaption>Tuning removed one false alarm and left the same 13 habitable planets found and 7 missed.</figcaption>
  </figure>

  <figure>
    <img src="assets/m4/ada_alpha_by_round.png" alt="Alpha of each stump in the first 30 rounds of the tuned model">
    <figcaption>The first stump gets by far the largest vote, and later stumps, which tackle the hard cases, carry less.</figcaption>
  </figure>

  <figure>
    <img src="assets/m4/ada_feature_importance.png" alt="Feature importance for the tuned AdaBoost model">
    <figcaption>Equilibrium temperature and planet radius carry most of the weight, with discovery method contributing almost nothing.</figcaption>
  </figure>

  <p>Against the Part 3 decision tree (Tree 1, Gini, depth 3), AdaBoost is better on accuracy and precision but worse on recall. The tree scored 99.1%, found 18 of 20 habitable planets, and raised 12 false alarms (60% of flags correct), against 99.3%, 13 of 20, and 3 false alarms (81%) for tuned AdaBoost. AdaBoost made 10 mistakes in total against 14 for the tree, an accuracy gain of 0.26 percentage points, but the tree missed 2 habitable planets where AdaBoost missed 7. The two end up essentially tied on F1, at about 0.72 each, so which did best depends on what matters: AdaBoost for a short, precise list, and the tree for missing fewer. With only 20 habitable planets in the testing set, neither difference should be over-read.</p>

  <figure>
    <img src="assets/m4/ada_vs_tree.png" alt="Accuracy, recall, and precision for the Part 3 decision tree and AdaBoost">
    <figcaption>AdaBoost trades recall for precision compared with the single tree, and the two have nearly the same overall balance.</figcaption>
  </figure>

  <h2>Conclusions</h2>
  <p>Boosting many simple stumps beat a single tree slightly on overall accuracy, but not on the thing that matters most for finding habitable planets, which is missing as few as possible. The models built so far form a spectrum: balanced logistic regression flagged 98 planets and caught all 20 habitable ones, the decision tree flagged 30 and caught 18, and AdaBoost flagged 16 and caught 13. Which is best depends on the cost of looking at a wrong planet against the cost of overlooking a right one, which for scarce telescope time is a real trade-off. Every model leans on the same few measurements, equilibrium temperature first and planet size second, so the profile of a candidate is stable even when the shortlists differ. Cautions carry over: only 20 habitable planets are in the testing set, many masses and radii are estimates tied together by a formula, and the label is built from quantities closely related to these same measurements.</p>
"""
    page("adaboost", "AdaBoost", ada_inner)

    # --- model tabs ---
    model_tabs = {
        "gradientboosting": ("Gradient Boosting", "a later module"),
        "xgboost":          ("XGBoost", "a later module"),
    }
    for slug, (title, module_note) in model_tabs.items():
        model_stub(slug, title, f"Content added in {module_note}")


    # --- Conclusions ---
    conclusions_inner = f"""
  <p class="eyebrow">Conclusions</p>
  <h1>Conclusions</h1>
  <div class="callout">
    <strong>Answering:</strong> {CENTRAL_QUESTION}
  </div>
  <div class="stub">
    <span class="module-tag">Final deliverable, Module 5</span>
    <p style="margin:0">The non-technical, 5+ paragraph answer belongs here, written in the same plain words as the question above, plus what the analysis could not show and what a next step would look like. No model names or technical jargon in this tab, only what was found and what it means.</p>
  </div>
"""
    page("conclusions", "Conclusions", conclusions_inner)

    # --- About / References ---
    about_inner = """
  <p class="eyebrow">About / References</p>
  <h1>About / References</h1>

  <h2>About</h2>
  <p>Hi, I'm Aayush. I'm a graduate student in the Data Science program at the University of Colorado Boulder's College of Engineering and Applied Science, expected to graduate in May 2027. Before Boulder, I completed an Integrated MSc in Physics at Birla Institute of Technology, Mesra, with a focus on computational and theoretical physics.</p>
  <p>That physics background is part of why this project's topic appealed to me. Exoplanet discovery and habitability sit right at the intersection of the kind of observational data I used to work with and the machine learning methods this course is building up module by module.</p>
  <p>I recently completed a remote internship at Ve-Lyra Labs in Bengaluru, India, working on retrieval-augmented generation pipelines and multi-agent architectures. I'm currently looking for data science and machine learning internships, entry-level roles, and full-time positions in the US.</p>
  <div class="callout">
    Add a line or two here about what you enjoy outside of coursework, a hobby, a side project, or what first got you interested in physics or machine learning.
  </div>

  <h2>References</h2>
  <p>NASA Exoplanet Archive. California Institute of Technology, operated for NASA's Exoplanet Exploration Program. <a href="https://exoplanetarchive.ipac.caltech.edu/">exoplanetarchive.ipac.caltech.edu</a></p>
  <div class="section-card">
    <p style="margin:0">This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program. Data are freely available and carry no reuse restriction.</p>
  </div>

  <p>Planetary Habitability Laboratory. Habitable Worlds Catalog. University of Puerto Rico at Arecibo. <a href="https://phl.upr.edu/hwc">phl.upr.edu/hwc</a></p>
  <div class="section-card">
    <p style="margin-bottom:0.6em">Credit: The Planetary Habitability Laboratory @ UPR Arecibo (<a href="https://phl.upr.edu/">phl.upr.edu</a>). Content and data are licensed under a <a href="https://phl.upr.edu/phl-website-content-license">Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License</a>, for non-commercial, academic use only.</p>
    <p style="margin:0"><code>data/hwc_full.csv</code> on this site is a direct copy of PHL data, and <code>data/exoplanets_clean.csv</code> builds on it by merging in habitability labels, so both files carry the same license forward: attribution required, non-commercial use only, share-alike if redistributed further.</p>
  </div>

  <h2>Code</h2>
  <p>Full source for this site and its data-gathering scripts: <a href="https://github.com/Aayushx9">github.com/Aayushx9</a></p>

  <p>Contact: aayushchinmay@gmail.com</p>
"""
    page("about_references", "About / References", about_inner)

    print("Built", len(NAV_LINKS), "pages.")


if __name__ == "__main__":
    build()
