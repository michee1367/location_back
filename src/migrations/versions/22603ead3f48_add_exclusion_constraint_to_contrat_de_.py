"""Add exclusion constraint to contrat_de_bail

Revision ID: 22603ead3f48
Revises: 410b50c4c63a
Create Date: 2025-12-11 17:03:08.266343

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22603ead3f48'
down_revision = '410b50c4c63a'
branch_labels = None
depends_on = None


def upgrade():
    # Activer l'extension PostgreSQL si nécessaire
    op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")

    # Ajouter la contrainte d'exclusion
    op.execute("""
        ALTER TABLE contrat_de_bail
        ADD CONSTRAINT exclude_contrat_overlap
        EXCLUDE USING gist (
            daterange(date_debut, COALESCE(date_fin, '9999-12-31'::date)) WITH &&,
            appartement_id WITH =
        );
    """)

    pass


def downgrade():
    op.execute("ALTER TABLE contrat_de_bail DROP CONSTRAINT IF EXISTS exclude_contrat_overlap;")
    #pass
