from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Enum as PgEnum,
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey, text
)
from sqlalchemy.dialects.postgresql import UUID, ExcludeConstraint
from enums.ModePayment import ModePayment
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)
from sqlalchemy.dialects.postgresql import TSRANGE
from sqlalchemy.schema import CheckConstraint
from sqlalchemy import func
from sqlalchemy import and_


class ContratDeBail(db.Model):
    __fillables__ = ["date_debut","date_fin","montant_loyer","duree_mois_garantie","statut", "appartement_id", "locateur_id"]
    __showables__ = ["id", "date_debut","date_fin","montant_loyer","duree_mois_garantie","statut", "appartement_id", "locateur_id"]
    __rel_showables__= ["appartement", "locateur_utilisateur"]
    __tablename__ = "contrat_de_bail"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=True)
    montant_loyer = Column(DECIMAL(10, 2), nullable=False)
    status = Column(PgEnum(ModePayment, name="modepayment", create_type=True), default=ModePayment.MOIS)
    duree_mois_garantie = Column(Integer)

    appartement_id = Column(UUID(as_uuid=True), ForeignKey("appartement.id"), nullable=False)
    locateur_id = Column(Integer, ForeignKey("locateur_utilisateur.id"), nullable=False)

    appartement = relationship("Appartement", back_populates="contrats")
    locateur_utilisateur = relationship("LocateurUtilisateur", back_populates="contrats")
    paiements = relationship("Paiement", back_populates="contrat", cascade="all, delete-orphan")

    def getWording(self) :
        
        if self.appartement :
            return self.appartement.getWording() + " (" + str(self.locateur_utilisateur.getWording()) + " )"
        
        return self.id
    
    
    __table_args__ = (

        # Empêche tout chevauchement pour le même appartement
        ExcludeConstraint(
            (func.tsrange(
                func.coalesce(date_debut, func.now()),
                func.coalesce(date_fin, func.now() + text("'100 years'::interval"))
            ), '&&'),
            (appartement_id, '='),
            name="exclude_contrat_overlap",
            using="gist"
        ),
    )