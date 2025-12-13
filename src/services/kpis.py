from sqlalchemy import func, case
from datetime import datetime, timedelta

from models.AdministrateurOrganisation import AdministrateurOrganisation
from models.GestionnaireSite import GestionnaireSite
from models.LocateurUtilisateur import LocateurUtilisateur
from models.Organisation import Organisation
from models.ContratDeBail import ContratDeBail
from models.Appartement import Appartement
from models.MoyenDePaiement import MoyenDePaiement
from models.Paiement import Paiement
#from models.StockItem import StockItem
from models.Site import Site
from datetime import datetime
from sqlalchemy import func, or_
from models import db
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from collections import defaultdict


def nb_mois_non_paye_contrats_encours():
    
    session = db.session
    today = datetime.today()

    # Récupérer tous les contrats en cours
    contrats = session.query(ContratDeBail).filter(
        or_(ContratDeBail.date_fin == None, ContratDeBail.date_fin >= today)
    ).all()

    result = []

    for contrat in contrats:
        # Nombre de mois depuis le début du contrat
        nb_mois_depuis_debut = (today.year - contrat.date_debut.year) * 12 + (today.month - contrat.date_debut.month) + 1

        # Total payé depuis le début du contrat
        total_paye = session.query(func.coalesce(func.sum(Paiement.montant), 0))\
            .filter(Paiement.contrat_id == contrat.id)\
            .scalar() or 0

        # Nombre de mois payés
        nb_mois_paye = int(float(total_paye) // float(contrat.montant_loyer))

        # Mois non payés
        nb_mois_non_paye = max(nb_mois_depuis_debut - nb_mois_paye, 0)

        result.append(
            {
                "id": contrat.id,
                "libelle": contrat.getWording(),
                "garantie": contrat.duree_mois_garantie,
                "mois_non_paye": nb_mois_non_paye,
                "nb_mois_depuis_debut": nb_mois_depuis_debut,
                "nb_mois_paye": nb_mois_paye
            }
        ) 
    return result

def stats_contrats_encours():
    session = db.session
    today = datetime.today()

    # Récupérer les contrats en cours
    contrats = session.query(ContratDeBail).filter(
        or_(ContratDeBail.date_fin == None, ContratDeBail.date_fin >= today)
    ).all()

    total_mois_depuis_debut = 0
    total_mois_paye = 0
    total_mois_non_paye = 0
    total_montant_paye = 0
    total_montant_attendu = 0

    for contrat in contrats:
        # Mois écoulés depuis le début du contrat
        nb_mois_depuis_debut = (
            (today.year - contrat.date_debut.year) * 12
            + (today.month - contrat.date_debut.month)
            + 1
        )

        # Montant total payé
        montant_paye = session.query(
            func.coalesce(func.sum(Paiement.montant), 0)
        ).filter(
            Paiement.contrat_id == contrat.id
        ).scalar() or 0

        # Mois payés
        nb_mois_paye = int(float(montant_paye) // float(contrat.montant_loyer))

        # Mois non payés
        nb_mois_non_paye = max(nb_mois_depuis_debut - nb_mois_paye, 0)

        # Montant total attendu
        montant_attendu = nb_mois_depuis_debut * contrat.montant_loyer

        # Totaux globaux
        total_mois_depuis_debut += nb_mois_depuis_debut
        total_mois_paye += nb_mois_paye
        total_mois_non_paye += nb_mois_non_paye
        total_montant_paye += montant_paye
        total_montant_attendu += montant_attendu

    # Taux d’argent restant à payer
    if total_montant_attendu > 0:
        taux_non_paye = ((total_montant_attendu - total_montant_paye) / total_montant_attendu) * 100
    else:
        taux_non_paye = 0

    return {
        "total_mois_depuis_debut": total_mois_depuis_debut,
        "total_mois_paye": total_mois_paye,
        "total_mois_non_paye": total_mois_non_paye,
        "total_montant_paye": total_montant_paye,
        "total_montant_attendu": total_montant_attendu,
        "taux_non_paye_percent": round(taux_non_paye, 2)
    }

def stats_10_derniers_mois():
    session = db.session
    today = datetime.today()

    # Début de la fenêtre : 10 mois en arrière
    start_date = (today.replace(day=1) - relativedelta(months=9)).date()

    # Tous contrats actifs dans la période
    contrats = session.query(ContratDeBail).filter(
        or_(
            ContratDeBail.date_fin == None,
            ContratDeBail.date_fin >= start_date
        )
    ).all()

    # Tous paiements de la période
    paiements = session.query(Paiement).filter(
        Paiement.date_paiement >= start_date
    ).all()

    # Paiements regroupés par YYYY-MM
    paiements_par_mois = defaultdict(float)
    for p in paiements:
        key = p.date_paiement.strftime("%Y-%m")
        paiements_par_mois[key] += float(p.montant)

    # Initialisation (10 mois)
    stats = {}
    current = start_date

    for _ in range(10):
        key = current.strftime("%Y-%m")
        stats[key] = {"attendu": 0, "paye": 0}
        # add 1 month
        current = (current + relativedelta(months=1)).replace(day=1)

    # Calcul du montant attendu par contrat
    for contrat in contrats:
        current = max(contrat.date_debut, start_date)

        # aller au premier jour du mois
        current = current.replace(day=1)

        fin = today.replace(day=1).date()

        while current <= fin:
            key = current.strftime("%Y-%m")

            if key in stats:
                stats[key]["attendu"] += float(contrat.montant_loyer)

            current = (current + relativedelta(months=1)).replace(day=1)

    # Ajout des paiements
    for key, montant in paiements_par_mois.items():
        if key in stats:
            stats[key]["paye"] += montant

    # Format du résultat final
    result = []
    for key in sorted(stats.keys()):
        attendu = stats[key]["attendu"]
        paye = stats[key]["paye"]

        taux = 0 if attendu == 0 else round((attendu - paye) / attendu * 100, 2)

        result.append({
            "mois": key,
            "montant_attendu": attendu,
            "montant_paye": paye,
            "taux_non_paye_percent": taux
        })

    return result

def stats_par_mois():
    session = db.session
    today = datetime.today()

    # On récupère tous les paiements
    paiements = session.query(Paiement).all()
    contrats = session.query(ContratDeBail).filter(
        or_(ContratDeBail.date_fin == None, ContratDeBail.date_fin >= today)
    ).all()

    # Organiser les paiements par mois YYYY-MM
    paiements_par_mois = defaultdict(float)
    for p in paiements:
        key = p.date_paiement.strftime("%Y-%m")
        paiements_par_mois[key] += float(p.montant)

    # Résultat final
    stats = defaultdict(lambda: {"attendu": 0, "paye": 0})

    for contrat in contrats:
        # Période entre date_debut et today
        current = contrat.date_debut.replace(day=1)
        fin = today.replace(day=1)

        while current <= fin:
            key = current.strftime("%Y-%m")

            # montant attendu pour ce contrat ce mois-là
            stats[key]["attendu"] += float(contrat.montant_loyer)

            # passe au mois suivant
            if current.month == 12:
                current = date(current.year + 1, 1, 1)
            else:
                current = date(current.year, current.month + 1, 1)

    # Ajouter les paiements
    for key, montant in paiements_par_mois.items():
        stats[key]["paye"] += montant

    # Convertir en liste triée
    result = []
    for key in sorted(stats.keys()):
        attendu = stats[key]["attendu"]
        paye = stats[key]["paye"]
        taux = 0 if attendu == 0 else round((attendu - paye) / attendu * 100, 2)

        result.append({
            "mois": key,
            "montant_attendu": attendu,
            "montant_paye": paye,
            "taux_non_paye_percent": taux
        })

    return result


def stats_depuis_plus_ancien_contrat():
    session = db.session
    today = datetime.today().date()

    # Trouver le contrat en cours le plus ancien
    plus_ancien = session.query(ContratDeBail).filter(
        or_(ContratDeBail.date_fin == None, ContratDeBail.date_fin >= today)
    ).order_by(ContratDeBail.date_debut.asc()).first()

    if not plus_ancien:
        return []

    # Date de départ = début du contrat le plus ancien
    date_depart = plus_ancien.date_debut.replace(day=1)

    # Génère tous les mois jusqu’à aujourd’hui
    mois_list = []
    current = date_depart

    while current <= today.replace(day=1):
        mois_list.append(current)
        current = (current + relativedelta(months=1)).replace(day=1)

    # Si plus de 10 mois → garder les 10 derniers
    if len(mois_list) > 10:
        mois_list = mois_list[-10:]

    # Appelons cela la fenêtre d’analyse
    mois_keys = [m.strftime("%Y-%m") for m in mois_list]
    date_min = mois_list[0]

    # --- Récupérer contrats actifs dans la fenêtre complète ---
    contrats = session.query(ContratDeBail).filter(
        or_(ContratDeBail.date_fin == None, ContratDeBail.date_fin >= date_min)
    ).all()

    # --- Paiements sur la période ---
    paiements = session.query(Paiement).filter(
        Paiement.date_paiement >= date_min
    ).all()

    paiements_par_mois = defaultdict(float)
    for p in paiements:
        key = p.date_paiement.strftime("%Y-%m")
        paiements_par_mois[key] += float(p.montant)

    # --- Initialisation des stats ---
    stats = {key: {"attendu": 0, "paye": 0} for key in mois_keys}

    # --- Loyer attendu par mois pour chaque contrat ---
    for contrat in contrats:
        # point de départ du contrat dans la fenêtre
        start = max(contrat.date_debut.replace(day=1), date_min)
        end = today.replace(day=1)

        current = start
        while current <= end:
            key = current.strftime("%Y-%m")
            if key in stats:
                stats[key]["attendu"] += float(contrat.montant_loyer)

            current = (current + relativedelta(months=1)).replace(day=1)

    # --- Ajouter les paiements ---
    for key, montant in paiements_par_mois.items():
        if key in stats:
            stats[key]["paye"] += montant

    # --- Formater les résultats ---
    result = []
    for key in mois_keys:
        attendu = stats[key]["attendu"]
        paye = stats[key]["paye"]

        taux = 0 if attendu == 0 else round((attendu - paye) / attendu * 100, 2)

        result.append({
            "mois": key,
            "montant_attendu": attendu,
            "montant_paye": paye,
            "taux_non_paye_percent": taux
        })

    return result


def stats_loyer_par_mois():
    session = db.session
    today = datetime.today().date()

    # --- 1. Trouver le contrat en cours le plus ancien
    plus_ancien = session.query(ContratDeBail).filter(
        or_(ContratDeBail.date_fin == None, ContratDeBail.date_fin >= today)
    ).order_by(ContratDeBail.date_debut.asc()).first()

    if not plus_ancien:
        return {}

    # Date de départ = début du plus ancien contrat
    date_depart = plus_ancien.date_debut.replace(day=1)

    # --- 2. Générer mois jusqu’à aujourd’hui
    mois = []
    current = date_depart
    while current <= today.replace(day=1):
        mois.append(current)
        current = (current + relativedelta(months=1)).replace(day=1)

    # Ne garder que les 10 derniers mois
    if len(mois) > 10:
        mois = mois[-10:]

    mois_keys = [m.strftime("%Y-%m") for m in mois]
    date_min = mois[0]

    # --- 3. Récupérer les contrats encore actifs dans cette période
    contrats = session.query(ContratDeBail).filter(
        or_(ContratDeBail.date_fin == None, ContratDeBail.date_fin >= date_min)
    ).all()

    # --- 4. Paiements depuis la période minimale
    paiements = session.query(Paiement).filter(
        Paiement.date_paiement >= date_min
    ).all()

    paiements_par_mois_et_contrat = defaultdict(lambda: defaultdict(float))

    for p in paiements:
        key = p.date_paiement.strftime("%Y-%m")
        paiements_par_mois_et_contrat[key][p.contrat_id] += float(p.montant)

    # --- 5. Calcul des montants attendus par mois
    attendu_par_mois_et_contrat = defaultdict(lambda: defaultdict(float))

    for contrat in contrats:
        start = max(contrat.date_debut.replace(day=1), date_min)
        end = today.replace(day=1)

        current = start
        while current <= end:
            key = current.strftime("%Y-%m")
            attendu_par_mois_et_contrat[key][contrat.id] += float(contrat.montant_loyer)
            current = (current + relativedelta(months=1)).replace(day=1)

    # --- 6. Statistiques par mois
    stats = []

    for key in mois_keys:
        attendu_contrats = attendu_par_mois_et_contrat[key]
        paye_contrats = paiements_par_mois_et_contrat[key]

        total_attendu = sum(attendu_contrats.values())
        total_paye = sum(paye_contrats.values())

        # Nombre de contrats considérés
        nb_contrats = len(attendu_contrats)

        # --- Comptage par mois ---
        contrats_totalement_payes = 0
        contrats_en_retard = 0

        for contrat_id, attendu in attendu_contrats.items():
            paye = paye_contrats.get(contrat_id, 0)

            if paye >= attendu:
                contrats_totalement_payes += 1
            else:
                contrats_en_retard += 1

        taux_non_paye = 0 if total_attendu == 0 else \
            round((total_attendu - total_paye) / total_attendu * 100, 2)

        stats.append( {
            "mois": key,
            "contrats": nb_contrats,
            "contrats_totalement_payes": contrats_totalement_payes,
            "contrats_en_retard": contrats_en_retard,
            "attendu": total_attendu,
            "paye": total_paye,
            "taux_non_paye_percent": taux_non_paye
        })

    return stats
