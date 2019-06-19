CREATE VIEW wip_cluster_filter AS
WITH mesosphere_ip AS
(
  SELECT ip
  FROM
  (
    SELECT ip, email
    FROM dcos.login
    WHERE email ILIKE '%mesosphere%'
    UNION ALL
    SELECT context_ip ip, email
    FROM dcos.dcos_login
    WHERE user_id ILIKE '%mesosphere%'
  ) x
  GROUP BY ip
  HAVING COUNT(DISTINCT email) >= 3
), gui AS
(
  SELECT cluster_id, context_ip ip, MAX((user_id ILIKE '%mesosphere%')::INT)::BOOLEAN m_user
  FROM dcos.pages
  GROUP BY cluster_id, ip
)
SELECT DISTINCT cm.cluster_id
FROM gui
JOIN cluster_metric cm USING(cluster_id)
LEFT OUTER JOIN mesosphere_ip USING(ip)
WHERE NOT cm.is_mesosphere AND (mesosphere_ip.ip IS NOT NULL OR m_user)
UNION
SELECT DISTINCT cluster_id
FROM cluster_metric
WHERE NOT is_mesosphere
  AND (package_version_array ILIKE '%stub%' OR package_version_array ILIKE '%scale%')
;
