"""empty message

Revision ID: 7ce0170b25d2
Revises: 87dc0133e741
Create Date: 2021-03-16 19:05:06.776995

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '7ce0170b25d2'
down_revision = '87dc0133e741'
branch_labels = None
depends_on = None

now = str(datetime.now())


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('attorneys', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('attorneys', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('courtrooms', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('courtrooms', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('defendants', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('defendants', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('detainer_warrants', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('detainer_warrants', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('districts', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('districts', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('judges', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('judges', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('organizer', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('organizer', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('phone_number_verifications', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('phone_number_verifications', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('plantiffs', sa.Column(
        'created_at', sa.DateTime(), nullable=False, server_default=now))
    op.add_column('plantiffs', sa.Column(
        'updated_at', sa.DateTime(), nullable=False, server_default=now))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('plantiffs', 'updated_at')
    op.drop_column('plantiffs', 'created_at')
    op.drop_column('phone_number_verifications', 'updated_at')
    op.drop_column('phone_number_verifications', 'created_at')
    op.drop_column('organizer', 'updated_at')
    op.drop_column('organizer', 'created_at')
    op.drop_column('judges', 'updated_at')
    op.drop_column('judges', 'created_at')
    op.drop_column('districts', 'updated_at')
    op.drop_column('districts', 'created_at')
    op.drop_column('detainer_warrants', 'updated_at')
    op.drop_column('detainer_warrants', 'created_at')
    op.drop_column('defendants', 'updated_at')
    op.drop_column('defendants', 'created_at')
    op.drop_column('courtrooms', 'updated_at')
    op.drop_column('courtrooms', 'created_at')
    op.drop_column('attorneys', 'updated_at')
    op.drop_column('attorneys', 'created_at')
    # ### end Alembic commands ###
