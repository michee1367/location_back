from enums.MiddlewareType import MiddlewareType
from tools.str_tools import generer_chaine_alea, sub_speciaux
from flask import current_app, send_file, after_this_request, jsonify
import os
import base64
import qrcode
from models import db
from enums.ActionMiddlewareRetrunType import ActionMiddlewareRetrunType

PROP_NAME_MIDDLEWARE_ACTION="__models_middleware_actions__"

class Middleware() :

    def __init__(self, *args, **kwargs):
        pass
    
    def getType(self) :
        return MiddlewareType.ACTION
    
    def getReturnType(self) :
        return ActionMiddlewareRetrunType.REFRECH
    
    def getWordingAction() :
        return "action"
    
    def handle(self, entity, *args, **kwargs) :
        return jsonify({"args":args, "kwargs":kwargs}), 200
    
    @staticmethod
    def check(*args, **kwargs) :
        return True
    
    def to_dict(self):
        return {
            "wording":self.getWordingAction(),
            "returnType":self.getReturnType().value
        }