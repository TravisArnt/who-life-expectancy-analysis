import pandas as pd
import os
from sqlalchemy import create_engine
import streamlit as st
from sqlalchemy.engine import URL

def get_secret(key: str):
    """
    First checks Render environment variables.
    If not found, falls back to Streamlit secrets.
    """
    return os.getenv(key) or st.secrets[key]
# 1. Load cleaned CSV
df = pd.read_csv("data/processed/life_expectancy_clean.csv")

# 2. Supabase connection

@st.cache_resource
def get_engine():
    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=get_secret("db_user"),
        password=get_secret("db_password"),
        host=get_secret("db_host"),
        port=int(get_secret("db_port")),
        database=get_secret("db_name"),
    )

    return create_engine(database_url)


engine = get_engine()

# 3. Upload to Supabase
df.to_sql(
    "life_expectancy",
    engine,
    if_exists="replace",
    index=False
)

print("Uploaded to Supabase successfully!")