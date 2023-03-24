import csv
import itertools
import math
import re
import typing


fichier_src = 'dpe-v2-logements-existants.csv'


Ligne = typing.Mapping[str, typing.Any]


class CastError(Exception):
    '''
    Une erreur de conversion d'un champ CSV.
    '''
    def __init__(self, type: str, value: typing.Any, *args: object) -> None:
        super().__init__(f'Cannot cast "{value}" into {type}', *args)


class GenError(Exception):
    '''
    Une erreur de génération d'un enregistrement CSV.
    '''
    pass


def cast_annee(x: str) -> int:
    '''
    Convertit un champ CSV en année.
    '''
    if re.match('^[0-9]{4}$', x):
        return int(x)
    raise CastError('annee', x)

def cast_bool(x: str) -> int:
    '''
    Convertit un champ CSV en booléen.
    '''
    if x == '1' or x == '0':
        return int(x)
    raise CastError('bool', x)

def cast_classe_inertie(x: str) -> str:
    '''
    Convertit un champ CSV en classe d'inertie.
    '''
    if re.match('^(Moyenne|(Très l|L)(égère|ourde))$', x):
        return x.lower()
    raise CastError('classe_inertie', x)

def cast_code(x: str) -> int:
    '''
    Convertit un champ CSV en code INSEE ou postal.
    '''
    if re.match('^[0-9]{5}$', x):
        return int(x)
    raise CastError('code', x)

def cast_conso(x: str) -> str:
    '''
    Convertit un champ CSV en consommation électrique (en kWh/an).
    '''
    if re.match('^[0-9]+(\.[0-9]+)?$', x) and float(x) > 1.:
        return x
    raise CastError('conso', x)

def cast_date(x: str) -> str:
    '''
    Convertit un champ CSV en date, au format "AAAA-MM-JJ".
    '''
    if re.match('^[0-9]{4}-[0-9]{2}-[0-9]{2}$', x):
        return x
    raise CastError('date', x)

def cast_etiquette(x: str) -> str:
    '''
    Convertit un champ CSV en étiquette A à G.
    '''
    if re.match('^[A-G]$', x):
        return x
    raise CastError('etiquette', x)

def cast_facteur(x: str) -> str:
    '''
    Convertit un champ CSV en facteur multiplicateur.
    '''
    if re.match('^(1|0(\.[0-9]+)?)$', x):
        return x
    raise CastError('facteur', x)

def cast_float(x: str) -> str:
    '''
    Convertit un champ CSV en réel positif.
    '''
    if re.match('^[0-9]+(\.[0-9]+)?$', x):
        return x
    raise CastError('float', x)

def cast_hauteur_sous_plafond(x: str) -> str:
    '''
    Convertit un champ CSV en hauteur de sous-plafond.
    '''
    m = re.match('^([0-9]{1,2})(?:\.([0-9]))?$', x)
    if m:
        return int(m.group(1) + (m.group(2) or ''))
    raise CastError('hauteur_sous_plafond', x)

def cast_invariant_fiscal_logement(x: str) -> int:
    '''
    Convertit un champ CSV en invariant fiscal de logement.
    '''
    if re.match('^[0-9]{10}$', x) and x != '0000000000':
        return int(x)
    raise CastError('invariant_fiscal_logement', x)

def cast_no_immatriculation(x: str) -> str:
    '''
    Convertit un champ CSV en numéro d'immatriculation de copropriété.
    '''
    if re.match('^[A-Z]{2}[0-9]{7}$', x):
        return x
    raise CastError('no_immatriculation', x)

def cast_nombre(x: str) -> int:
    '''
    Convertit un champ CSV en entier naturel.
    '''
    if re.match('^[0-9]+$', x):
        return int(x)
    raise CastError('nombre', x)

def cast_str(x: str) -> str:
    '''
    Convertit un champ CSV en chaîne de caractères non vide.
    '''
    if x != '':
        return x.replace('\ufffd', 'é')
    raise CastError('str', x)

def cast_surface(x: str) -> str:
    '''
    Convertit un champ CSV en surface.
    '''
    if re.match('^[0-9]{1,5}(\.[0-9]+)?$', x):
        return x
    raise CastError('surface', x)

def cast_type_batiment(x: str) -> str:
    '''
    Convertit un champ CSV en type de logement.
    '''
    if x == 'maison' or x == 'appartement' or x == 'immeuble':
        return x
    raise CastError('type_batiment', x)

def cast_type_installation_general(x: str) -> str:
    '''
    Convertit un champ CSV en type d'installations.
    '''
    if x == 'collectif' or x == 'individuel':
        return x
    if x == 'mixte (collectif-individuel)':
        return 'mixte'
    raise CastError('type_installation_general', x)

def cast_type_installation(x: str) -> str:
    '''
    Convertit un champ CSV en type d'installation.
    '''
    if x == 'installation collective' or x == 'installation collective multi-bâtiment : modélisée comme un réseau de chaleur':
        return 'collective'
    if x == 'installation individuelle':
        return 'individuelle'
    if x == 'installation hybride collective-individuelle (chauffage base + appoint individuel ou convecteur bi-jonction)':
        return 'mixte'
    raise CastError('type_installation', x)

def cast_typologie(x: str) -> str:
    '''
    Convertit un champ CSV en typologie de logement.
    '''
    if re.match('T[1-6]', x):
        return x
    if x == 'T7 ou plus':
        return 'T7'
    raise CastError('typologie', x)

def cast_zone_climatique(x: str) -> str:
    '''
    Convertit un champ CSV en zone climatique.
    '''
    if re.match('H[1-3][a-d]?', x):
        return x
    raise CastError('zone_climatique', x)


departements: typing.Dict[int, Ligne] = {}

def generer_departement(ligne: Ligne) -> Ligne:
    '''
    Extrait, ou récupère en cache, les données d'un département.
    '''
    try:
        no_departement = cast_nombre(ligne['N°_département_(BAN)'])
        if no_departement in departements:
            return departements[no_departement]
    except CastError:
        raise GenError("Numéro de département invalide")

    departement: Ligne = { 'no_departement': no_departement }

    departement['no_region'] = cast_nombre(ligne['N°_région_(BAN)'])

    departement['zone_climatique'] = cast_zone_climatique(ligne['Zone_climatique_'])

    return departement


communes: typing.Dict[int, Ligne] = {}

def generer_commune(ligne: Ligne, departement: Ligne) -> Ligne:
    '''
    Extrait, ou récupère en cache, les données d'une commune.
    '''
    try:
        code_insee = cast_code(ligne['Code_INSEE_(BAN)'])
        if code_insee in communes:
            return communes[code_insee]
    except CastError:
        raise GenError("Code INSEE invalide")

    commune: Ligne = {
        'code_insee': code_insee,
        'no_departement': departement['no_departement']
    }

    try:
        commune['nom_commune'] = cast_str(ligne['Nom__commune_(BAN)'])
    except CastError:
        commune['nom_commune'] = cast_str(ligne['Nom__commune_(Brut)'])

    try:
        commune['code_postal'] = cast_code(ligne['Code_postal_(BAN)'])
    except CastError:
        commune['code_postal'] = cast_code(ligne['Code_postal_(brut)'])

    return commune


logements: typing.Dict[str, Ligne] = {}
logements_par_id_ban: typing.Dict[str, str] = {}
logements_par_adresse_brute: typing.Dict[str, str] = {}

def generer_logement(ligne: Ligne, commune: Ligne) -> Ligne:
    '''
    Extrait, ou récupère en cache, les données d'un logement.
    ATTENTION : les appartements d'un même immeuble ne sont pas distingués, et
                ne semblent pas pouvoir clairement l'être avec les données mises
                à disposition.
    '''
    try:
        id_ban = cast_str(ligne['Identifiant__BAN'])
        if id_ban in logements_par_id_ban:
            print('\tEXISTE')
            return logements[logements_par_id_ban[id_ban]]
    except CastError:
        try:
            id_ban = None
            adresse_brute = cast_str(ligne['Adresse_brute'])
            if adresse_brute in logements_par_adresse_brute:
                print('\tEXISTE (brut)')
                return logements[logements_par_adresse_brute[adresse_brute]]
        except CastError:
            raise GenError("Pas d'adresse")

    logement: Ligne = {
        'id_logement': id_ban or adresse_brute,
        'code_insee': commune['code_insee']
    }

    try:
        logement['annee_construction'] = cast_annee(ligne['Année_construction'])
    except CastError:
        pass

    try:
        type_batiment =\
        logement['type_batiment'] = cast_type_batiment(ligne['Type_bâtiment'])
    except CastError:
        raise GenError("Type de bâtiment invalide")

    try:
        logement['type_installation_chauffage'] = cast_type_installation_general(ligne['Type_installation_chauffage'])
    except CastError:
        pass

    try:
        logement['type_instalation_ecs'] = cast_type_installation_general(ligne['Type_installation_ECS_(général)'])
    except CastError:
        pass

    try:
        logement['hauteur_sous_plafond'] = cast_hauteur_sous_plafond(ligne['Hauteur_sous-plafond'])
    except CastError:
        raise GenError('Hauteur de sous-plafond invalide')

    if type_batiment == 'appartement':
        try:
            nb_niveau = cast_nombre(ligne['Nombre_niveau_logement'])
            if nb_niveau < 1000:
                # nos remerciements à la copropriété des Valladiers pour obliger à cette vérification ridicule.
                logement['nb_niveau'] = nb_niveau
        except CastError:
            try:
                # niveau 1 si l'immeuble n'a qu'un niveau
                if cast_nombre(ligne['Nombre_niveau_immeuble']) == 1:
                    logement['nb_niveau'] = 1
            except CastError:
                pass

    try:
        logement['surface_habitable'] = cast_surface(ligne['Surface_habitable_logement'])
    except CastError:
        try:
            # s'il n'y a qu'un appartement, sa surface est celle de l'immeuble
            if cast_nombre(ligne['Nombre_appartement']) == 1:
                logement['surface_habitable'] = cast_surface(ligne['Surface_habitable_immeuble'])
        except CastError:
            raise GenError('Surface habitable invalide')

    try:
        logement['classe_inertie'] = cast_classe_inertie(ligne['Classe_inertie_bâtiment'])
    except CastError:
        pass

    if type_batiment == 'appartement':
        try:
            logement['typologie'] = cast_typologie(ligne['Typologie_logement'])
        except CastError:
            pass

    return logement


def generer_dpe(ligne: Ligne, no_dpe: str, logement: Ligne) -> Ligne:
    '''
    Extrait les données d'un DPE.
    '''
    dpe: Ligne = { 'no_dpe': no_dpe }

    dpe['id_logement'] = logement['id_logement']

    dpe['date_reception']     = cast_date(ligne['Date_réception_DPE'])
    dpe['date_etablissement'] = cast_date(ligne['Date_établissement_DPE'])
    dpe['date_visite']        = cast_date(ligne['Date_visite_diagnostiqueur'])

    try:
        cast_str(ligne['N°_DPE_remplacé'])
        dpe['dpe_remplace'] = 1
    except CastError:
        dpe['dpe_remplace'] = 0
        pass

    dpe['date_fin_validite'] = cast_date(ligne['Date_fin_validité_DPE'])

    dpe['version'] = cast_str(ligne['Version_DPE'])

    try:
        dpe['appartement_non_visite'] = cast_bool(ligne['Appartement_non_visité_(0/1)'])
    except CastError:
        pass

    try:
        dpe['no_immatriculation_copropriete'] = cast_no_immatriculation(ligne['N°_immatriculation_copropriété'])
    except CastError:
        pass

    try:
        dpe['invariant_fiscal_logement'] = cast_invariant_fiscal_logement(ligne['Invariant_fiscal_logement'])
    except CastError:
        pass

    dpe['etiquette_ges'] = cast_etiquette(ligne['Etiquette_GES'])
    dpe['etiquette_dpe'] = cast_etiquette(ligne['Etiquette_DPE'])

    try:
        type_ventilation = cast_str(ligne['Type_ventilation'])
        surface_ventilee = cast_surface(ligne['Surface_ventilée'])
        dpe['type_ventilation'] = type_ventilation
        dpe['surface_ventilee'] = surface_ventilee
    except CastError:
        pass

    try:
        dpe['production_enr'] = cast_conso(ligne['Production_électricité_PV_(kWhep/an)'])

        try:
            dpe['conso_enr'] = cast_conso(ligne['Electricité_PV_autoconsommée'])
        except CastError:
            dpe['conso_enr'] = 0

        try:
            dpe['surface_capteurs_pv'] = cast_conso(ligne['Surface_totale_capteurs_photovoltaïque'])
        except CastError:
            dpe['surface_capteurs_pv'] = 0

        type_enr = cast_str(ligne['Catégorie_ENR'])
        if type_enr != 'Il existe plusieurs descriptifs ENR':
            dpe['type_enr'] = type_enr
    except CastError:
        pass

    return dpe


def generer_installation_chauffage(ligne: Ligne, dpe: Ligne, no_installation: int) -> Ligne:
    '''
    Extrait les données d'une installation de chauffage.
    '''
    installation: Ligne = {
        'no_dpe': dpe['no_dpe'],
        'no_installation_chauffage': no_installation
    }

    try:
        installation['description_installation_chauffage'] = cast_str(ligne[f'Description_installation_chauffage_n°{no_installation}'])
    except CastError:
        pass

    try:
        installation['type_installation_chauffage'] = cast_type_installation(ligne[f'Type_installation_chauffage_n°{no_installation}'])
    except CastError:
        raise GenError("Type d'installation de chauffage invalide")

    installation['configuration_installation_chauffage'] = cast_str(ligne[f'Configuration_installation_chauffage_n°{no_installation}'])

    try:
        installation['surface_chauffee'] = cast_surface(ligne[f'Surface_chauffée_installation_chauffage_n°{no_installation}'])
    except CastError:
        raise GenError("Surface chauffée invalide")

    installation['type_emetteur_chauffage'] = cast_str(ligne[f'Type_émetteur_installation_chauffage_n°{no_installation}'])

    return installation


def generer_installation_ecs(ligne: Ligne, dpe: Ligne) -> Ligne:
    '''
    Extrait les données d'une installation d'ECS.
    '''
    installation: Ligne = {
        'no_dpe': dpe['no_dpe'],
        'no_installation_ecs': 1
    }

    try:
        installation['description_installation_ecs'] = cast_str(ligne['Description_installation_ECS'])
    except CastError:
        pass

    try:
        installation['type_installation_ecs'] = cast_type_installation(ligne['Type_installation_ECS'])
    except CastError:
        raise GenError("Type d'installation d'ECS invalide")

    installation['configuration_installation_ecs'] = cast_str(ligne['Configuration_installation_ECS'])

    return installation


def generer_installation_solaire(ligne: Ligne, dpe: Ligne) -> Ligne:
    '''
    Extrait les données d'une installation solaire, pour ECS.
    '''
    installation: Ligne = {
        'no_dpe': dpe['no_dpe'],
        'no_installation_solaire': 1
    }

    try:
        installation['type_installation_solaire'] = cast_str(ligne['Type_installation_solaire'])
    except CastError:
        raise GenError("Type d'installation solaire invalide")

    try:
        installation['facteur_couverture_solaire'] = cast_facteur(ligne['Facteur_couverture_solaire'])
    except CastError:
        raise GenError('Facteur de couverture solaire invalide')

    return installation


def generer_generateur_chauffage(ligne: Ligne, installation_chauffage: Ligne, no_generateur: int) -> Ligne:
    '''
    Extrait les données de chauffage d'un générateur.
    '''
    no_installation = installation_chauffage['no_installation_chauffage']
    generateur: Ligne = {
        'no_dpe': dpe['no_dpe'],
        'no_generateur': 2 * no_installation - no_generateur,
        'no_installation_chauffage': no_installation
    }

    try:
        generateur['conso_chauffage']           = cast_conso(ligne[f'Conso_chauffage_générateur_n°{no_generateur}_installation_n°{no_installation}'])
        generateur['conso_chauffage_depensier'] = cast_conso(ligne[f'Conso_chauffage_dépensier_générateur_n°{no_generateur}_installation_n°{no_installation}'])
    except CastError:
        generateur['conso_chauffage']           = 0
        generateur['conso_chauffage_depensier'] = 0

    generateur['conso_ecs']           = 0
    generateur['conso_ecs_depensier'] = 0

    try:
        generateur['description_generateur'] = cast_str(ligne[f'Description_générateur_chauffage_n°{no_generateur}_installation_n°{no_installation}'])
    except CastError:
        pass

    try:
        generateur['type_energie'] = cast_str(ligne[f'Type_énergie_générateur_n°{no_generateur}_installation_n°{no_installation}'])
    except CastError:
        raise GenError("Type d'énergie de chauffage manquant")

    try:
        generateur['type_generateur'] = cast_str(ligne[f'Type_générateur_n°{no_generateur}_installation_n°{no_installation}'])
    except CastError:
        raise GenError('Type de générateur de chauffage manquant')

    try:
        generateur['usage'] = cast_str(ligne[f"Usage_générateur_n°{no_generateur}_installation_n°{no_installation}"])
    except CastError:
        raise GenError("Type d'usage invalide")

    return generateur


def generer_generateur_ecs(ligne: Ligne, installation_ecs: Ligne, no_generateur: int) -> Ligne:
    '''
    Extrait les données d'ECS d'un générateur.
    '''
    no_installation = installation_ecs['no_installation_ecs']
    generateur: Ligne = {
        'no_dpe': dpe['no_dpe'],
        'no_generateur': 3 + no_generateur,
        'no_installation_ecs': no_installation
    }

    generateur['conso_chauffage']           = 0
    generateur['conso_chauffage_depensier'] = 0

    try:
        generateur['conso_ecs']           = cast_conso(ligne[f'Conso_é_finale_générateur_ECS_n°{no_generateur}'])
        generateur['conso_ecs_depensier'] = cast_conso(ligne[f'Conso_é_finale_dépensier_générateur_ECS_n°{no_generateur}'])
    except CastError:
        generateur['conso_ecs']           = 0
        generateur['conso_ecs_depensier'] = 0

    try:
        generateur['description_generateur'] = cast_str(ligne[f'Description_générateur_ECS_n°{no_generateur}'])
    except CastError:
        pass

    try:
        generateur['date_installation_generateur'] = cast_str(ligne[f'Date_installation_générateur_ECS_n°{no_generateur}'])
    except CastError:
        pass

    try:
        generateur['type_energie'] = cast_str(ligne[f'Type_énergie_générateur_ECS_n°{no_generateur}'])
    except CastError:
        raise GenError("Type d'énergie d'ECS manquant")

    try:
        generateur['type_generateur'] = cast_str(ligne[f'Type_générateur_ECS_n°{no_generateur}'])
    except CastError:
        raise GenError("Type de générateur d'ECS manquant")

    try:
        generateur['usage'] = cast_str(ligne[f"Usage_générateur_ECS_n°{no_generateur}"])
    except CastError:
        raise GenError("Type d'usage invalide")

    return generateur


def combiner_generateurs(generateurs_chauffage: list[Ligne], generateurs_ecs: list[Ligne]) -> list[Ligne]:
    '''
    Combine les données de chauffage et d'ECS de générateurs, si possible.
    '''
    generateurs_chauffage_simple     = list(filter(lambda g: g['usage'] == 'chauffage', generateurs_chauffage))
    generateurs_chauffage_a_combiner = list(filter(lambda g: g['usage'] == 'chauffage + ecs', generateurs_chauffage))

    generateurs_ecs_simple     = list(filter(lambda g: g['usage'] == 'ecs', generateurs_ecs))
    generateurs_ecs_a_combiner = list(filter(lambda g: g['usage'] == 'chauffage + ecs', generateurs_ecs))

    for generateur_chauffage in generateurs_chauffage_a_combiner:
        generateur_ecs = None

        potentiels = [ g for g in generateurs_ecs_a_combiner if g['type_generateur'] == generateur_chauffage['type_generateur'] ]
        if potentiels:
            generateur_ecs = potentiels[0]
        else:
            potentiels = [ g for g in generateurs_ecs_a_combiner if g['type_energie'] == generateur_chauffage['type_energie'] ]
            if len(potentiels) == 1:
                generateur_ecs = potentiels[0]

        if generateur_ecs:
            generateurs_ecs_a_combiner.remove(generateur_ecs)
            generateur_chauffage['no_installation_ecs'] = generateur_ecs['no_installation_ecs']
            generateur_chauffage['conso_ecs']           = generateur_ecs['conso_ecs']
            generateur_chauffage['conso_ecs_depensier'] = generateur_ecs['conso_ecs_depensier']
            if 'no_installation_solaire' in generateur_ecs:
                generateur_chauffage['no_installation_solaire']      = generateur_ecs['no_installation_solaire']
            if 'description_generateur' not in generateur_chauffage and 'description_generateur' in generateur_ecs:
                generateur_chauffage['description_generateur']       = generateur_ecs['description_generateur']
            if 'date_installation_generateur' not in generateur_chauffage and 'date_installation_generateur' in generateur_ecs:
                generateur_chauffage['date_installation_generateur'] = generateur_ecs['date_installation_generateur']

    generateurs = generateurs_chauffage_simple + generateurs_ecs_simple + generateurs_chauffage_a_combiner + generateurs_ecs_a_combiner

    for generateur in generateurs:
        del generateur['usage']

    return generateurs


with open(fichier_src, 'rb') as f:
    def _make_gen(reader):
        while True:
            b = reader(2 ** 16)
            if not b: break
            yield b
    nb_lignes = sum(buf.count(b"\n") for buf in _make_gen(f.raw.read))
nb_lignes      -= 1
nb_lignes_log10 = 1 + int(math.log10(nb_lignes))

with open(fichier_src, 'r', encoding='utf-8-sig') as src, \
     open('data/departements.csv'           , 'w', newline='') as out_departement, \
     open('data/communes.csv'               , 'w', newline='') as out_commune, \
     open('data/logements.csv'              , 'w', newline='') as out_logement, \
     open('data/dpes.csv'                   , 'w', newline='') as out_dpe, \
     open('data/installations_chauffage.csv', 'w', newline='') as out_installation_chauffage, \
     open('data/installations_ecs.csv'      , 'w', newline='') as out_installation_ecs, \
     open('data/installations_solaire.csv'  , 'w', newline='') as out_installation_solaire, \
     open('data/generateurs.csv'            , 'w', newline='') as out_generateur:

    table_departement = csv.DictWriter(out_departement, [
        'no_departement',
        'no_region',
        'zone_climatique'
    ])
    table_departement.writeheader()

    table_commune = csv.DictWriter(out_commune, [
        'code_insee',
        'no_departement',
        'nom_commune',
        'code_postal'
    ])
    table_commune.writeheader()

    table_logement = csv.DictWriter(out_logement, [
        'id_logement',
        'code_insee',
        'annee_construction',
        'type_batiment',
        'type_installation_chauffage',
        'type_instalation_ecs',
        'hauteur_sous_plafond',
        'nb_niveau',
        'surface_habitable',
        'classe_inertie',
        'typologie',
    ])
    table_logement.writeheader()

    table_dpe = csv.DictWriter(out_dpe, [
        'no_dpe',
        'id_logement',
        'date_reception',
        'date_etablissement',
        'date_visite',
        'dpe_remplace',
        'date_fin_validite',
        'version',
        'appartement_non_visite',
        'no_immatriculation_copropriete',
        'invariant_fiscal_logement',
        'etiquette_ges',
        'etiquette_dpe',
        'type_ventilation',
        'surface_ventilee',
        'type_enr',
        'conso_enr',
        'production_enr',
        'surface_capteurs_pv'
    ])
    table_dpe.writeheader()

    table_installation_chauffage = csv.DictWriter(out_installation_chauffage, [
        'no_dpe',
        'no_installation_chauffage',
        'description_installation_chauffage',
        'type_installation_chauffage',
        'configuration_installation_chauffage',
        'surface_chauffee',
        'type_emetteur_chauffage'
    ])
    table_installation_chauffage.writeheader()

    table_installation_ecs = csv.DictWriter(out_installation_ecs, [
        'no_dpe',
        'no_installation_ecs',
        'description_installation_ecs',
        'type_installation_ecs',
        'configuration_installation_ecs'
    ])
    table_installation_ecs.writeheader()

    table_installation_solaire = csv.DictWriter(out_installation_solaire, [
        'no_dpe',
        'no_installation_solaire',
        'type_installation_solaire',
        'facteur_couverture_solaire'
    ])
    table_installation_solaire.writeheader()

    table_generateur = csv.DictWriter(out_generateur, [
        'no_dpe',
        'no_generateur',
        'no_installation_chauffage',
        'no_installation_ecs',
        'no_installation_solaire',
        'conso_chauffage',
        'conso_chauffage_depensier',
        'conso_ecs',
        'conso_ecs_depensier',
        'description_generateur',
        'date_installation_generateur',
        'type_energie',
        'type_generateur'
    ])
    table_generateur.writeheader()

    for i, ligne in zip(itertools.count(1), csv.DictReader(src)):
        try:
            no_dpe = cast_str(ligne['N°DPE'])
            #print(f'Traitement du DPE {no_dpe} ({f"{i}".rjust(nb_lignes_log10)}/{nb_lignes})...')

            try:
                departement = generer_departement(ligne)
                commune     = generer_commune(ligne, departement)
                logement    = generer_logement(ligne, commune)

                if logement['type_batiment'] == 'immeuble':
                    continue

                dpe = generer_dpe(ligne, no_dpe, logement)

                installations_chauffage = []
                generateurs_chauffage   = []
                for no_installation in range(1, 3):
                    try:
                        installation_chauffage = generer_installation_chauffage(ligne, dpe, no_installation)

                        generateurs_installation_chauffage = []
                        for no_generateur in range(1, 3):
                            try:
                                generateurs_installation_chauffage.append(generer_generateur_chauffage(ligne, installation_chauffage, no_generateur))
                            except GenError:
                                pass
                        if not generateurs_installation_chauffage:
                            raise GenError()

                        installations_chauffage.append(installation_chauffage)
                        generateurs_chauffage += generateurs_installation_chauffage
                    except GenError:
                        pass

                installations_ecs = []
                generateurs_ecs   = []
                try:
                    installation_ecs = generer_installation_ecs(ligne, dpe)

                    generateurs_installation_ecs = []
                    for no_generateur in range(1, 3):
                        try:
                            generateurs_installation_ecs.append(generer_generateur_ecs(ligne, installation_ecs, no_generateur))
                        except GenError:
                            pass
                    if not generateurs_installation_ecs:
                        raise GenError()

                    installations_ecs.append(installation_ecs)
                    generateurs_ecs += generateurs_installation_ecs
                except GenError:
                    pass

                try:
                    installation_solaire = generer_installation_solaire(ligne, dpe)
                    for generateur_ecs in generateurs_ecs:
                        generateur_ecs['no_installation_solaire'] = 1
                except GenError:
                    installation_solaire = None
                    pass

                generateurs = combiner_generateurs(generateurs_chauffage, generateurs_ecs)

                if not generateurs:
                    raise GenError("Installations et générateurs invalides")

            except GenError as e:
                print(f"{no_dpe} : {e}")
                continue

            no_departement = departement['no_departement']
            if no_departement not in departements:
                departements[no_departement] = departement
                table_departement.writerow(departement)

            code_insee = commune['code_insee']
            if code_insee not in communes:
                communes[code_insee] = commune
                table_commune.writerow(commune)

            id_logement = logement['id_logement']
            if id_logement not in logements:
                logements[id_logement] = logement
                if 'id_ban' in logement:
                    logements_par_id_ban[logement['id_ban']] = id_logement
                    del logement['id_ban']
                if 'adresse_brute' in logement:
                    logements_par_adresse_brute[logement['adresse_brute']] = id_logement
                    del logement['adresse_brute']
                table_logement.writerow(logement)

            table_dpe.writerow(dpe)
            table_installation_chauffage.writerows(installations_chauffage)
            table_installation_ecs.writerows(installations_ecs)
            if installation_solaire:
                table_installation_solaire.writerow(installation_solaire)
            table_generateur.writerows(generateurs)

        except Exception as e:
            print(f'Traitement du DPE {no_dpe} ({f"{i}".rjust(nb_lignes_log10)}/{nb_lignes})...')
            raise e