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
from services.actions import run_middleware_action
from flask import request
from sqlalchemy import text
from flask import current_app, send_file, after_this_request
import os
#from services.import_file import upload_file
import shutil
from flask import Response



def run_action(table_name, name, record_id):
    """
    run action of name, a table and id
    ---
    parameters:
      - name: table_name
        in: path
        type: string
        required: true
        description: nom de la table
      - name: name
        in: path
        type: string
        required: true
        description: Nom de l'action
      - name: record_id
        in: path
        type: integer
        required: true
        description: identifiant de l'enregistrement
    responses:
        200:
          description: All save data of the model with pagination info
          examples:
            application/json: 
              {
                "data": {
                    "id": 1,
                    "denomination": "Peche de poisson capitain",
                    "geomCentroid": null,
                    "production_actuelle": 40000.0,
                    "production_potentielle": 40000.0,
                    "territoire_id": null,
                    "type_id": null
                  }
              }
"""
    return run_middleware_action(name, table_name, record_id)