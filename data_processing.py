
"""
data_processing.py
==================
Extracts and merges socioeconomic and crime data from Eurostat and World Bank Excel files.

Sources:
  - Eurostat: crim_hom_soff (intentional homicide per 100k), tipsun20 (unemployment rate)
  - World Bank: NY.GDP.PCAP.CD (GDP per capita), SI.POV.GINI (Gini index),
                SP.URB.TOTL.IN.ZS (urban population %)

Countries: Portugal, Spain, France, Germany, Italy, Netherlands
Years: 2015-2022

Output: Merged pandas DataFrame with 48 rows × 7 columns.
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------

COUNTRIES = ["Portugal", "Spain", "France", "Germany", "Italy", "Netherlands"]
YEARS = list(range(2015, 2023))

# Expected Excel filenames
FILE_GDP = "API_NY.GDP.PCAP.CD_DS2_en_excel_v2_478015.xls"
FILE_GINI = "API_SI.POV.GINI_DS2_en_excel_v2_459602.xls"
FILE_URBAN = "API_SP.URB.TOTL.IN.ZS_DS2_en_excel_v2_477768.xls"
FILE_HOMICIDE = "crim_hom_soff$defaultview_spreadsheet.xlsx"
FILE_UNEMPLOYMENT = "tipsun20_page_spreadsheet.xlsx"

# ---------------------------------------------------------------------------
# WORLD BANK DATA
# ---------------------------------------------------------------------------

def load_worldbank_data():
    """Load GDP, Gini, and urban population from World Bank Excel files."""
    df_gdp = pd.read_excel(FILE_GDP, sheet_name="Data", skiprows=3)
    df_gini = pd.read_excel(FILE_GINI, sheet_name="Data", skiprows=3)
    df_urban = pd.read_excel(FILE_URBAN, sheet_name="Data", skiprows=3)
    return df_gdp, df_gini, df_urban


def extract_worldbank_variable(df, variable_name):
    """Extract a World Bank variable for the configured countries and years."""
    records = []
    for country in COUNTRIES:
        row = df[df["Country Name"] == country]
        if not row.empty:
            for year in YEARS:
                col = str(year)
                val = row[col].values[0] if col in row.columns else np.nan
                records.append({"country": country, "year": year, variable_name: val})
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# EUROSTAT DATA — HOMICIDES
# ---------------------------------------------------------------------------

def load_homicide_data():
    """Load intentional homicide rate (per 100k) from Eurostat Excel file."""
    df_raw = pd.read_excel(FILE_HOMICIDE, sheet_name="Data", header=None)

    # Locate the table with "Per hundred thousand inhabitants"
    start_row = None
    for i, row in df_raw.iterrows():
        if "Per hundred thousand inhabitants" in " ".join(row.astype(str)):
            start_row = i
            break

    if start_row is None:
        raise ValueError("Could not find 'Per hundred thousand inhabitants' in homicide file.")

    header_row = start_row + 2
    df = pd.read_excel(FILE_HOMICIDE, sheet_name="Data", skiprows=header_row)
    df = df.rename(columns={df.columns[0]: "geo"})

    # Keep only year columns
    cols = ["geo"] + [str(y) for y in range(2015, 2023)]
    df = df[cols]
    return df


def extract_homicide(df):
    """Extract homicide rates for configured countries."""
    records = []
    for country in COUNTRIES:
        row = df[df["geo"] == country]
        if not row.empty:
            for year in YEARS:
                col = str(year)
                val = row[col].values[0]
                val = clean_value(val)
                records.append({"country": country, "year": year, "crime_rate": val})
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# EUROSTAT DATA — UNEMPLOYMENT
# ---------------------------------------------------------------------------

def load_unemployment_data():
    """Load unemployment rate from Eurostat Excel file."""
    df_raw = pd.read_excel(FILE_UNEMPLOYMENT, sheet_name="Data", header=None)

    header_row = None
    for i, row in df_raw.iterrows():
        if "TIME" in " ".join(row.astype(str)):
            header_row = i
            break

    if header_row is None:
        raise ValueError("Could not find header in unemployment file.")

    df = pd.read_excel(FILE_UNEMPLOYMENT, sheet_name="Data", skiprows=header_row)
    df = df.rename(columns={df.columns[0]: "geo"})

    cols = ["geo"] + [str(y) for y in range(2015, 2023)]
    df = df[cols]
    return df


def extract_unemployment(df):
    """Extract unemployment rates for configured countries."""
    records = []
    for country in COUNTRIES:
        row = df[df["geo"] == country]
        if not row.empty:
            for year in YEARS:
                col = str(year)
                val = row[col].values[0]
                val = clean_value(val)
                records.append({"country": country, "year": year, "unemployment": val})
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# UTILS
# ---------------------------------------------------------------------------

def clean_value(val):
    """Convert Eurostat missing marker ':' to NaN, otherwise float."""
    if isinstance(val, str):
        val = val.strip()
        if val in (":", ""):
            return np.nan
        try:
            return float(val)
        except ValueError:
            return np.nan
    return val


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def build_dataset():
    """Run full extraction pipeline and return merged DataFrame."""
    print("Loading World Bank data...")
    df_gdp, df_gini, df_urban = load_worldbank_data()

    print("Extracting GDP...")
    df_gdp_clean = extract_worldbank_variable(df_gdp, "gdp_per_capita")

    print("Extracting Gini...")
    df_gini_clean = extract_worldbank_variable(df_gini, "gini")

    print("Extracting urban population...")
    df_urban_clean = extract_worldbank_variable(df_urban, "urban_population")

    print("Loading homicide data...")
    df_homicide = load_homicide_data()
    df_homicide_clean = extract_homicide(df_homicide)

    print("Loading unemployment data...")
    df_unemployment = load_unemployment_data()
    df_unemp_clean = extract_unemployment(df_unemployment)

    print("Merging...")
    df = df_gdp_clean
    df = df.merge(df_gini_clean, on=["country", "year"], how="left")
    df = df.merge(df_urban_clean, on=["country", "year"], how="left")
    df = df.merge(df_homicide_clean, on=["country", "year"], how="left")
    df = df.merge(df_unemp_clean, on=["country", "year"], how="left")

    print(f"Done. Dataset: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


if __name__ == "__main__":
    df = build_dataset()
    print(df.head(12))
