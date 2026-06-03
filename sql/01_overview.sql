-- 01_overview.sql
CREATE OR REPLACE VIEW mart_overview AS
SELECT
    ROUND(AVG("lifeexpectancy")::numeric, 2) AS avg_life_expectancy,
    ROUND(MAX("lifeexpectancy")::numeric, 2) AS max_life_expectancy,
    ROUND(MIN("lifeexpectancy")::numeric, 2) AS min_life_expectancy,
    COUNT(DISTINCT "country") AS total_countries,
    COUNT(*) AS total_records,
    MIN("year") AS start_year,
    MAX("year") AS end_year
FROM life_expectancy;