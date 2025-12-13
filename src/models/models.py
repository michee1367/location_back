from datetime import datetime
from uuid import uuid4
from sqlalchemy import (
    Column, String, Date, DateTime, Float, Integer, DECIMAL, ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from models import db  # db = SQLAlchemy(app)


# ==============================
# Utilisateur (classe de base)
# ==============================

class Utilisateur(db.Model):
    __tablename__ = "utilisateur"
    id = Column(Integer, primary_key=True, default=uuid4)
    nom = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    telephone = Column(String(30))
    role = Column(String(50), nullable=False)
    date_creation = Column(DateTime, default=datetime.utcnow)

    type = Column(String(50))  # Discriminateur pour l’héritage polymorphique

    __mapper_args__ = {
        'polymorphic_identity': 'utilisateur',
        'polymorphic_on': type
    }

    # Relations communes
    organisations = relationship("Organisation", back_populates="proprietaire")


# ==============================
# Administrateur d'organisation
# ==============================

class AdministrateurOrganisation(Utilisateur):
    __tablename__ = "administrateur_organisation"

    id = Column(Integer, ForeignKey("utilisateur.id"), primary_key=True)
    date_ajout = Column(DateTime, default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_identity': 'administrateur_organisation'
    }

    # Relation spécifique
    organisations_admin = relationship("Organisation", back_populates="administrateur")


# ==============================
# Gestionnaire de site
# ==============================

class GestionnaireSite(Utilisateur):
    __tablename__ = "gestionnaire_site"

    id = Column(Integer, ForeignKey("utilisateur.id"), primary_key=True)
    date_affectation = Column(DateTime, default=datetime.utcnow)
    site_id = Column(Integer, ForeignKey("site.id"))

    site = relationship("Site", back_populates="gestionnaires")

    __mapper_args__ = {
        'polymorphic_identity': 'gestionnaire_site'
    }


# ==============================
# Locateur (hérite de Utilisateur)
# ==============================

class LocateurUtilisateur(Utilisateur):
    __tablename__ = "locateur_utilisateur"

    id = Column(Integer, ForeignKey("utilisateur.id"), primary_key=True)
    adresse = Column(String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'locateur'
    }

    contrats = relationship("ContratDeBail", back_populates="locateur_utilisateur")


# ==============================
# Organisation
# ==============================

class Organisation(db.Model):
    __tablename__ = "organisation"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nom = Column(String(100), nullable=False)
    adresse = Column(String(255))
    email = Column(String(120))
    telephone = Column(String(30))

    proprietaire_id = Column(UUID(as_uuid=True), ForeignKey("utilisateur.id"))
    administrateur_id = Column(UUID(as_uuid=True), ForeignKey("administrateur_organisation.id"))

    proprietaire = relationship("Utilisateur", back_populates="organisations")
    administrateur = relationship("AdministrateurOrganisation", back_populates="organisations_admin")

    sites = relationship("Site", back_populates="organisation", cascade="all, delete-orphan")


# ==============================
# Site
# ==============================

class Site(db.Model):
    __tablename__ = "site"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    nom = Column(String(100), nullable=False)
    adresse = Column(String(255))
    ville = Column(String(100))

    organisation_id = Column(UUID(as_uuid=True), ForeignKey("organisation.id"), nullable=False)
    organisation = relationship("Organisation", back_populates="sites")

    appartements = relationship("Appartement", back_populates="site", cascade="all, delete-orphan")
    gestionnaires = relationship("GestionnaireSite", back_populates="site")


# ==============================
# Appartement
# ==============================

class Appartement(db.Model):
    __tablename__ = "appartement"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(String(50), unique=True, nullable=False)
    surface = Column(Float)
    nb_chambres = Column(Integer)
    loyer_mensuel = Column(DECIMAL(10, 2), nullable=False)
    statut = Column(String(50), default="libre")

    site_id = Column(UUID(as_uuid=True), ForeignKey("site.id"), nullable=False)
    site = relationship("Site", back_populates="appartements")

    contrats = relationship("ContratDeBail", back_populates="appartement", cascade="all, delete-orphan")


# ==============================
# Contrat de Bail
# ==============================

class ContratDeBail(db.Model):
    __tablename__ = "contrat_de_bail"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    montant_loyer = Column(DECIMAL(10, 2), nullable=False)
    duree_mois = Column(Integer)
    statut = Column(String(50), default="actif")

    appartement_id = Column(UUID(as_uuid=True), ForeignKey("appartement.id"), nullable=False)
    locateur_id = Column(UUID(as_uuid=True), ForeignKey("locateur_utilisateur.id"), nullable=False)

    appartement = relationship("Appartement", back_populates="contrats")
    locateur_utilisateur = relationship("LocateurUtilisateur", back_populates="contrats")
    paiements = relationship("Paiement", back_populates="contrat", cascade="all, delete-orphan")


# ==============================
# Moyen de Paiement
# ==============================

class MoyenDePaiement(db.Model):
    __tablename__ = "moyen_de_paiement"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    type = Column(String(50), nullable=False)  # Mobile, Banque, Cash
    details = Column(String(255))

    paiements = relationship("Paiement", back_populates="moyen_de_paiement")


# ==============================
# Paiement
# ==============================

class Paiement(db.Model):
    __tablename__ = "paiement"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    date_paiement = Column(Date, default=datetime.utcnow)
    montant = Column(DECIMAL(10, 2), nullable=False)
    reference = Column(String(100))

    contrat_id = Column(UUID(as_uuid=True), ForeignKey("contrat_de_bail.id"), nullable=False)
    moyen_id = Column(UUID(as_uuid=True), ForeignKey("moyen_de_paiement.id"), nullable=False)

    contrat = relationship("ContratDeBail", back_populates="paiements")
    moyen_de_paiement = relationship("MoyenDePaiement", back_populates="paiements")
