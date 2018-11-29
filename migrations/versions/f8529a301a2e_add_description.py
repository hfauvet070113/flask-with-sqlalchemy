"""add description

Revision ID: f8529a301a2e
Revises: 3e0c9e4caec8
Create Date: 2018-11-29 10:43:44.891524

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8529a301a2e'
down_revision = '3e0c9e4caec8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('description', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'description')
    # ### end Alembic commands ###