CREATE OR REPLACE VIEW wip_devcustomerkeys AS
SELECT DISTINCT customer_key
FROM cluster_metric
WHERE customer_key IS NOT NULL
  AND
  (
    environment_version_min LIKE '%-%' 
    OR customer_name LIKE '%Mesosphere%'
    OR customer_key = '00000000-0000-0000-0000-000000000000'
    OR customer_key LIKE '%12345%'
    OR customer_key ILIKE '%xxxxx%'
    OR customer_key ILIKE '%galaxy%'
    OR customer_key ILIKE '%qwerty%'
    OR customer_key ILIKE '%aaaa%'
  )
;
