--05_health_factors.sql
CREATE OR REPLACE VIEW mart_health_factors_scatter AS
SELECT 
    "country",
    "year",
    "status",
    "lifeexpectancy",
    "adultmortality",
    "infantdeaths",
    "under_fivedeaths",
    "alcohol_consumption",
    "bmi",
    "hiv_aids",
    "measles",
    "gdp",
    "population",
    "schooling",
    "totalexpenditure"
FROM life_expectancy;
