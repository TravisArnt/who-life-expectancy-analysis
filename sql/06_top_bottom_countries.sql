-- 06_top_bottom_countries.sql

CREATE OR REPLACE VIEW mart_top_bottom_life_expectancy AS 
SELECT 
    "country",
    "status",
    "year",
    ROUND("lifeexpectancy"::numeric, 2) AS life_expectancy
FROM life_expectancy
WHERE "year"  = (
    SELECT MAX("year")
    FROM life_expectancy
);

-- Top 10 Country
CREATE OR REPLACE VIEW mart_top_10_life_expectancy AS
SELECT
    "country",
    "status",
    "year",
    "life_expectancy"
FROM mart_top_bottom_life_expectancy
ORDER BY "life_expectancy" DESC
LIMIT 10;

-- Bottom 10 Country
CREATE OR REPLACE VIEW mart_bottom_10_life_expectancy AS
SELECT
    "country",
    "status",
    "year",
    "life_expectancy"
FROM mart_top_bottom_life_expectancy
ORDER BY "life_expectancy" ASC
LIMIT 10;