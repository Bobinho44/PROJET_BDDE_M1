LOAD DATA INFILE generateurs.csv "STR '\r\n'"
APPEND INTO TABLE generateurs
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( no_dpe
    , no_generateur
    , no_installation_chauffage
    , no_installation_ecs
    , no_installation_solaire
    , conso_chauffage              "to_number(:conso_chauffage,           '9999999D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    , conso_chauffage_depensier    "to_number(:conso_chauffage_depensier, '9999999D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    , conso_ecs                    "to_number(:conso_ecs,                 '9999999D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    , conso_ecs_depensier          "to_number(:conso_ecs_depensier,       '9999999D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    , description_generateur
    , date_installation_generateur
    , type_energie
    , type_generateur
    )