LOAD DATA INFILE logements.csv "STR '\r\n'"
APPEND INTO TABLE logements
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( id_logement
    , code_insee
    , annee_construction
    , type_batiment
    , type_installation_chauffage
    , type_instalation_ecs
    , hauteur_sous_plafond
    , nb_niveau
    , surface_habitable           "to_number(:surface_habitable, '99999D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    , classe_inertie
    , typologie
    )