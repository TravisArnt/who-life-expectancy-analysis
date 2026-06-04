import pandas as pd
import os
from sqlalchemy import create_engine
import streamlit as st
from sqlalchemy.engine import URL

def get_secret(key: str) -> str:
    """
    Read config from environment variables first, then local Streamlit secrets.
    """
    value = os.getenv(key) or os.getenv(key.upper())
    if value:
        return value

    try:
        return st.secrets[key]
    except Exception as exc:
        raise RuntimeError(
            f"Missing required setting '{key}'. Add it as an environment "
            f"variable, or add it to .streamlit/secrets.toml for local runs."
        ) from exc
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
