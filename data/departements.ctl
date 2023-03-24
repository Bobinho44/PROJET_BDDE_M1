LOAD DATA INFILE departements.csv "STR '\r\n'"
APPEND INTO TABLE departements
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( no_departement
    , no_region
    , zone_climatique
    )