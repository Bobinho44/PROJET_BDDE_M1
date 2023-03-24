-- nombre de DPE réalisés par an avec cumul, par type d'établissement

SELECT type_batiment
     , EXTRACT(YEAR FROM date_etablissement) AS annee
     , COUNT(*) AS nb_dpes
     , SUM(COUNT(*)) OVER (ORDER BY EXTRACT(YEAR FROM date_etablissement) ROWS UNBOUNDED PRECEDING) AS nb_dpes_cumules

FROM         dpes
NATURAL JOIN logements

GROUP BY GROUPING SETS ( EXTRACT(YEAR FROM date_etablissement)
                       , (type_batiment, EXTRACT(YEAR FROM date_etablissement))
                       )

ORDER BY type_batiment, annee;