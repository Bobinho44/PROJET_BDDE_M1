-- nombre d'installations chauffage/ECS/solaire par appartement

WITH a (nb_dpe) AS (SELECT COUNT(*) FROM dpes)

          SELECT 'chauffage' AS type_installation, COUNT(*) / nb_dpe AS nb_avg FROM installations_chauffage, a GROUP BY nb_dpe
UNION ALL SELECT 'ecs'       AS type_installation, COUNT(*) / nb_dpe AS nb_avg FROM installations_ecs      , a GROUP BY nb_dpe
UNION ALL SELECT 'solaire'   AS type_installation, COUNT(*) / nb_dpe AS nb_avg FROM installations_solaire  , a GROUP BY nb_dpe;