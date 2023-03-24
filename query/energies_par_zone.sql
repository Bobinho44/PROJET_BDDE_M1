-- 3 types d'énergies les plus utilisés par zone climatique

SELECT *

FROM (SELECT zone_climatique
           , type_energie
           , RANK() OVER (PARTITION BY zone_climatique
                          ORDER BY COUNT(*) DESC) AS rang
           , COUNT(*) AS nb_generateurs

      FROM         generateurs
      NATURAL JOIN dpes
      NATURAL JOIN logements
      NATURAL JOIN communes
      NATURAL JOIN departements

      GROUP BY zone_climatique, type_energie)

WHERE rang <= 3

ORDER BY zone_climatique, rang;