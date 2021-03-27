"""empty message

Revision ID: 2e00c280b37a
Revises: 6c1ce20ad624
Create Date: 2021-03-26 15:13:29.058339

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e00c280b37a'
down_revision = '6c1ce20ad624'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'phone_number_verifications', ['phone_number'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'phone_number_verifications', type_='unique')
    # ### end Alembic commands ###