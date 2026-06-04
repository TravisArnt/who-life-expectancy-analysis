This project follows a simple analytics engineering workflow:

1. Data cleaning and preprocessing were completed using Python and pandas.
2. The cleaned dataset was uploaded into Supabase PostgreSQL.
3. SQL analytical views were created to serve as lightweight data marts.
4. Streamlit connects to Supabase and queries the prepared marts.
5. Query results are cached using Streamlit caching to improve dashboard performance.
6. Plotly is used to build interactive visualizations for trend analysis, status comparison, vaccine coverage, health factors, and country ranking.