LOAD DATA INFILE installations_chauffage.csv "STR '\r\n'"
APPEND INTO TABLE installations_chauffage
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( no_dpe
    , no_installation_chauffage
    , description_installation_chauffage   CHAR(1000)
    , type_installation_chauffage
    , configuration_installation_chauffage
    , surface_chauffee                     "to_number(:surface_chauffee, '99999D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    , type_emetteur_chauffage
    )