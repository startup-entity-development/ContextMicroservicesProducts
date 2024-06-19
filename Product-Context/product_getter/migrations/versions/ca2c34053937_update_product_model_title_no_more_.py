"""update product model title no more unique

Revision ID: ca2c34053937
Revises: 47f9f5159370
Create Date: 2024-03-13 05:00:02.787838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca2c34053937'
down_revision = '47f9f5159370'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.drop_constraint('Product_title_key', type_='unique')

    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.Float(precision=10),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.create_unique_constraint('Product_title_key', ['title'])

    # ### end Alembic commands ###