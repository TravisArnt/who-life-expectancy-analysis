-- 02_life_expectancy_trends.sql

CREATE OR REPLACE VIEW global_life_expectancy_trend AS 
SELECT 
    "year",
    ROUND(AVG("lifeexpectancy")::numeric,2) AS avg_life_expectancy
FROM life_expectancy
GROUP BY "year"
ORDER BY "year";

CREATE OR REPLACE VIEW country_life_expectancy_trend AS
SELECT 
    "country",
    "year",
    ROUND(AVG("lifeexpectancy")::numeric,2) AS avg_life_expectancy
FROM life_expectancy
GROUP BY "country", "year"
ORDER BY "country", "year";