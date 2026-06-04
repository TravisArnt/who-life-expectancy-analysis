# WHO Life Expectancy Dashboard

An analytics engineering project exploring global life expectancy trends using WHO data (2000–2015). 
Built with Python, SQL, Supabase, and Streamlit.

🔗 [Live demo](https://who-life-expectancy-analysis.onrender.com/)

## Dataset

This project uses the Life Expectancy WHO dataset from Kaggle. The dataset contains country-level health, economic, and demographic indicators from 2000 to 2015.

Dataset source: [Life Expectancy WHO Dataset](https://www.kaggle.com/datasets/kumarajarshi/life-expectancy-who)

## Project Workflow

This project follows an analytics engineering workflow:

1. **Data Cleaning**

   * Cleaned and preprocessed the WHO Life Expectancy dataset using Python and pandas.

2. **Database Loading**

   * Uploaded the cleaned dataset into Supabase PostgreSQL.

3. **Data Modeling**

   * Created SQL analytical views to serve as lightweight data marts for dashboard analysis.

4. **Dashboard Development**

   * Built an interactive Streamlit dashboard connected to Supabase.
   * Used Streamlit caching to improve query performance and reduce repeated database calls.

5. **Data Visualization**

   * Used Plotly to create interactive visualizations for:

     * Global life expectancy trends
     * Developed vs developing country comparison
     * Vaccine coverage analysis
     * Health factor analysis
     * Top and bottom country rankings


## Dashboard Features

The dashboard allows users to explore WHO life expectancy data through interactive visualizations, including:

* Global life expectancy trends
* Developed vs developing country comparison
* Vaccine coverage analysis
* Health factor analysis
* Top and bottom country rankings

## Tech Stack

* Python
* pandas
* PostgreSQL / Supabase
* SQL
* Streamlit
* Plotly
* Render

## Deployment

This dashboard is deployed on Render as a web service.

The app connects to Supabase using environment variables configured in Render. Database credentials are not stored in the GitHub repository.

Required Render environment variables:

```txt
SUPABASE_URL
SUPABASE_KEY
```

## How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/your-username/who-life-expectancy-dashboard.git
cd who-life-expectancy-dashboard
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

For Windows:

```bash
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Add Supabase credentials:

Create a `.streamlit/secrets.toml` file and add:

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-supabase-anon-key"
```

5. Run the Streamlit app:

```bash
streamlit run main.py
```

