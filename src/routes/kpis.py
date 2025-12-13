



from flask import Blueprint
from controllers.KPIController import get_nb_mois_non_paye_contrats_encours, get_stats_contrats_encours, get_stats_10_derniers_mois,\
    get_stats_par_mois
from services.auth_service import auth_required
from hashlib import pbkdf2_hmac

kpi = Blueprint('kpi', __name__)

kpi.route("/get_nb_mois_non_paye_contrats_encours", methods=["GET"])(get_nb_mois_non_paye_contrats_encours)
kpi.route("/get_stats_contrats_encours", methods=["GET"])(get_stats_contrats_encours)
kpi.route("/get_stats_10_derniers_mois", methods=["GET"])(get_stats_10_derniers_mois)
kpi.route("/get_stats_par_mois", methods=["GET"])(get_stats_par_mois)
