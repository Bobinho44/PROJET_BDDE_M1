-- consommation moyenne selon la typologie du logement, puis selon aussi la
-- classe d'inertie

SELECT typologie, classe_inertie
     , AVG(conso_chauffage) AS consommation_chauffage_moyenne
     , AVG(conso_ecs)       AS consommation_ecs_moyenne
     , AVG(conso_enr)       AS consommation_enr_moyenne

FROM         generateurs
NATURAL JOIN dpes
NATURAL JOIN logements

GROUP BY ROLLUP (typologie, classe_inertie);