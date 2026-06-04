import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
from sqlalchemy.engine import URL


# 1. Load cleaned CSV
df = pd.read_csv("data/processed/life_expectancy_clean.csv")

# 2. Supabase connection
@st.cache_resource
def get_engine():
    database_url = URL.create(
    drivername="postgresql+psycopg2",
    username=st.secrets["db_user"],
    password=st.secrets["db_password"],
    host=st.secrets["db_host"],
    port=int(st.secrets["db_port"]),
    database=st.secrets["db_name"],
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