from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)
from models.User import User

class AdministrateurOrganisation(User):
    __tablename__ = "administrateur_organisation"
    __fillables__ = ["nom", "post_nom","prenom","email","phone", "date_ajout"]
    __showables__ = ["id", "nom", "post_nom","picture","prenom","email","phone", "date_ajout"]
    __rel_showables__=[]

    id = Column(Integer, ForeignKey("utilisateur.id"), primary_key=True)
    date_ajout = Column(DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'administrateur_organisation'
    }

    # Relation spécifique
    organisations_admin = relationship("Organisation", back_populates="administrateur")
    
    def getWording(self) :
        return self.get_full_name() + " " + str(self.id)
