import json
from flask import jsonify
from models import db
#, db
  
#from services.compress.model import get_search_model_compress
#from services.data_tempo import validate_data
  
#from services.import_file import get_data_import
#from services.data_tempo import get_records
#from services.form_service import insert_data
from services.ExceptionService import ExceptionService
from flask import request
from sqlalchemy import text
from flask import current_app, send_file, after_this_request
import os
from services.kpis import nb_mois_non_paye_contrats_encours, stats_contrats_encours, stats_10_derniers_mois, stats_par_mois,\
  stats_depuis_plus_ancien_contrat, stats_loyer_par_mois
import shutil
from flask import Response


#MetaRecordController
def get_nb_mois_non_paye_contrats_encours():
    """
    tous les contrat en cours avec le nombre de mois deja payé
    ---
    responses:
      200:
        description: tous les contrat en cours avec le nombre de mois deja payé 
        examples:
          application/json: {
            "data": [
                {
                    "id": contrat.id,
                    "libelle": contrat.getWording(),
                    "mois_non_paye": nb_mois_non_paye,
                    "nb_mois_depuis_debut": nb_mois_depuis_debut,
                    "nb_mois_paye": nb_mois_paye
                }
            ]
        }
    """
    return jsonify(nb_mois_non_paye_contrats_encours())



def get_stats_contrats_encours():
    """
    statistique des contrats
    ---
    responses:
      200:
        description: statistique des contrats 
        examples:
          application/json: {
            "data": {
                    "total_mois_depuis_debut": total_mois_depuis_debut,
                    "total_mois_paye": total_mois_paye,
                    "total_mois_non_paye": total_mois_non_paye,
                    "total_montant_paye": total_montant_paye,
                    "total_montant_attendu": total_montant_attendu,
                    "taux_non_paye_percent": round(taux_non_paye, 2)
                }
        }
    """
    return jsonify(stats_contrats_encours())
  
  
stats_10_derniers_mois, stats_par_mois

def get_stats_10_derniers_mois():
    """
    stats_10_derniers_mois
    ---
    responses:
      200:
        description: stats_10_derniers_mois
        examples:
          application/json: {
            "data": [
            {
              "mois": "2024-01",
              "montant_attendu": 300000,
              "montant_paye": 200000,
              "taux_non_paye_percent": 33.33
            },
            {
              "mois": "2024-02",
              "montant_attendu": 300000,
              "montant_paye": 300000,
              "taux_non_paye_percent": 0
            }
          ]
        }
    """
    return jsonify(stats_loyer_par_mois())
  
  

def get_stats_par_mois():
    """
    stats_par_mois
    ---
    responses:
      200:
        description: stats_par_mois
        examples:
          application/json: {
            "data": [
            {
              "mois": "2024-01",
              "montant_attendu": 300000,
              "montant_paye": 200000,
              "taux_non_paye_percent": 33.33
            },
            {
              "mois": "2024-02",
              "montant_attendu": 300000,
              "montant_paye": 300000,
              "taux_non_paye_percent": 0
            }
          ]
        }
    """
    return jsonify(stats_par_mois())
  
  
