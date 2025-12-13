from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)

class Appartement(db.Model):
    __fillables__ = ["code","surface","nb_chambres","loyer_mensuel", "site_id"]
    __showables__ = ["id", "code","surface","nb_chambres","loyer_mensuel", "site_id"]
    __rel_showables__= ["site"]
    __tablename__ = "appartement"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(50), unique=True, nullable=False)
    surface = Column(Float)
    nb_chambres = Column(Integer)
    loyer_mensuel = Column(DECIMAL(10, 2), nullable=False)

    site_id = Column(UUID(as_uuid=True), ForeignKey("site.id"), nullable=False)
    site = relationship("Site", back_populates="appartements")

    contrats = relationship("ContratDeBail", back_populates="appartement", cascade="all, delete-orphan")

    def getWording(self) :
        
        if self.site :
            return self.site.getWording() + " (" + str(self.code) + " )"
        
        return self.id