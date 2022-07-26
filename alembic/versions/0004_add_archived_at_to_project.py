"""

Revision ID: 8944cc28a60b
Revises: 985db696b9a7
Create Date: 2022-08-10 00:34:14.638866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8944cc28a60b'
down_revision = '985db696b9a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('archived_at', sa.DateTime(), nullable=True))
    op.drop_column('project', 'archived')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('archived', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.drop_column('project', 'archived_at')
    # ### end Alembic commands ###
