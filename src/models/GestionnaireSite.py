from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)
from models.User import User

class GestionnaireSite(User):
    __tablename__ = "gestionnaire_site"
    __fillables__ = ["nom", "post_nom","prenom","email","phone", "date_affectation"]
    __showables__ = ["id", "nom", "post_nom","prenom","email","phone", "date_affectation"]
    __rel_showables__=[]

    id = Column(Integer, ForeignKey("utilisateur.id"), primary_key=True)
    date_affectation = Column(DateTime, default=datetime.utcnow)
    
    sites = relationship("Site", back_populates="gestionnaire")
    

    __mapper_args__ = {
        'polymorphic_identity': 'gestionnaire_site'
    }
    def getWording(self) :
        return self.get_full_name() + " " + str(self.id)
