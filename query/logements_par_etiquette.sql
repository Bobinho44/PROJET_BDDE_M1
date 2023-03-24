-- nombre de logements avec l'étiquette GES, l'étiquette DPE, et les deux

SELECT etiquette_ges
     , etiquette_dpe
     , COUNT(*) AS nb_logements

FROM dpes

WHERE dpe_remplace = 0

GROUP BY CUBE (etiquette_ges, etiquette_dpe);