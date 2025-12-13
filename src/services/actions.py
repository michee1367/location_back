import json
from models import db
from jsonschema import validate, exceptions
from services.ExceptionService import ExceptionService
#from services.unit import get_quantities, transform_quantity_data, transform_show, getSettingsWithoutUser, transform_record
#from models.Enregistrement import Enregistrement
from sqlalchemy.inspection import inspect
from datetime import datetime, timezone
import geopandas as gpd
import pandas as pd
from shapely import wkt 
#from models.TaskImport import CSV_IMPORT_TASK, EXCEL_IMPORT_TASK, ZIP_IMPORT_TASK, JSON_IMPORT_TASK, GEOJSON_IMPORT_TASK
import shutil
import os
from flask import current_app
from sqlalchemy import func
from shapely import wkt
import math
import numbers
from sqlalchemy import or_, and_
from tools.geo import wtkToJson
from services.picture import get_pic_url
#from models.EntityAdministration.territory import Territory
from tools.objects.PaginateReturn import PaginateReturn
from tools.model import get_attr_by_path
from middlewares.Middleware import PROP_NAME_MIDDLEWARE_ACTION
from services.middlewares.middleware import middleware_list_to_dict
from tools.emums import get_enums_from_model
from services.models import get_model_class_by_tablename

def run_middleware_action(name, table_name, entityId) :
    
    class_model = get_model_class_by_tablename(table_name)
    
    if not class_model : 
        raise ExceptionService("Model not found", 404)
    
    if not hasattr(class_model, PROP_NAME_MIDDLEWARE_ACTION) :
        raise ExceptionService("models doesn't have middleware action", 404)
    
    
    middleware_actions = getattr(class_model, PROP_NAME_MIDDLEWARE_ACTION)
    
    middleware_action = next(
        (m for m in middleware_actions if m.name == name),
        None
    )
    
    if not middleware_action :
        raise ExceptionService("middleware_action doesn't exits", 404)
    
    
    entity = class_model.query.filter(class_model.id == entityId).first()
    
    if not entity : 
        raise ExceptionService("entity not found", 404)
    
    return middleware_action.middleware.handle(entity)
    
    
    