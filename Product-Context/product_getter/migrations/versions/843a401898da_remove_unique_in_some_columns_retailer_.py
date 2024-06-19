"""remove unique in some columns retailer location

Revision ID: 843a401898da
Revises: 53ff1440245b
Create Date: 2024-03-08 12:46:45.273338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '843a401898da'
down_revision = '53ff1440245b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10),
               existing_nullable=True)

    with op.batch_alter_table('RetailerLocation', schema=None) as batch_op:
        batch_op.drop_constraint('RetailerLocation_country_key', type_='unique')
        batch_op.drop_constraint('RetailerLocation_state_key', type_='unique')
        batch_op.drop_constraint('RetailerLocation_street_addr_key', type_='unique')
        batch_op.drop_constraint('RetailerLocation_zipcode_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('RetailerLocation', schema=None) as batch_op:
        batch_op.create_unique_constraint('RetailerLocation_zipcode_key', ['zipcode'])
        batch_op.create_unique_constraint('RetailerLocation_street_addr_key', ['street_addr'])
        batch_op.create_unique_constraint('RetailerLocation_state_key', ['state'])
        batch_op.create_unique_constraint('RetailerLocation_country_key', ['country'])

    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.Float(precision=10),
               type_=sa.REAL(),
               existing_nullable=True)

    # ### end Alembic commands ###
