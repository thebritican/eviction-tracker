"""empty message

Revision ID: 28df5be25152
Revises: 5575d76d1738
Create Date: 2021-04-04 09:45:58.836695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28df5be25152'
down_revision = '5575d76d1738'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('detainer_warrants_plantiff_id_fkey', 'detainer_warrants', type_='foreignkey')
    op.create_foreign_key(None, 'detainer_warrants', 'plantiffs', ['plantiff_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'detainer_warrants', type_='foreignkey')
    op.create_foreign_key('detainer_warrants_plantiff_id_fkey', 'detainer_warrants', 'plantiffs', ['plantiff_id'], ['id'])
    # ### end Alembic commands ###
