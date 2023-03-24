LOAD DATA INFILE communes.csv "STR '\r\n'"
APPEND INTO TABLE communes
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( code_insee
    , no_departement
    , nom_commune
    , code_postal
    )