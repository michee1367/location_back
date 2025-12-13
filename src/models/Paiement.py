from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)

class Paiement(db.Model):
    __fillables__ = ["date_paiement","montant","contrat_id","moyen_id"]
    __showables__ = ["id", "date_paiement","montant","reference","contrat_id","moyen_id"]
    __rel_showables__= ["contrat", "moyen_de_paiement"]
    __tablename__ = "paiement"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date_paiement = Column(Date, default=datetime.utcnow)
    montant = Column(DECIMAL(10, 2), nullable=False)
    reference = Column(String(100))

    contrat_id = Column(UUID(as_uuid=True), ForeignKey("contrat_de_bail.id"), nullable=False)
    moyen_id = Column(UUID(as_uuid=True), ForeignKey("moyen_de_paiement.id"), nullable=False)

    contrat = relationship("ContratDeBail", back_populates="paiements")
    moyen_de_paiement = relationship("MoyenDePaiement", back_populates="paiements")
    
    
    def getWording(self) :
        wording = ""
        if(self.contrat) :
            wording = wording + " " + self.contrat.getWording()
        if(self.moyen_de_paiement) :
            wording = wording + " " + self.moyen_de_paiement.getWording()

        return wording + " " + str(self.id)
