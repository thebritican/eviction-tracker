"""empty message

Revision ID: 905a870dfffb
Revises: 28df5be25152
Create Date: 2021-04-04 09:49:11.609986

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '905a870dfffb'
down_revision = '28df5be25152'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plaintiffs',
                    sa.Column('created_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=False),
                    sa.Column('attorney_id', sa.Integer(), nullable=True),
                    sa.Column('district_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(
                        ['attorney_id'], ['attorneys.id'], ),
                    sa.ForeignKeyConstraint(
                        ['district_id'], ['districts.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.drop_constraint('detainer_warrants_plantiff_id_fkey',
                       'detainer_warrants', type_='foreignkey')
    op.drop_table('plantiffs')
    op.add_column('detainer_warrants', sa.Column(
        'plaintiff_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'detainer_warrants', 'plaintiffs', [
                          'plaintiff_id'], ['id'], ondelete='CASCADE')
    op.drop_column('detainer_warrants', 'plantiff_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('detainer_warrants', sa.Column(
        'plantiff_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'detainer_warrants', type_='foreignkey')
    op.create_foreign_key('detainer_warrants_plantiff_id_fkey', 'detainer_warrants', 'plantiffs', [
                          'plantiff_id'], ['id'], ondelete='CASCADE')
    op.drop_column('detainer_warrants', 'plaintiff_id')
    op.create_table('plantiffs',
                    sa.Column('id', sa.INTEGER(),
                              autoincrement=True, nullable=False),
                    sa.Column('name', sa.VARCHAR(length=255),
                              autoincrement=False, nullable=False),
                    sa.Column('attorney_id', sa.INTEGER(),
                              autoincrement=False, nullable=True),
                    sa.Column('district_id', sa.INTEGER(),
                              autoincrement=False, nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        "'2021-03-22 15:08:31.871232'::timestamp without time zone"), autoincrement=False, nullable=False),
                    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text(
                        "'2021-03-22 15:08:31.871232'::timestamp without time zone"), autoincrement=False, nullable=False),
                    sa.ForeignKeyConstraint(
                        ['attorney_id'], ['attorneys.id'], name='plantiffs_attorney_id_fkey'),
                    sa.ForeignKeyConstraint(
                        ['district_id'], ['districts.id'], name='plantiffs_district_id_fkey'),
                    sa.PrimaryKeyConstraint('id', name='plantiffs_pkey')
                    )
    op.drop_table('plaintiffs')
    # ### end Alembic commands ###
