"""empty message

Revision ID: c157d9ddb430
Revises: d8eb98ede669
Create Date: 2021-03-22 12:01:52.771838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c157d9ddb430'
down_revision = 'd8eb98ede669'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('detainer_warrants', 'amount_claimed',
                    existing_type=sa.VARCHAR(length=30),
                    type_=sa.Numeric(scale=2),
                    existing_nullable=True,
                    postgresql_using="amount_claimed::numeric")

    op.alter_column('detainer_warrants', 'court_date',
                    existing_type=sa.VARCHAR(length=255),
                    type_=sa.Date(),
                    existing_nullable=True,
                    postgresql_using="court_date::date")
    op.alter_column('detainer_warrants', 'file_date',
                    existing_type=sa.VARCHAR(length=255),
                    type_=sa.Date(),
                    existing_nullable=False,
                    postgresql_using="court_date::date")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('detainer_warrants', 'file_date',
                    existing_type=sa.Date(),
                    type_=sa.VARCHAR(length=255),
                    existing_nullable=False)
    op.alter_column('detainer_warrants', 'court_date',
                    existing_type=sa.Date(),
                    type_=sa.VARCHAR(length=255),
                    existing_nullable=True)
    op.alter_column('detainer_warrants', 'amount_claimed',
                    existing_type=sa.Numeric(scale=2),
                    type_=sa.VARCHAR(length=30),
                    existing_nullable=True)
    # ### end Alembic commands ###
