import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from flask import current_app

def generate_facture_pdf(paiement):
    """
    Génère une facture PDF pour un paiement et retourne le chemin du fichier créé.
    """
    # Dossier de stockage
    storage_path = os.path.join(current_app.root_path, "storage", "factures")
    os.makedirs(storage_path, exist_ok=True)

    # Nom du fichier PDF
    filename = f"facture_{paiement.id}.pdf"
    filepath = os.path.join(storage_path, filename)

    # Création du PDF
    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4

    # Titre
    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, height - 50, "FACTURE DE PAIEMENT LOYER")

    # Infos du paiement
    c.setFont("Helvetica", 12)
    y = height - 120

    c.drawString(50, y, f"Référence paiement : {paiement.reference}")
    y -= 20
    c.drawString(50, y, f"Date paiement : {paiement.date_paiement}")
    y -= 20
    c.drawString(50, y, f"Montant : {paiement.montant} USD")
    y -= 20

    # Contrat
    c.drawString(50, y, f"Contrat : {paiement.contrat.id}")
    y -= 20

    # Moyen de paiement
    c.drawString(50, y, f"Moyen de paiement : {paiement.moyen_de_paiement.type}")
    y -= 40
    
    c.drawString(50, y, "Nom et Signature du percepteurs")
    y -= 90
    c.drawString(50, y, "Nom et signature du locateur")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 40, "Document généré automatiquement par votre système.")
    y -= 40

    c.save()

    return filepath
