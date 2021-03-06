"""empty message

Revision ID: 9f266a1e3be0
Revises: b0c774f8135c
Create Date: 2020-06-01 01:13:27.316487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f266a1e3be0'
down_revision = 'b0c774f8135c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
