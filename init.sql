CLEAR SCREEN;

DROP TABLE generateurs             CASCADE CONSTRAINTS PURGE;
DROP TABLE installations_solaire   CASCADE CONSTRAINTS PURGE;
DROP TABLE installations_ecs       CASCADE CONSTRAINTS PURGE;
DROP TABLE installations_chauffage CASCADE CONSTRAINTS PURGE;
DROP TABLE dpes                    CASCADE CONSTRAINTS PURGE;
DROP TABLE logements               CASCADE CONSTRAINTS PURGE;
DROP TABLE communes                CASCADE CONSTRAINTS PURGE;
DROP TABLE departements            CASCADE CONSTRAINTS PURGE;

CREATE TABLE departements
    ( no_departement  NUMBER(3) CONSTRAINT pk_departements                 PRIMARY KEY
    , no_region       NUMBER(2) CONSTRAINT nn_departements_no_region       NOT NULL
    , zone_climatique CHAR(3)   CONSTRAINT nn_departements_zone_climatique NOT NULL
    );

CREATE TABLE communes
    ( code_insee     NUMBER(5)    CONSTRAINT pk_communes                PRIMARY KEY
    , no_departement              CONSTRAINT nn_communes_no_departement NOT NULL
                                  CONSTRAINT fk_communes_departements   REFERENCES departements ON DELETE CASCADE
    , nom_commune    VARCHAR2(50) CONSTRAINT nn_communes_nom_commune    NOT NULL
    , code_postal    NUMBER(5)    CONSTRAINT nn_communes_code_postal    NOT NULL
    );

CREATE TABLE logements
    ( id_logement                 VARCHAR2(300) CONSTRAINT pk_logements                      PRIMARY KEY
    , code_insee                                CONSTRAINT nn_logements_code_insee           NOT NULL
                                                CONSTRAINT fk_logements_communes             REFERENCES communes ON DELETE CASCADE
    , annee_construction          NUMBER(4)
    , type_batiment               VARCHAR2(11)  CONSTRAINT nn_logements_type_batiment        NOT NULL
    , type_installation_chauffage VARCHAR2(10)
    , type_instalation_ecs        VARCHAR2(10)
    , hauteur_sous_plafond        NUMBER(4,1)   CONSTRAINT nn_logements_hauteur_sous_plafond NOT NULL
    , nb_niveau                   NUMBER(3)
    , surface_habitable           NUMBER(6,1)   CONSTRAINT nn_logements_surface_habitable    NOT NULL
    , classe_inertie              VARCHAR2(15)
    , typologie                   CHAR(2)
    );

CREATE TABLE dpes
    ( no_dpe                         CHAR(13)     CONSTRAINT pk_dpes                    PRIMARY KEY
    , id_logement                                 CONSTRAINT fk_dpes_logements          REFERENCES logements ON DELETE CASCADE
    , date_reception                 DATE         CONSTRAINT nn_dpes_date_reception     NOT NULL
    , date_etablissement             DATE         CONSTRAINT nn_dpes_date_etablissement NOT NULL
    , date_visite                    DATE         CONSTRAINT nn_dpes_date_visite        NOT NULL
    , dpe_remplace                   NUMBER(1)    CONSTRAINT nn_dpes_dpe_remplace       NOT NULL
    , date_fin_validite              DATE         CONSTRAINT nn_dpes_date_fin_validite  NOT NULL
    , version                        NUMBER(2,1)  CONSTRAINT nn_dpes_version            NOT NULL
    , appartement_non_visite         NUMBER(1)
    , no_immatriculation_copropriete CHAR(9)
    , invariant_fiscal_logement      NUMBER(10)
    , etiquette_ges                  CHAR(1)      CONSTRAINT nn_dpes_etiquette_ges      NOT NULL
    , etiquette_dpe                  CHAR(1)      CONSTRAINT nn_dpes_etiquette_dpe      NOT NULL
    , type_ventilation               VARCHAR2(70)
    , surface_ventilee               NUMBER(6,1)
    , type_enr                       VARCHAR2(40)
    , conso_enr                      NUMBER(5,1)
    , production_enr                 NUMBER(8,1)
    , surface_capteurs_pv            NUMBER(5,1)
    
    , CONSTRAINT chk_dpes_ventilation CHECK (type_ventilation IS NOT NULL AND surface_ventilee IS NOT NULL
                                          OR type_ventilation IS     NULL AND surface_ventilee IS     NULL)
    , CONSTRAINT chk_dpes_enr         CHECK (conso_enr IS NOT NULL AND production_enr IS NOT NULL AND surface_capteurs_pv IS NOT NULL
                                          OR conso_enr IS     NULL AND production_enr IS     NULL AND surface_capteurs_pv IS     NULL AND type_enr IS NULL)
    );

CREATE TABLE installations_chauffage
    ( no_dpe                                              CONSTRAINT fk_installations_chauffage_dpes                                 REFERENCES dpes ON DELETE CASCADE
    , no_installation_chauffage            NUMBER(1)
    , description_installation_chauffage   VARCHAR2(1000)
    , type_installation_chauffage          VARCHAR2(12)   CONSTRAINT nn_installations_chauffage_type_installation_chauffage          NOT NULL
    , configuration_installation_chauffage VARCHAR2(200)  CONSTRAINT nn_installations_chauffage_configuration_installation_chauffage NOT NULL
    , surface_chauffee                     NUMBER(6,1)    CONSTRAINT nn_installations_chauffage_surface_chauffee                     NOT NULL
    , type_emetteur_chauffage              VARCHAR2(150)  CONSTRAINT nn_installations_chauffage_type_emetteur_chauffage              NOT NULL
    
    , CONSTRAINT pk_installations_chauffage PRIMARY KEY (no_dpe, no_installation_chauffage)
    );

CREATE TABLE installations_ecs
    ( no_dpe                                        CONSTRAINT fk_installations_ecs_dpes                           REFERENCES dpes ON DELETE CASCADE
    , no_installation_ecs            NUMBER(1)
    , description_installation_ecs   VARCHAR2(1000)
    , type_installation_ecs          VARCHAR2(12)   CONSTRAINT nn_installations_ecs_type_installation_ecs          NOT NULL
    , configuration_installation_ecs VARCHAR2(200)  CONSTRAINT nn_installations_ecs_configuration_installation_ecs NOT NULL
    
    , CONSTRAINT pk_installations_ecs PRIMARY KEY (no_dpe, no_installation_ecs)
    );

CREATE TABLE installations_solaire
    ( no_dpe                                  CONSTRAINT fk_installations_solaire_dpes                       REFERENCES dpes ON DELETE CASCADE
    , no_installation_solaire    NUMBER(1)
    , type_installation_solaire  VARCHAR2(30) CONSTRAINT nn_installations_solaire_type_installation_solaire  NOT NULL
    , facteur_couverture_solaire NUMBER(2,1)  CONSTRAINT nn_installations_solaire_facteur_couverture_solaire NOT NULL
    
    , CONSTRAINT pk_installations_solaire PRIMARY KEY (no_dpe, no_installation_solaire)
    );

CREATE TABLE generateurs
    ( no_dpe                                     CONSTRAINT fk_generateurs_dpes                      REFERENCES dpes ON DELETE CASCADE
    , no_generateur                NUMBER(1)
    , no_installation_chauffage
    , no_installation_ecs
    , no_installation_solaire
    , conso_chauffage              NUMBER(8,1)   CONSTRAINT nn_generateurs_conso_chauffage           NOT NULL
    , conso_chauffage_depensier    NUMBER(8,1)   CONSTRAINT nn_generateurs_conso_chauffage_depensier NOT NULL
    , conso_ecs                    NUMBER(8,1)   CONSTRAINT nn_generateurs_conso_ecs                 NOT NULL
    , conso_ecs_depensier          NUMBER(8,1)   CONSTRAINT nn_generateurs_conso_ecs_depensier       NOT NULL
    , description_generateur       VARCHAR2(150)
    , date_installation_generateur VARCHAR2(20)
    , type_energie                 VARCHAR2(100) CONSTRAINT nn_generateurs_type_energie              NOT NULL
    , type_generateur              VARCHAR2(150) CONSTRAINT nn_generateurs_type_generateur           NOT NULL
    
    , CONSTRAINT pk_generateurs                         PRIMARY KEY (no_dpe, no_generateur)
    , CONSTRAINT fk_generateurs_installations_chauffage FOREIGN KEY (no_dpe, no_installation_chauffage) REFERENCES installations_chauffage ON DELETE CASCADE
    , CONSTRAINT fk_generateurs_installations_ecs       FOREIGN KEY (no_dpe, no_installation_ecs)       REFERENCES installations_ecs       ON DELETE CASCADE
    , CONSTRAINT fk_generateurs_installations_solaire   FOREIGN KEY (no_dpe, no_installation_solaire)   REFERENCES installations_solaire   ON DELETE CASCADE
    );

CREATE OR REPLACE FUNCTION test_role(p_role IN VARCHAR2) RETURN NUMBER IS
    nb NUMBER;
BEGIN
    SELECT COUNT(*) INTO nb
    FROM dual
    WHERE EXISTS (SELECT NULL
                  FROM dba_role_privs
                  WHERE grantee = USER AND granted_role = UPPER(p_role));
    RETURN nb;
END;
/

DROP ROLE dpe_admin;
DROP ROLE dpe_diagnostiqueur;
DROP ROLE dpe_proprietaire;
DROP ROLE dpe_base;

CREATE ROLE dpe_admin;
CREATE ROLE dpe_diagnostiqueur;
CREATE ROLE dpe_proprietaire;
CREATE ROLE dpe_base;

GRANT ALL ON departements            TO dpe_admin;
GRANT ALL ON communes                TO dpe_admin;
GRANT ALL ON logements               TO dpe_admin;
GRANT ALL ON dpes                    TO dpe_admin;
GRANT ALL ON installations_chauffage TO dpe_admin;
GRANT ALL ON installations_ecs       TO dpe_admin;
GRANT ALL ON installations_solaire   TO dpe_admin;
GRANT ALL ON generateurs             TO dpe_admin;

GRANT SELECT, INSERT ON departements            TO dpe_diagnostiqueur;
GRANT SELECT, INSERT ON communes                TO dpe_diagnostiqueur;
GRANT SELECT, INSERT ON logements               TO dpe_diagnostiqueur;
GRANT SELECT, INSERT ON dpes                    TO dpe_diagnostiqueur;
GRANT SELECT, INSERT ON installations_chauffage TO dpe_diagnostiqueur;
GRANT SELECT, INSERT ON installations_ecs       TO dpe_diagnostiqueur;
GRANT SELECT, INSERT ON installations_solaire   TO dpe_diagnostiqueur;
GRANT SELECT, INSERT ON generateurs             TO dpe_diagnostiqueur;

GRANT SELECT ON departements            TO dpe_proprietaire;
GRANT SELECT ON communes                TO dpe_proprietaire;
GRANT SELECT ON logements               TO dpe_proprietaire;
GRANT SELECT ON dpes                    TO dpe_proprietaire;
GRANT SELECT ON installations_chauffage TO dpe_proprietaire;
GRANT SELECT ON installations_ecs       TO dpe_proprietaire;
GRANT SELECT ON installations_solaire   TO dpe_proprietaire;
GRANT SELECT ON generateurs             TO dpe_proprietaire;

GRANT SELECT ON departements            TO dpe_base;
GRANT SELECT ON communes                TO dpe_base;
GRANT SELECT ON logements               TO dpe_base;
GRANT SELECT ON dpes                    TO dpe_base;
GRANT SELECT ON installations_chauffage TO dpe_base;
GRANT SELECT ON installations_ecs       TO dpe_base;
GRANT SELECT ON installations_solaire   TO dpe_base;
GRANT SELECT ON generateurs             TO dpe_base;

-- GRANT  TO testuser;
