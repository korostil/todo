"""

Revision ID: afb9a678b423
Revises: 09508d06a36f
Create Date: 2023-01-24 23:04:36.587644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afb9a678b423'
down_revision = '09508d06a36f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goal', 'week')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('week', sa.INTEGER(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
