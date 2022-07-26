"""

Revision ID: 61fde8a256eb
Revises: 5fedf774492b
Create Date: 2022-08-18 21:24:55.496626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '61fde8a256eb'
down_revision = '5fedf774492b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('goal_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'project', 'goal', ['goal_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'project', type_='foreignkey')
    op.drop_column('project', 'goal_id')
    # ### end Alembic commands ###
