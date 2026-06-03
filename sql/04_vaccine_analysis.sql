-- 04_vaccine_analysis.sql

-- For line chart
CREATE OR REPLACE VIEW mart_vaccine_coverage_trend AS 
SELECT 
    "year",
    ROUND(AVG("hepatitisb_vaccine_coverage")::numeric,2) AS avg_hepatitisb_vaccine_coverage,
    ROUND(AVG("polio_vaccine_coverage")::numeric,2) AS avg_polio_vaccine_coverage,
    ROUND(AVG("diphtheria_vaccine_coverage")::numeric,2) AS avg_diphtheria_vaccine_coverage
FROM life_expectancy
GROUP BY "year"
ORDER BY "year";



--For scatter plot
CREATE OR REPLACE VIEW mart_vaccine_life_expectancy_scatter AS
SELECT 
    "country",
    "year",
    "status",
    "lifeexpectancy",
    "hepatitisb_vaccine_coverage",
    "polio_vaccine_coverage",
    "diphtheria_vaccine_coverage"
FROM life_expectancy;