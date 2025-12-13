from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)
from models.User import User

class LocateurUtilisateur(User):
    __tablename__ = "locateur_utilisateur"
    __fillables__ = ["nom", "post_nom","prenom","email","phone", "adresse"]
    __showables__ = ["id","nom", "post_nom","prenom","email","phone", "adresse"]
    __rel_showables__=[]

    id = Column(Integer, ForeignKey("utilisateur.id"), primary_key=True)
    adresse = Column(String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'locateur'
    }

    contrats = relationship("ContratDeBail", back_populates="locateur_utilisateur")
    
    def getWording(self) :
        return self.get_full_name() + " " + str(self.id)
