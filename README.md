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

## Deployment

This dashboard is deployed on Render as a web service.

The app connects to Supabase PostgreSQL using environment variables configured in Render. Database credentials are not stored in the GitHub repository.

How to Run Locally
Clone the repository:
git clone https://github.com/your-username/who-life-expectancy-dashboard.git
cd who-life-expectancy-dashboard
Create and activate a virtual environment:
python -m venv .venv
source .venv/bin/activate

For Windows:

.venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Add database credentials:

Create a .streamlit/secrets.toml file and add your Supabase PostgreSQL connection string:

[database]
url = "postgresql+psycopg2://username:password@host:5432/database"
Run the Streamlit app:
streamlit run app.py
Dashboard Features

The dashboard allows users to explore WHO life expectancy data through interactive visualizations, including:

Global life expectancy trends
Developed vs developing country comparison
Vaccine coverage analysis
Health factor analysis
Top and bottom country rankings

## Tech Stack

- Python
- pandas
- PostgreSQL / Supabase
- SQL
- Streamlit
- Plotly