LOAD DATA INFILE installations_ecs.csv "STR '\r\n'"
APPEND INTO TABLE installations_ecs
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( no_dpe
    , no_installation_ecs
    , description_installation_ecs   CHAR(1000)
    , type_installation_ecs
    , configuration_installation_ecs
    )