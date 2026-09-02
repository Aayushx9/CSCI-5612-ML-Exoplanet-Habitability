# fetch_exoplanet_data.py
"""
This code pulls up confirmed exoplanet data from the NASA Exoplanet Archive's public
TAP (Table Access Protocol) API and saves it as a raw CSV for the 
DataPrep_EDA tab of the project. 
"""
import pandas as pd
import requests

# Core TAP endpoint
TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# Columns from the Planetary Systems Composite Parameters table
# (pscomppars): one best estimate row per confirmed planet.
COLUMNS = [
    "pl_name",        # planet name
    "hostname",       # host star name
    "discoverymethod",# transit, radial velocity, imaging, microlensing, etc.
    "disc_year",      # year of discovery
    "pl_orbper",      # orbital period (days)
    "pl_rade",        # planet radius (Earth radii)
    "pl_bmasse",      # planet mass (Earth masses)
    "pl_eqt",         # equilibrium temperature (K)
    "st_teff",        # host star effective temperature (K)
    "st_rad",         # host star radius (solar radii)
    "st_mass",        # host star mass (solar masses)
    "sy_dist",        # system distance from Earth (parsecs)
]


def fetch_raw_data() -> pd.DataFrame:
    query = f"select {','.join(COLUMNS)} from pscomppars"
    params = {"query": query, "format": "csv"}
    response = requests.get(TAP_URL, params=params, timeout=60)
    response.raise_for_status()

    # requests.Response has .url with the final, fully-encoded GET URL.
    # This is the exact request worth citing in the DataPrep_EDA writeup.
    print("Request URL:", response.url)

    from io import StringIO
    return pd.read_csv(StringIO(response.text))


if __name__ == "__main__":
    df = fetch_raw_data()
    df.to_csv("exoplanets_raw.csv", index=False)
    print(f"Saved {len(df)} rows to exoplanets_raw.csv")
    print(df.head())
