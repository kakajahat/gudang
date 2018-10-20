"""empty message

Revision ID: 6704c6bc1e48
Revises: 8090c6127121
Create Date: 2018-10-17 03:22:47.696930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6704c6bc1e48'
down_revision = '8090c6127121'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reqbarang', sa.Column('keterangan', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reqbarang', 'keterangan')
    # ### end Alembic commands ###
