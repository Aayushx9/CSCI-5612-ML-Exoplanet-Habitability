"""
Generates the static HTML pages for the exoplanet project site from
a shared template. Run this locally whenever page content changes;
it is a build helper and is not itself part of the published site.
"""
import os

PAGES = [
    ("index",        "Home"),
    ("introduction",  "Introduction"),
    ("dataprep_eda",  "DataPrep_EDA"),
    ("clustering",    "Clustering"),
    ("pca",           "PCA"),
    ("naivebayes",    "NaiveBayes"),
    ("dectrees",      "DecTrees"),
    ("svms",          "SVMs"),
    ("regression",    "Regression"),
    ("nn",            "NN"),
    ("conclusions",   "Conclusions"),
    ("about",         "About"),
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Exoplanet Discovery &amp; Habitability</title>
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


def nav(active):
    links = [
        ("index.html", "Home"),
        ("introduction.html", "Introduction"),
        ("dataprep_eda.html", "DataPrep_EDA"),
        ("clustering.html", "Clustering"),
        ("pca.html", "PCA"),
        ("naivebayes.html", "NaiveBayes"),
        ("dectrees.html", "DecTrees"),
        ("svms.html", "SVMs"),
        ("regression.html", "Regression"),
        ("nn.html", "NN"),
        ("conclusions.html", "Conclusions"),
        ("about.html", "About"),
    ]
    items = []
    for href, label in links:
        cls = ' class="active"' if href == f"{active}.html" else ""
        items.append(f'<a href="{href}"{cls}>{label}</a>')
    return (
        '<nav class="topnav">'
        '<span class="brand">Exoplanet Discovery &amp; Habitability</span>'
        + "".join(items)
        + "</nav>"
    )


def stub_page(slug, title, module_note):
    body = f"""
<main>
  <p class="eyebrow">{title}</p>
  <h1>{title}</h1>
  <div class="stub">
    <span class="module-tag">{module_note}</span>
    <p style="margin:0">This tab will hold the Overview, Data, Code, and Results sections for {title}
    once that stage of the project is reached. Structure is in place now so the site's
    navigation stays complete from Module 1 onward.</p>
  </div>
</main>
"""
    return HEAD.format(title=title) + nav(slug) + body + FOOT


def write(slug, html):
    with open(f"{slug}.html", "w") as f:
        f.write(html)


def build():
    os.makedirs("out", exist_ok=True)

    # --- index ---
    index_body = """
<div class="hero">
  <p class="eyebrow">A semester-long Data Science Lifecycle project</p>
  <h1>Exoplanet Discovery &amp; Habitability</h1>
  <p class="lede">What has been found around other stars so far, and how much of it could plausibly support life? This project follows the full data science lifecycle, from gathering and cleaning to exploring, modeling, and communicating, using the public record of confirmed exoplanets.</p>
  <figure>
    <img src="assets/transit-diagram.svg" alt="Diagram of a planet transiting its star and the resulting dip in the star's observed brightness">
    <figcaption>A transiting planet briefly dims its host star's light. This dip is the signal behind most confirmed exoplanet discoveries.</figcaption>
  </figure>
  <p><a href="introduction.html">Start with the Introduction &rarr;</a></p>
</div>
"""
    write("index", HEAD.format(title="Home") + nav("index") + index_body + FOOT)

    # --- introduction ---
    intro_body = """
<main>
  <p class="eyebrow">Introduction</p>
  <h1>Introduction</h1>

  <p>For most of human history, the planets orbiting other stars existed only as speculation. That changed within the last three decades, as advances in telescope sensitivity turned the search for exoplanets into one of the most active fields in astronomy. Missions such as NASA's Kepler Space Telescope and its successor, the Transiting Exoplanet Survey Satellite (TESS), have monitored hundreds of thousands of stars, watching for the tiny, periodic dimming that occurs when a planet passes directly in front of its star. Ground-based observatories have complemented this work by detecting the subtle gravitational wobble a planet induces in the star it orbits. Together, these efforts have confirmed thousands of worlds beyond the Solar System, ranging from scorched gas giants that circle their stars faster than Mercury circles the Sun to small, rocky planets that may resemble Earth in size. Each discovery adds to a growing public catalog, the NASA Exoplanet Archive, which records the physical and orbital properties of every confirmed planet, including its radius, mass, orbital period, and the characteristics of its host star. This catalog has become the primary reference point for astronomers and educators alike, and it is updated continuously as new missions and instruments refine existing measurements or discover new worlds. What began as a search to answer a single question, whether stars other than the Sun have planets, has grown into a broader effort to catalog an entire population of worlds and understand how common planetary systems are throughout the galaxy. The scale of that population, now numbering in the thousands and growing every year, is the starting point for the story of modern exoplanet science.</p>

  <figure>
    <img src="assets/transit-diagram.svg" alt="Diagram of a planet transiting its star and the resulting dip in the star's observed brightness">
    <figcaption>The transit method: a planet crossing its star produces a small, periodic dip in the star's measured brightness.</figcaption>
  </figure>

  <p>Among the thousands of confirmed exoplanets, a smaller and more carefully studied group has drawn particular attention: those that might be capable of supporting life. The question of habitability extends beyond simple existence, asking instead whether a planet's size, temperature, and position around its star place it within the conditions thought necessary for liquid water and a stable climate. The Planetary Habitability Laboratory at the University of Puerto Rico at Arecibo has maintained a running catalog of these candidates for over a decade, ranking known planets according to indices such as the Earth Similarity Index and their position within a star's habitable zone. Interest in this question extends well beyond academic astronomy: educators use potentially habitable worlds to illustrate scientific concepts to students, science communicators and the public follow new candidates with the same curiosity once reserved for missions to Mars, and space agencies weigh habitability findings when prioritizing future telescopes and instruments designed to analyze distant atmospheres for signs of biological activity. At the same time, the criteria used to judge habitability remain incomplete and are still debated among scientists, since every assessment is built from a handful of measurable properties rather than direct observation of a planet's surface or atmosphere. Some planets once considered promising candidates have since been reclassified as measurements improved, and the definition of what counts as an Earth-like world continues to be refined. This tension, between the desire to identify worlds that could host life and the limitations of what can currently be measured from light-years away, sits at the center of exoplanet habitability research today.</p>

  <h2>Questions to explore</h2>
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
</main>
"""
    write("introduction", HEAD.format(title="Introduction") + nav("introduction") + intro_body + FOOT)

    # --- dataprep_eda (partially filled per Module 1 requirements) ---
    dataprep_body = """
<main>
  <p class="eyebrow">DataPrep_EDA</p>
  <h1>Data Preparation &amp; Exploration</h1>

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
    <p style="margin-bottom:0.6em">Website: <a href="https://phl.upr.edu/hwc">phl.upr.edu/hwc</a>, maintained by the Planetary Habitability Laboratory, University of Puerto Rico at Arecibo.</p>
    <p style="margin:0">Downloaded directly (not via API) to cross-reference computed habitability indices, including the Earth Similarity Index, habitable-zone distance, and habitable-zone classification, against the raw planetary parameters pulled from the Exoplanet Archive.</p>
  </div>

  <div class="stub">
    <span class="module-tag">To be added as data collection progresses</span>
    <p style="margin:0">Raw and cleaned data previews, the general cleaning log (missing values, unit conversions, outlier handling), and at least ten exploratory visualizations will be added here.</p>
  </div>
</main>
"""
    write("dataprep_eda", HEAD.format(title="DataPrep_EDA") + nav("dataprep_eda") + dataprep_body + FOOT)

    # --- conclusions stub (slightly different copy than model stubs) ---
    conclusions_body = """
<main>
  <p class="eyebrow">Conclusions</p>
  <h1>Conclusions</h1>
  <div class="stub">
    <span class="module-tag">Final deliverable</span>
    <p style="margin:0">The non-technical, 5+ paragraph closing narrative, covering what was found and what it means for anyone curious about exoplanets and habitability, will be written here once every modeling stage is complete.</p>
  </div>
</main>
"""
    write("conclusions", HEAD.format(title="Conclusions") + nav("conclusions") + conclusions_body + FOOT)

    # --- about stub ---
    about_body = """
<main>
  <p class="eyebrow">About</p>
  <h1>About Me</h1>
  <div class="stub">
    <span class="module-tag">Optional tab</span>
    <p style="margin:0">This is the one tab written in the first person. A short bio can go here.</p>
  </div>
</main>
"""
    write("about", HEAD.format(title="About") + nav("about") + about_body + FOOT)

    # --- remaining model tabs: generated stubs ---
    model_tabs = {
        "clustering":  ("Clustering", "Module 2"),
        "pca":         ("PCA", "Module 2"),
        "naivebayes":  ("Naive Bayes", "Module 3"),
        "dectrees":    ("Decision Trees", "Module 3"),
        "svms":        ("Support Vector Machines", "Module 4"),
        "regression":  ("Regression", "Module 5"),
        "nn":          ("Neural Networks", "Module 5"),
    }
    for slug, (title, module_note) in model_tabs.items():
        write(slug, stub_page(slug, title, f"Content added in {module_note}"))

    print("Built", len(PAGES), "pages.")


if __name__ == "__main__":
    build()
