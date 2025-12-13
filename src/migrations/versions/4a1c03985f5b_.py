"""empty message

Revision ID: 4a1c03985f5b
Revises: fe559f3bed54
Create Date: 2025-11-13 10:07:45.360054

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a1c03985f5b'
down_revision = 'fe559f3bed54'
branch_labels = None
depends_on = None

def upgrade():
    # création du type ENUM avant utilisation
    modepayment_enum = sa.Enum('MOIS', 'JOUR', 'TRIMESTRE', 'SEMESTRE', 'ANNEE', name='modepayment')
    modepayment_enum.create(op.get_bind())

    with op.batch_alter_table('contrat_de_bail', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', modepayment_enum, nullable=True))

def downgrade():
    with op.batch_alter_table('contrat_de_bail', schema=None) as batch_op:
        batch_op.drop_column('status')

    # suppression du type ENUM après suppression de la colonne
    modepayment_enum = sa.Enum(name='modepayment')
    modepayment_enum.drop(op.get_bind())

