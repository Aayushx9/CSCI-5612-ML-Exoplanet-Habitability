"""
Generates the static HTML pages for the exoplanet project site from
a shared template. Run this locally whenever page content changes;
it is a build helper and is not itself part of the published site.

Tab structure follows the professor's Week 3 requirements:
Introduction (landing page) -> Data Gathering -> Cleaning & Prep -> EDA
-> one tab per model -> Conclusions -> About / References
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

NAV_LINKS = [
    ("index.html", "Introduction"),
    ("data_gathering.html", "Data Gathering"),
    ("cleaning_prep.html", "Cleaning &amp; Prep"),
    ("eda.html", "EDA"),
    ("clustering.html", "Clustering"),
    ("pca.html", "PCA"),
    ("naivebayes.html", "NaiveBayes"),
    ("dectrees.html", "DecTrees"),
    ("svms.html", "SVMs"),
    ("regression.html", "Regression"),
    ("nn.html", "NN"),
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


def write(slug, html):
    with open(f"{slug}.html", "w") as f:
        f.write(html)


def page(slug, title, body):
    write(slug, HEAD.format(title=title) + nav(f"{slug}.html") + body + FOOT)


def model_stub(slug, title, module_note):
    body = f"""
<main>
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
</main>
"""
    page(slug, title, body)


def build():
    # --- Introduction (landing page) ---
    intro_body = f"""
<main>
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
</main>
"""
    page("index", "Introduction", intro_body)

    # --- Data Gathering ---
    gathering_body = """
<main>
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
    <p style="margin-bottom:0.6em">Website: <a href="https://phl.upr.edu/hwc">phl.upr.edu/hwc</a>, maintained by the Planetary Habitability Laboratory, University of Puerto Rico at Arecibo.</p>
    <p style="margin:0">Downloaded directly, not via API, to cross-reference computed habitability indices, including the Earth Similarity Index, habitable-zone distance, and habitable-zone classification, against the raw planetary parameters pulled from the Exoplanet Archive.</p>
  </div>

  <div class="stub">
    <span class="module-tag">To be added</span>
    <p style="margin:0">A small preview of the raw data as pulled, before any cleaning, with a link to the full raw file.</p>
  </div>
</main>
"""
    page("data_gathering", "Data Gathering", gathering_body)

    # --- Cleaning & Prep ---
    cleaning_body = """
<main>
  <p class="eyebrow">Cleaning &amp; Prep</p>
  <h1>Cleaning &amp; Prep</h1>
  <div class="stub">
    <span class="module-tag">To be added</span>
    <p style="margin:0 0 1em">This tab will show, side by side, what the raw data looked like and what it looked like after cleaning: missing values handled, incorrect or impossible values corrected, units standardized, and any columns added, removed, or normalized. Each step will be explained in plain language, not just shown.</p>
    <p style="margin:0"><strong>Planned before/after items:</strong> missing radius, mass, or temperature values; unit consistency across NASA Exoplanet Archive and PHL Habitable Worlds Catalog columns; outlier orbital periods and masses; merging the two sources into one working table keyed by planet name.</p>
  </div>
</main>
"""
    page("cleaning_prep", "Cleaning & Prep", cleaning_body)

    # --- EDA ---
    eda_body = """
<main>
  <p class="eyebrow">EDA</p>
  <h1>Exploratory Data Analysis</h1>
  <div class="stub">
    <span class="module-tag">To be added</span>
    <p style="margin:0">At least ten visualizations exploring distributions and relationships in the cleaned data will go here, each with a title, labeled axes, and one sentence of takeaway explaining what it shows and why it matters to the central question.</p>
  </div>
</main>
"""
    page("eda", "EDA", eda_body)

    # --- model tabs ---
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
        model_stub(slug, title, f"Content added in {module_note}")

    # --- Conclusions ---
    conclusions_body = f"""
<main>
  <p class="eyebrow">Conclusions</p>
  <h1>Conclusions</h1>
  <div class="callout">
    <strong>Answering:</strong> {CENTRAL_QUESTION}
  </div>
  <div class="stub">
    <span class="module-tag">Final deliverable, Module 5</span>
    <p style="margin:0">The non-technical, 5+ paragraph answer belongs here, written in the same plain words as the question above, plus what the analysis could not show and what a next step would look like. No model names or technical jargon in this tab, only what was found and what it means.</p>
  </div>
</main>
"""
    page("conclusions", "Conclusions", conclusions_body)

    # --- About / References ---
    about_body = """
<main>
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
  <p>Planetary Habitability Laboratory. Habitable Worlds Catalog. University of Puerto Rico at Arecibo. <a href="https://phl.upr.edu/hwc">phl.upr.edu/hwc</a></p>

  <h2>Code</h2>
  <p>Full source for this site and its data-gathering scripts: <a href="https://github.com/Aayushx9">github.com/Aayushx9</a></p>

  <p>Contact: aayushchinmay@gmail.com</p>
</main>
"""
    page("about_references", "About / References", about_body)

    print("Built", len(NAV_LINKS), "pages.")


if __name__ == "__main__":
    build()
