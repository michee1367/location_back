from enums.MiddlewareType import MiddlewareType
from models.User import User
from tools.str_tools import generer_chaine_alea, sub_speciaux
from flask import current_app, send_file, after_this_request
import os
import base64
import qrcode
from models import db
from middlewares.Middleware import Middleware
from enums.ActionMiddlewareRetrunType import ActionMiddlewareRetrunType

class Qrcorable(Middleware) :
    
    def getType(self) :
        return MiddlewareType.ACTION
    
    
    def getWordingAction(self) :
        return "generer Qrcode"
    
    def getReturnType(self) :
        return ActionMiddlewareRetrunType.DOWNLOAD
    
    
    def handle(self, entity : User, **args) :
        
        phone = entity.phone
        password = generer_chaine_alea()
        
        
        #change pwd
        entity.set_password(password)
        db.session.commit()
                
        credentials = str(phone) + ":" + str(password)
        
        credentials_bytes = credentials.encode("utf-8")
        
        # Encodage Base64
        credentials_bytes_base64_bytes = base64.b64encode(credentials_bytes)

        # Conversion en string lisible
        credentials_base64 = credentials_bytes_base64_bytes.decode("utf-8")
        
        QRCODE_ACTION_URL = current_app.config["QRCODE_ACTION_URL"]
        
        url = str(QRCODE_ACTION_URL) + "?token="+ str(credentials_base64)
        
        # Création du QR code
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4
        )

        qr.add_data(url)
        qr.make(fit=True)
        
        # Image du QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        FOLDER_QRCODE = current_app.config["FOLDER_QRCODE"]
        os.makedirs(FOLDER_QRCODE, exist_ok=True)
        
        filename =  sub_speciaux(entity.phone) + "_" + generer_chaine_alea(3)
        
        path_qrcode = FOLDER_QRCODE + "/" + filename + ".png"
        entity.qrcode_path = path_qrcode
        
        db.session.commit()
        
        # Sauvegarde
        img.save(path_qrcode)
        
        @after_this_request
        def remove_file(response):
            try:
                os.remove(path_qrcode)
                print(f"Fichier temporaire {path_qrcode} supprimé.")
                
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier : {e}")
            return response
        # Ensuite envoyer le fichier
        response = send_file(   
            path_qrcode,
            as_attachment=True,
            download_name=os.path.basename(path_qrcode),
            mimetype="image/png"
        )

        response.headers["Content-Disposition"] = f"attachment; filename={filename}.png"
        response.headers["Content-Type"] = "image/png"
        
        return response
    
    def to_dict(self):
        return {
            "wording":self.getWordingAction(),
            "returnType":self.getReturnType().value
        }