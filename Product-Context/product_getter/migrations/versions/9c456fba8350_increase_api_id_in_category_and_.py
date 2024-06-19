"""increase api_id in category and subcategory to 1000

Revision ID: 9c456fba8350
Revises: 0a881891cba4
Create Date: 2024-03-08 16:20:57.327898

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c456fba8350'
down_revision = '0a881891cba4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Category', schema=None) as batch_op:
        batch_op.alter_column('api_id',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1000),
               existing_nullable=False)

    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10),
               existing_nullable=True)

    with op.batch_alter_table('SubCategory', schema=None) as batch_op:
        batch_op.alter_column('api_id',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1000),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('SubCategory', schema=None) as batch_op:
        batch_op.alter_column('api_id',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.Float(precision=10),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('Category', schema=None) as batch_op:
        batch_op.alter_column('api_id',
               existing_type=sa.String(length=1000),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)

    # ### end Alembic commands ###
