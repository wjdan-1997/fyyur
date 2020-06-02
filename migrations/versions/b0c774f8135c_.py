"""empty message

Revision ID: b0c774f8135c
Revises: b5f92c46bfac
Create Date: 2020-05-30 03:45:47.728045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b0c774f8135c'
down_revision = 'b5f92c46bfac'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'website2')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('website2', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    # ### end Alembic commands ###