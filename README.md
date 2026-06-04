## Project Workflow

This project follows an analytics engineering workflow:

1. **Data Cleaning**
   - Cleaned and preprocessed the WHO Life Expectancy dataset using Python and pandas.

2. **Database Loading**
   - Uploaded the cleaned dataset into Supabase PostgreSQL.

3. **Data Modeling**
   - Created SQL analytical views to serve as lightweight data marts for dashboard analysis.

4. **Dashboard Development**
   - Built an interactive Streamlit dashboard connected to Supabase.
   - Used Streamlit caching to improve query performance and reduce repeated database calls.

5. **Data Visualization**
   - Used Plotly to create interactive visualizations for:
     - Global life expectancy trends
     - Developed vs developing country comparison
     - Vaccine coverage analysis
     - Health factor analysis
     - Top and bottom country rankings