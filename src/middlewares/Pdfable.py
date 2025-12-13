from enums.MiddlewareType import MiddlewareType
from models.User import User
from models.Paiement import Paiement
from tools.str_tools import generer_chaine_alea, sub_speciaux
from flask import current_app, send_file, after_this_request
import os
import base64
import qrcode
from models import db
from middlewares.Middleware import Middleware
from enums.ActionMiddlewareRetrunType import ActionMiddlewareRetrunType
from flask import jsonify
from datetime import datetime
from services.bill import generate_facture_pdf

class Pdfable(Middleware) :
    
    def getType(self) :
        return MiddlewareType.ACTION
    
    
    def getWordingAction(self) :
        return "generer facture"
    
    def getReturnType(self) :
        return ActionMiddlewareRetrunType.DOWNLOAD
    
    
    def handle(self, entity : Paiement, **args) :
        
        if not isinstance(entity, Paiement) :
            return jsonify({"message":"enetité non conforme"}), 400
        
        annee = datetime.now().year
        entity.reference = "refs/" + str(entity.id) + "/" + str(annee)
        
        filename = "refs_" + str(entity.id) + "_" + str(annee)
        #change ref
        db.session.commit()
        
        filepath = generate_facture_pdf(entity)
        
        @after_this_request
        def remove_file(response):
            try:
                os.remove(filepath)
                print(f"Fichier temporaire {filepath} supprimé.")
                
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier : {e}")
            return response
        # Ensuite envoyer le fichier
        response = send_file(   
            filepath,
            as_attachment=True,
            download_name=os.path.basename(filepath),
        )

        response.headers["Content-Disposition"] = f"attachment; filename={filename}.pdf"
        
        return response
    
    def to_dict(self):
        return {
            "wording":self.getWordingAction(),
            "returnType":self.getReturnType().value
        }