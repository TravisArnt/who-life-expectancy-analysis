import pandas as pd
from sqlalchemy import create_engine

# 1. Load your cleaned CSV
df = pd.read_csv("data/processed/life_expectancy_clean.csv")

# 2. Supabase connection
engine = create_engine(
    "postgresql+psycopg2://postgres:Password@db.yhaiasmiepaqidykdbsm.supabase.co:5432/postgres"
)

# 3. Upload to Supabase
df.to_sql(
    "life_expectancy",
    engine,
    if_exists="replace",
    index=False
)

print("Uploaded to Supabase successfully!")