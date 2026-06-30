
"""
Streamlit Dashboard — Socioeconomic Predictors of Urban Crime in Europe
========================================================================
Interactive exploration of crime rates, unemployment, GDP, and inequality
across 6 European countries (2015-2022).
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---------------------------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Crime & Socioeconomics in Europe",
    page_icon="📊",
    layout="wide"
)

st.title("Socioeconomic Predictors of Urban Crime in Europe")
st.markdown("Portugal · Spain · France · Germany · Italy · Netherlands (2015–2022)")

# ---------------------------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------------------------

@st.cache_data
def load_data():
        return pd.read_csv("dashboard/final_dataset.csv")
df = load_data()

# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------

st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=sorted(df["country"].unique()),
    default=sorted(df["country"].unique())
)

selected_years = st.sidebar.slider(
    "Select year range",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(int(df["year"].min()), int(df["year"].max()))
)

# Filter data
filtered = df[
    (df["country"].isin(selected_countries)) &
    (df["year"] >= selected_years[0]) &
    (df["year"] <= selected_years[1])
]

# ---------------------------------------------------------------------------
# METRICS ROW
# ---------------------------------------------------------------------------

st.subheader("Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    avg_crime = filtered["crime_rate"].mean()
    st.metric("Avg Crime Rate (per 100k)", f"{avg_crime:.2f}")

with col2:
    avg_unemp = filtered["unemployment"].mean()
    st.metric("Avg Unemployment (%)", f"{avg_unemp:.1f}")

with col3:
    avg_gdp = filtered["gdp_per_capita"].mean()
    st.metric("Avg GDP per Capita ($)", f"${avg_gdp:,.0f}")

with col4:
    avg_gini = filtered["gini"].mean()
    st.metric("Avg Gini Index", f"{avg_gini:.1f}")

# ---------------------------------------------------------------------------
# CHART 1: Crime Rate Over Time
# ---------------------------------------------------------------------------

st.subheader("Crime Rate Evolution")

fig1, ax1 = plt.subplots(figsize=(10, 5))
for country in selected_countries:
    data = filtered[filtered["country"] == country].sort_values("year")
    if not data.empty:
        ax1.plot(data["year"], data["crime_rate"], marker="o", label=country, linewidth=2)

ax1.set_xlabel("Year")
ax1.set_ylabel("Crime Rate (per 100,000 inhabitants)")
ax1.legend()
ax1.grid(True, alpha=0.3)
st.pyplot(fig1)

# ---------------------------------------------------------------------------
# CHART 2: Crime vs Unemployment
# ---------------------------------------------------------------------------

st.subheader("Crime Rate vs Unemployment Rate")

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered, x="unemployment", y="crime_rate", hue="country", s=100, ax=ax2)
ax2.set_xlabel("Unemployment Rate (%)")
ax2.set_ylabel("Crime Rate (per 100,000 inhabitants)")
ax2.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
ax2.grid(True, alpha=0.3)
st.pyplot(fig2)

# ---------------------------------------------------------------------------
# CHART 3: Crime vs GDP
# ---------------------------------------------------------------------------

st.subheader("Crime Rate vs GDP per Capita")

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.scatterplot(data=filtered, x="gdp_per_capita", y="crime_rate", hue="country", s=100, ax=ax3)
ax3.set_xlabel("GDP per Capita (current US$)")
ax3.set_ylabel("Crime Rate (per 100,000 inhabitants)")
ax3.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
ax3.grid(True, alpha=0.3)
st.pyplot(fig3)

# ---------------------------------------------------------------------------
# CHART 4: Correlation Heatmap
# ---------------------------------------------------------------------------

st.subheader("Correlation Matrix")

numeric_cols = ["gdp_per_capita", "gini", "urban_population", "crime_rate", "unemployment"]
corr = filtered[numeric_cols].corr()

fig4, ax4 = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, fmt=".2f", square=True, ax=ax4)
st.pyplot(fig4)

# ---------------------------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------------------------

st.subheader("Raw Data")
st.dataframe(filtered.sort_values(["country", "year"]), use_container_width=True)

# ---------------------------------------------------------------------------
# FOOTER
# ---------------------------------------------------------------------------

st.markdown("---")
st.markdown("*Data sources: Eurostat & World Bank · Undergraduate project in Computational Social Science*")
