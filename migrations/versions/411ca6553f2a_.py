"""empty message

Revision ID: 411ca6553f2a
Revises: 6a172a3eee40
Create Date: 2020-06-01 21:04:53.483126

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '411ca6553f2a'
down_revision = '6a172a3eee40'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('seeking_description', sa.String(length=500)))
    op.add_column('Artist', sa.Column('seeking_talent', sa.Boolean()))
    op.alter_column('Artist', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=30)),
               nullable=False)
    op.add_column('Venue', sa.Column('seeking_description', sa.String(length=500)))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean()))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'seeking_description')
    op.alter_column('Artist', 'genres',
               existing_type=postgresql.ARRAY(sa.VARCHAR(length=30)),
               nullable=True)
    op.drop_column('Artist', 'seeking_talent')
    op.drop_column('Artist', 'seeking_description')
    # ### end Alembic commands ###