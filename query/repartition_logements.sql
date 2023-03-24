-- nombre de logements par type d'installation, zone climatique et/ou région

SELECT zone_climatique
     , no_region
     , type_installation_chauffage
     , COUNT(*) AS nb_logements
     , GROUPING_ID(zone_climatique, no_region, type_installation_chauffage) AS id_groupe

FROM         logements
NATURAL JOIN communes
NATURAL JOIN departements

GROUP BY GROUPING SETS ( ()                                             -- tous les logements
                       , (type_installation_chauffage)                  -- par type d'installation
                       , (zone_climatique)                              -- par zone climatique
                       , (no_region, type_installation_chauffage)       -- par région et type d'installation
                       , (zone_climatique, type_installation_chauffage) -- par zone climatique et type d'installation
                       );