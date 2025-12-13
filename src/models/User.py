#from flask_sqlalchemy import SQLAlchemy
import uuid
#db = SQLAlchemy()
from models import db
from geoalchemy2.types import Geometry
#from models.MetaRecord import MetaRecord
from datetime import datetime, timezone

from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import (
    Column, String, DateTime, Enum as PgEnum, ForeignKey,
    DECIMAL, Integer, Text, Date, Boolean
)
from enums.UserRole import UserRole
from sqlalchemy.orm import relationship

#from app import bcrypt
from extensions import bcrypt

from decorators.models import decorate_model_middleware_action
#from middlewares.UserChildable import UserChildable
#from models.GestionnaireSite import GestionnaireSite
# Creating the Inserttable for inserting data into the database

#@decorate_model_middleware_action(UserChildable, clsChild = GestionnaireSite)
class User(db.Model):
    '''table des utilisateurs.'''

    __tablename__ = 'utilisateur'
    __fillables__ = ["nom", "post_nom","picture","prenom","email","phone"]
    __showables__ = ["id","nom", "post_nom","picture","prenom","email","phone"]
    __rel_showables__=[]
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    #id = db.Column(Integer, primary_key=True, default=uuid.uuid4)
    uniq_key = db.Column("uniq_key",db.String(80), nullable=True) # nom
    nom = db.Column("nom",db.String(80), nullable=True) # nom
    post_nom = db.Column("post_nom",db.String(80), nullable=True) # nom
    picture = db.Column("picture",db.String(255), nullable=True) # nom
    prenom = db.Column("prenom",db.String(80), nullable=True) # nom
    email = db.Column("email",db.String(80), nullable=False) # nom
    phone = db.Column("phone",db.String(80), nullable=True) # nom
    password = db.Column("password",db.String(255), nullable=True)
    
    roles = db.Column("roles",postgresql.ARRAY(db.String(80)), nullable=True) # nom
    #role = Column(PgEnum(UserRole))
    other_data = db.Column("other_data",postgresql.JSON) # other property
    
    activate_at = db.Column("activate_at",db.DateTime, nullable=True)
    deactivate_at = db.Column("deactivate_at",db.DateTime, nullable=True)
    
    qrcode_path = db.Column("qrcode_path",db.String(255), nullable=True)
    
    created_at = db.Column("created_at",db.DateTime, nullable=True, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        nullable=True,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )
    
    deleted_at = db.Column("deleted_at",db.DateTime, nullable=True)
    # Relations communes
    organisations = relationship("Organisation", back_populates="proprietaire")
    
    # Méthode pour convertir le modèle en dictionnaire
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name != "password"}

    def getRoles(self) :
        if self.roles is None :
            return ["ROLE_VISITOR"]
        return self.roles
    
    def get_full_name(self) :
        return self.nom + " " + self.post_nom + " " + self.prenom
    
    def setUniqKey(self) :
        pg_id = ""
        if self.nom :
            pg_id = pg_id + "-" + str(self.nom)
        if self.prenom :
            pg_id = pg_id + "-" + str(self.prenom)
        if self.post_nom :
            pg_id = pg_id + "-" + str(self.post_nom)
            
        self.uniq_key = pg_id
    # method used to represent a class's objects as a string
    
    
    # ✅ méthode pour définir le mot de passe
    def set_password(self, password: str):
        """Hache et stocke le mot de passe"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # ✅ méthode pour vérifier le mot de passe
    def check_password(self, password: str) -> bool:
        """Vérifie si le mot de passe correspond""" 
        if not self.password:
            return False

        try:
            valid = bcrypt.check_password_hash(self.password, password)

            return valid

        except Exception:
            return False
        
    
    def getWording(self) :
        return self.get_full_name() + " " + str(self.id)
    
    def __repr__(self):
        return '<users %r>' % self.email
    

    
