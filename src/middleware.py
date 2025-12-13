from services.middlewares.middleware import add_model_middleware_action
from middlewares.UserChildable import UserChildable
from middlewares.Qrcorable import Qrcorable
from middlewares.Pdfable import Pdfable
from models.User import User
from models.GestionnaireSite import GestionnaireSite
from models.AdministrateurOrganisation import AdministrateurOrganisation
from models.LocateurUtilisateur import LocateurUtilisateur
from models.Paiement import Paiement
from enums.ActionMiddlewareRetrunType import ActionMiddlewareRetrunType



def init_middleware() :
    add_model_middleware_action(
        LocateurUtilisateur, Qrcorable, 
        "qrcode"
    )
    add_model_middleware_action(
        User, UserChildable, 
        "user_manager_site",
        clsChild=GestionnaireSite, 
        wording = "rendre gestionnaire site"
    )
    add_model_middleware_action(
        User, 
        UserChildable, 
        "user_admin_org", 
        clsChild=AdministrateurOrganisation, 
        wording = "rendre administrateur organisation"
    )
    add_model_middleware_action(
        User, 
        UserChildable, 
        "user_locateur", 
        clsChild=LocateurUtilisateur, 
        wording = "rendre locateur"
    )
    add_model_middleware_action(
        Paiement, Pdfable, 
        "billing"
    )