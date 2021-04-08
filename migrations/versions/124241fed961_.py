"""empty message

Revision ID: 124241fed961
Revises: 88ce4e07559c
Create Date: 2021-04-03 20:16:46.227509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '124241fed961'
down_revision = '88ce4e07559c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('defendants', sa.Column('first_name', sa.String(length=50), nullable=True))
    op.add_column('defendants', sa.Column('last_name', sa.String(length=50), nullable=True))
    op.add_column('defendants', sa.Column('middle_name', sa.String(length=50), nullable=True))
    op.add_column('defendants', sa.Column('suffix', sa.String(length=20), nullable=True))
    op.drop_column('defendants', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('defendants', sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('defendants', 'suffix')
    op.drop_column('defendants', 'middle_name')
    op.drop_column('defendants', 'last_name')
    op.drop_column('defendants', 'first_name')
    # ### end Alembic commands ###