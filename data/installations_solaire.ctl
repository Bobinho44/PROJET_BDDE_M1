LOAD DATA INFILE installations_solaire.csv "STR '\r\n'"
APPEND INTO TABLE installations_solaire
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( no_dpe
    , no_installation_solaire
    , type_installation_solaire
    , facteur_couverture_solaire "to_number(:facteur_couverture_solaire, '9D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    )