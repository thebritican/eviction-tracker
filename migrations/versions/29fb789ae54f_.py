"""empty message

Revision ID: 29fb789ae54f
Revises: a5ced3885cae
Create Date: 2021-04-21 14:57:26.380776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29fb789ae54f'
down_revision = 'a5ced3885cae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detainer_warrants', sa.Column('plaintiff_attorney_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'detainer_warrants', 'attorneys', ['plaintiff_attorney_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('plaintiffs_attorney_id_fkey', 'plaintiffs', type_='foreignkey')
    op.drop_column('plaintiffs', 'attorney_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('plaintiffs', sa.Column('attorney_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('plaintiffs_attorney_id_fkey', 'plaintiffs', 'attorneys', ['attorney_id'], ['id'])
    op.drop_constraint(None, 'detainer_warrants', type_='foreignkey')
    op.drop_column('detainer_warrants', 'plaintiff_attorney_id')
    # ### end Alembic commands ###
