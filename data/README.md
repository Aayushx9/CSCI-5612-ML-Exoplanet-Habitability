# Data sources and licensing

## exoplanets_raw.csv
Pulled from the NASA Exoplanet Archive (exoplanetarchive.ipac.caltech.edu) via its
public TAP API, `pscomppars` table. NASA Exoplanet Archive data are freely available
with no reuse restriction. Standard acknowledgment:

> This research has made use of the NASA Exoplanet Archive, which is operated by
> the California Institute of Technology, under contract with the National
> Aeronautics and Space Administration under the Exoplanet Exploration Program.

## hwc_full.csv
A direct copy of the Planetary Habitability Laboratory's Habitable Worlds Catalog
(phl.upr.edu/hwc/data), downloaded as a CSV.

Credit: The Planetary Habitability Laboratory @ UPR Arecibo (phl.upr.edu).
Licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0
Unported License (https://phl.upr.edu/phl-website-content-license). Non-commercial,
academic use only. Not endorsed by PHL.

## exoplanets_clean.csv
Derived from exoplanets_raw.csv, merged with habitability labels and the Earth
Similarity Index from hwc_full.csv. Because this file builds on PHL's licensed
data, it carries the same license forward: attribution required, non-commercial
use only, share-alike if redistributed further.
