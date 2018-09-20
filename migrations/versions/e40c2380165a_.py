"""empty message

Revision ID: e40c2380165a
Revises: 
Create Date: 2018-09-15 16:10:30.498337

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e40c2380165a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('peranan',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=60), nullable=True),
    sa.Column('level', sa.Integer(), nullable=True),
    sa.Column('deskripsi', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('nama')
    )
    op.create_table('pengguna',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=60), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('uname', sa.String(length=60), nullable=True),
    sa.Column('passwd_hash', sa.String(length=128), nullable=True),
    sa.Column('peran_id', sa.Integer(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['peran_id'], ['peranan.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pengguna_email'), 'pengguna', ['email'], unique=True)
    op.create_index(op.f('ix_pengguna_nama'), 'pengguna', ['nama'], unique=False)
    op.create_index(op.f('ix_pengguna_uname'), 'pengguna', ['uname'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pengguna_uname'), table_name='pengguna')
    op.drop_index(op.f('ix_pengguna_nama'), table_name='pengguna')
    op.drop_index(op.f('ix_pengguna_email'), table_name='pengguna')
    op.drop_table('pengguna')
    op.drop_table('peranan')
    # ### end Alembic commands ###