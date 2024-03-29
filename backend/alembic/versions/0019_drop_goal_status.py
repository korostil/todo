"""

Revision ID: 6b2105afa271
Revises: 7865f7a69cd3
Create Date: 2023-03-29 22:24:29.803976

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '6b2105afa271'
down_revision = '7865f7a69cd3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('achieved_at', sa.DateTime(), nullable=True))
    op.drop_column('goal', 'status')
    op.drop_column('goal', 'archived_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goal', sa.Column('archived_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('goal', sa.Column('status', sa.INTEGER(), server_default=sa.text('1'), autoincrement=False, nullable=False))
    op.drop_column('goal', 'achieved_at')
    # ### end Alembic commands ###
