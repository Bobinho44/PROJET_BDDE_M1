-- départements avec la + haute consommation moyenne

SELECT *

FROM (SELECT no_departement
           , AVG(conso_chauffage + conso_ecs) AS conso_moyenne
           , COUNT(*) AS nb_generateurs

      FROM         communes
      NATURAL JOIN logements
      NATURAL JOIN dpes
      NATURAL JOIN generateurs

      GROUP BY no_departement

      ORDER BY conso_moyenne DESC)

WHERE ROWNUM <= 10;