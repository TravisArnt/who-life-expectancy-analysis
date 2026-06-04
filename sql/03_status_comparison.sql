-- 03_status_comparison.sql

--For bar chart
CREATE OR REPLACE VIEW mart_status_life_expectancy_trend AS 
SELECT 
    "year",
    "status",
    ROUND(AVG("lifeexpectancy")::numeric,2) AS avg_life_expectancy,
    COUNT(DISTINCT "country") AS country_count
FROM life_expectancy
GROUP BY "year", "status"
ORDER BY "year", "status";


--For pie chart 
CREATE OR REPLACE VIEW mart_status_distribution AS
SELECT "status",
    COUNT(DISTINCT "country") AS country_count
FROM life_expectancy
GROUP BY "status"
ORDER BY country_count DESC;


--for boxplot
CREATE OR REPLACE VIEW mart_status_life_expectancy_boxplot AS
SELECT 
    "country",
    "year",
    "status",
    "lifeexpectancy"
FROM life_expectancy;