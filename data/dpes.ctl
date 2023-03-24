LOAD DATA INFILE dpes.csv "STR '\r\n'"
APPEND INTO TABLE dpes
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"' AND '"'
TRAILING NULLCOLS
    ( no_dpe
    , id_logement
    , date_reception                 DATE "yyyy-mm-dd"
    , date_etablissement             DATE "yyyy-mm-dd"
    , date_visite                    DATE "yyyy-mm-dd"
    , dpe_remplace
    , date_fin_validite              DATE "yyyy-mm-dd"
    , version                        "to_number(:version,             '9D9',       'NLS_NUMERIC_CHARACTERS=''.,''')"
    , appartement_non_visite
    , no_immatriculation_copropriete
    , invariant_fiscal_logement
    , etiquette_ges
    , etiquette_dpe
    , type_ventilation
    , surface_ventilee               "to_number(:surface_ventilee,    '99999D9',   'NLS_NUMERIC_CHARACTERS=''.,''')"
    , type_enr
    , conso_enr                      "to_number(:conso_enr,           '9999D9',    'NLS_NUMERIC_CHARACTERS=''.,''')"
    , production_enr                 "to_number(:production_enr,      '9999999D9', 'NLS_NUMERIC_CHARACTERS=''.,''')"
    , surface_capteurs_pv            "to_number(:surface_capteurs_pv, '9999D9',    'NLS_NUMERIC_CHARACTERS=''.,''')"
    )