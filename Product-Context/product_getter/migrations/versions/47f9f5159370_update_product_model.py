"""update product model 

Revision ID: 47f9f5159370
Revises: b2390d328808
Create Date: 2024-03-13 04:59:23.449180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47f9f5159370'
down_revision = 'b2390d328808'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Category', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.alter_column('api_id',
               existing_type=sa.VARCHAR(length=250),
               type_=sa.String(length=300),
               existing_nullable=False)

    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('cost',
               existing_type=sa.Float(precision=10),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.alter_column('api_id',
               existing_type=sa.String(length=300),
               type_=sa.VARCHAR(length=250),
               existing_nullable=False)

    with op.batch_alter_table('Category', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    # ### end Alembic commands ###