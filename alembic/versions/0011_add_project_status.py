"""

Revision ID: f17800959dac
Revises: 61fde8a256eb
Create Date: 2022-08-22 22:08:58.687289

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f17800959dac'
down_revision = '61fde8a256eb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('status', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'status')
    # ### end Alembic commands ###
