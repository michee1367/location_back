from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)

class Organisation(db.Model):
    __fillables__ = ["nom","serial_number","adresse","email","telephone", "devise", "sign_devise", "proprietaire_id"]
    __showables__ = ["id", "nom","serial_number","adresse","email","telephone", "devise", "sign_devise", "administrateur_id"]
    __rel_showables__= ["proprietaire", "administrateur"]
    __tablename__ = "organisation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nom = Column(String(100), nullable=False)
    adresse = Column(String(255))
    email = Column(String(120))
    telephone = Column(String(30))
    devise = Column(String(50), default="dolars")
    sign_devise = Column(String(50), default="$")

    proprietaire_id = Column(Integer, ForeignKey("utilisateur.id"))
    administrateur_id = Column(Integer, ForeignKey("administrateur_organisation.id"))
    
    proprietaire = relationship("User", back_populates="organisations", foreign_keys=[proprietaire_id])
    administrateur = relationship("AdministrateurOrganisation", back_populates="organisations_admin", foreign_keys=[administrateur_id])

    sites = relationship("Site", back_populates="organisation", cascade="all, delete-orphan")
    
    def getWording(self) :
        return self.nom
