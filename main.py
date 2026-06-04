import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from supabase import create_client, Client


def get_secret(key: str):
    """
    First checks Render environment variables.
    If not found, falls back to Streamlit secrets.
    """
    return os.getenv(key) or st.secrets[key]

# Iniitialize connection to db

@st.cache_resource
def init_connection():
    url: str = get_secret("supabase_url")
    key: str = get_secret("supabase_key")

    client: Client = create_client(url, key)
    return client


client = init_connection()

st.set_page_config(
    page_title="WHO Life Expectancy",
    page_icon="🌍",
    layout="wide"
)

# ── Connection & caching ──────────────────────────────────────────────────────
@st.cache_resource
def init_connection() -> Client:
    return create_client(st.secrets["supabase_url"], st.secrets["supabase_key"])

client = init_connection()

@st.cache_data(ttl=600)
def query(table: str) -> pd.DataFrame:
    return pd.DataFrame(client.table(table).select("*").execute().data)

# ── Load all data upfront ─────────────────────────────────────────────────────
with st.spinner("Loading data..."):
    df_overview   = query("mart_overview")
    df_global     = query("global_life_expectancy_trend")
    df_country    = query("country_life_expectancy_trend")
    df_trend      = query("mart_status_life_expectancy_trend")
    df_dist       = query("mart_status_distribution")
    df_box        = query("mart_status_life_expectancy_boxplot")
    df_vac_trend  = query("mart_vaccine_coverage_trend")
    df_vac_sc     = query("mart_vaccine_life_expectancy_scatter")
    df_health     = query("mart_health_factors_scatter")
    df_top        = query("mart_top_10_life_expectancy")
    df_bot        = query("mart_bottom_10_life_expectancy")

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🌍 WHO Life Expectancy Dashboard")
st.caption("Interactive overview of global health indicators · 2000–2015")

# ── Global filters (affect all charts) ───────────────────────────────────────
with st.container():
    fc1, fc2, fc3 = st.columns([1, 1, 2])
    status_filter = fc1.selectbox("Status", ["All", "Developed", "Developing"], key="global_status")
    all_years = sorted(df_box["year"].dropna().astype(int).unique().tolist())
    year_range = fc2.select_slider("Year range", options=all_years, value=(all_years[0], all_years[-1]))
    fc3.write("")  # spacer

def apply_filters(df, status_col="status", year_col="year"):
    d = df.copy()
    if status_filter != "All" and status_col in d.columns:
        d = d[d[status_col] == status_filter]
    if year_col in d.columns:
        d = d[d[year_col].astype(int).between(*year_range)]
    return d

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 1 — KPI cards
# ═══════════════════════════════════════════════════════════════════════════════
row = df_overview.iloc[0]
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Avg life expectancy", f"{row['avg_life_expectancy']} yrs")
k2.metric("Max life expectancy", f"{row['max_life_expectancy']} yrs")
k3.metric("Min life expectancy", f"{row['min_life_expectancy']} yrs")
k4.metric("Total countries",     int(row['total_countries']))
k5.metric("Year range",          f"{int(row['start_year'])}–{int(row['end_year'])}")

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 2 — Global trend + Developed vs Developing bar
# ═══════════════════════════════════════════════════════════════════════════════
col1, col2 = st.columns(2)

with col1:
    st.subheader("Global life expectancy trend")
    df_g = df_global[df_global["year"].astype(int).between(*year_range)]
    fig = px.line(df_g, x="year", y="avg_life_expectancy", markers=True,
                  labels={"avg_life_expectancy": "Avg (yrs)", "year": ""})
    fig.update_traces(line_color="#1D9E75", line_width=2.5)
    fig.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Developed vs developing over time")
    df_t = apply_filters(df_trend, year_col="year")
    fig2 = px.bar(df_t, x="year", y="avg_life_expectancy", color="status", barmode="group",
                  color_discrete_map={"Developed": "#1D9E75", "Developing": "#378ADD"},
                  labels={"avg_life_expectancy": "Avg (yrs)", "year": ""})
    fig2.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)",
                       legend=dict(title="", orientation="h", y=1.1), margin=dict(t=10,b=10))
    st.plotly_chart(fig2, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Country comparison + Donut + Box plot
# ═══════════════════════════════════════════════════════════════════════════════
col3, col4, col5 = st.columns([2, 1, 1])

with col3:
    st.subheader("Country comparison")
    all_countries = sorted(df_country["country"].dropna().unique().tolist())
    defaults = [c for c in ["Thailand","Japan","United States of America","Nigeria","Brazil"] if c in all_countries]
    selected = st.multiselect("Select countries", all_countries, default=defaults, key="cmp")
    if selected:
        df_cmp = df_country[
            df_country["country"].isin(selected) &
            df_country["year"].astype(int).between(*year_range)
        ]
        fig3 = px.line(df_cmp, x="year", y="avg_life_expectancy", color="country", markers=True,
                       labels={"avg_life_expectancy": "Avg (yrs)", "year": ""})
        fig3.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)",
                           legend=dict(title=""), margin=dict(t=10,b=10))
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Select at least one country.")

with col4:
    st.subheader("Country distribution")
    fig4 = px.pie(df_dist, names="status", values="country_count", hole=0.5,
                  color_discrete_sequence=["#1D9E75","#378ADD"])
    fig4.update_traces(textposition="outside", textinfo="percent+label")
    fig4.update_layout(showlegend=False, margin=dict(t=10,b=10,l=10,r=10))
    st.plotly_chart(fig4, use_container_width=True)

with col5:
    st.subheader("Distribution box plot")
    df_bx = apply_filters(df_box, year_col="year")
    fig5 = px.box(df_bx, x="status", y="lifeexpectancy", color="status", points="outliers",
                  color_discrete_map={"Developed": "#1D9E75", "Developing": "#378ADD"},
                  labels={"lifeexpectancy": "Life exp (yrs)", "status": ""})
    fig5.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10))
    st.plotly_chart(fig5, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 4 — Vaccine trend + Vaccine scatter
# ═══════════════════════════════════════════════════════════════════════════════
col6, col7 = st.columns(2)

with col6:
    st.subheader("Vaccine coverage trend")
    df_vt = df_vac_trend[df_vac_trend["year"].astype(int).between(*year_range)]
    fig6 = go.Figure()
    vac_map = {
        "avg_hepatitisb_vaccine_coverage": ("Hepatitis B", "#1D9E75", "solid"),
        "avg_polio_vaccine_coverage":      ("Polio",       "#378ADD", "dash"),
        "avg_diphtheria_vaccine_coverage": ("Diphtheria",  "#D85A30", "dot"),
    }
    for col_name, (label, color, dash) in vac_map.items():
        fig6.add_trace(go.Scatter(x=df_vt["year"], y=df_vt[col_name], name=label,
                                  mode="lines+markers",
                                  line=dict(color=color, width=2, dash=dash)))
    fig6.update_layout(hovermode="x unified", plot_bgcolor="rgba(0,0,0,0)",
                       yaxis_title="Coverage (%)", xaxis_title="",
                       legend=dict(title="", orientation="h", y=1.1), margin=dict(t=10,b=10))
    st.plotly_chart(fig6, use_container_width=True)

with col7:
    st.subheader("Vaccine vs life expectancy")
    vaccine_opts = {
        "hepatitisb_vaccine_coverage": "Hepatitis B",
        "polio_vaccine_coverage":      "Polio",
        "diphtheria_vaccine_coverage": "Diphtheria",
    }
    vax = st.selectbox("Vaccine", list(vaccine_opts.keys()),
                       format_func=lambda x: vaccine_opts[x], key="vax_sel")
    df_vs = apply_filters(df_vac_sc, year_col="year").dropna(subset=[vax, "lifeexpectancy"])
    fig7 = px.scatter(df_vs, x=vax, y="lifeexpectancy", color="status", opacity=0.5,
                      trendline="ols",
                      color_discrete_map={"Developed": "#1D9E75", "Developing": "#378ADD"},
                      labels={vax: f"{vaccine_opts[vax]} coverage (%)", "lifeexpectancy": "Life exp (yrs)"},
                      hover_data=["country", "year"])
    fig7.update_layout(plot_bgcolor="rgba(0,0,0,0)", legend=dict(title=""),
                       margin=dict(t=10,b=10))
    st.plotly_chart(fig7, use_container_width=True)

st.divider()

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 5 — Health factor scatter + Correlation + Top/Bottom
# ═══════════════════════════════════════════════════════════════════════════════
col8, col9, col10 = st.columns([2, 1, 1])

FACTORS = {
    "adultmortality":    "Adult mortality",
    "alcohol_consumption": "Alcohol consumption",
    "bmi":               "BMI",
    "hiv_aids":          "HIV/AIDS",
    "gdp":               "GDP (USD)",
    "schooling":         "Schooling (yrs)",
    "totalexpenditure":  "Health expenditure",
}

with col8:
    st.subheader("Health factor vs life expectancy")
    factor = st.selectbox("Factor", list(FACTORS.keys()),
                          format_func=lambda x: FACTORS[x], key="hf_sel")
    df_hf = apply_filters(df_health, year_col="year").dropna(subset=[factor, "lifeexpectancy"])
    fig8 = px.scatter(df_hf, x=factor, y="lifeexpectancy", color="status", opacity=0.45,
                      trendline="ols",
                      color_discrete_map={"Developed": "#1D9E75", "Developing": "#378ADD"},
                      labels={factor: FACTORS[factor], "lifeexpectancy": "Life exp (yrs)"},
                      hover_data=["country", "year"])
    fig8.update_layout(plot_bgcolor="rgba(0,0,0,0)", legend=dict(title=""),
                       margin=dict(t=10,b=10))
    st.plotly_chart(fig8, use_container_width=True)

with col9:
    st.subheader("Correlations")
    num_cols = list(FACTORS.keys()) + ["lifeexpectancy"]
    corr = (df_health[num_cols].dropna().corr()[["lifeexpectancy"]]
            .drop("lifeexpectancy")
            .rename(columns={"lifeexpectancy": "r"})
            .sort_values("r"))
    fig9 = px.bar(corr, x="r", y=corr.index, orientation="h",
                  color="r", color_continuous_scale=["#D85A30","#F1EFE8","#1D9E75"],
                  range_color=[-1, 1], labels={"y": "", "r": "Pearson r"})
    fig9.update_layout(plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
                       margin=dict(t=10,b=10))
    st.plotly_chart(fig9, use_container_width=True)

with col10:
    st.subheader("Top & bottom 10")
    view = st.radio("View", ["Top 10 🏆", "Bottom 10 ⚠️"], horizontal=True, key="tb_view")
    if "Top" in view:
        df_tb = df_top.sort_values("life_expectancy")
        bar_color = "#1D9E75"
    else:
        df_tb = df_bot.sort_values("life_expectancy", ascending=False)
        bar_color = "#D85A30"
    fig10 = px.bar(df_tb, x="life_expectancy", y="country", orientation="h",
                   text="life_expectancy",
                   labels={"life_expectancy": "Life exp (yrs)", "country": ""})
    fig10.update_traces(marker_color=bar_color, textposition="outside")
    fig10.update_layout(plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=10,b=10),
                        xaxis_range=[40, df_tb["life_expectancy"].max() + 3])
    st.plotly_chart(fig10, use_container_width=True)