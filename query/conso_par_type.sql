-- consommation moyenne d'un générateur de chaque type d'énergie, classés selon
-- le nombre de générateurs de ce type

SELECT type_energie
     , AVG(conso_chauffage) AS conso_chauffage_moyenne
     , AVG(conso_ecs) AS conso_ecs_moyenne
     , RANK() OVER (ORDER BY COUNT(*) DESC) AS rank

FROM generateurs

GROUP BY type_energie

ORDER BY rank;