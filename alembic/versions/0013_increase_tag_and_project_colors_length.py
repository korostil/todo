"""

Revision ID: c9bd8576a895
Revises: b076adf56c87
Create Date: 2022-11-23 21:56:42.802181

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9bd8576a895'
down_revision = 'b076adf56c87'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'color',
                    existing_type=sa.String(length=6),
                    type_=sa.String(length=7),
                    existing_nullable=True)
    op.alter_column('tag', 'color',
                    existing_type=sa.String(length=6),
                    type_=sa.String(length=7),
                    existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('project', 'color',
                    existing_type=sa.String(length=7),
                    type_=sa.String(length=6),
                    existing_nullable=True)
    op.alter_column('tag', 'color',
                    existing_type=sa.String(length=7),
                    type_=sa.String(length=6),
                    existing_nullable=True)
    # ### end Alembic commands ###