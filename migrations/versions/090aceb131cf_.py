"""empty message

Revision ID: 090aceb131cf
Revises: 812c93346335
Create Date: 2020-05-29 18:45:19.326589

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '090aceb131cf'
down_revision = '812c93346335'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'city1')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('city1', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
