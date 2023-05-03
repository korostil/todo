"""

Revision ID: 7865f7a69cd3
Revises: 6648e385195c
Create Date: 2023-02-19 19:40:44.377956

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7865f7a69cd3'
down_revision = '6648e385195c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('due_date', sa.Date(), nullable=True))
    op.add_column('task', sa.Column('due_time', sa.Time(), nullable=True))
    op.drop_column('task', 'due')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('due', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('task', 'due_time')
    op.drop_column('task', 'due_date')
    # ### end Alembic commands ###