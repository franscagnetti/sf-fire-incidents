SELECT
  DATE_TRUNC('month', incident_date::timestamp) AS month,
  neighborhood_district AS district,
  battalion,
  COUNT(*) AS total_incidents
FROM {{ ref('stg_fire_incidents') }}
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3
