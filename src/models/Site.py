from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)

class Site(db.Model):
    __fillables__ = ["nom","adresse","ville","organisation_id","gestionnaire_id"]
    __showables__ = ["id", "nom","adresse","ville","organisation_id","gestionnaire_id"]
    __rel_showables__= ["organisation", "gestionnaire"]
    __tablename__ = "site"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nom = Column(String(100), nullable=False)
    adresse = Column(String(255))
    ville = Column(String(100))

    organisation_id = Column(UUID(as_uuid=True), ForeignKey("organisation.id"), nullable=False)
    organisation = relationship("Organisation", back_populates="sites")
    
    
    gestionnaire_id = Column(Integer, ForeignKey("gestionnaire_site.id"))
    gestionnaire = relationship("GestionnaireSite", back_populates="sites")

    appartements = relationship("Appartement", back_populates="site", cascade="all, delete-orphan")
    
    def getWording(self) :
        return self.nom + " " + self.ville
    
