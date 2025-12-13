from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)

class MoyenDePaiement(db.Model):
    __fillables__ = ["type","serial_number","details"]
    __showables__ = ["id", "type","serial_number","details"]
    __rel_showables__= ["asset_type"]
    __tablename__ = "moyen_de_paiement"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(50), nullable=False)  # Mobile, Banque, Cash
    details = Column(String(255))

    paiements = relationship("Paiement", back_populates="moyen_de_paiement")
    
    def getWording(self) :
        return self.type
    