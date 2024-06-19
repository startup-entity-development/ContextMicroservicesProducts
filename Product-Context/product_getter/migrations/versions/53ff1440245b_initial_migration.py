"""initial migration

Revision ID: 53ff1440245b
Revises: 
Create Date: 2024-03-08 11:42:39.711346

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53ff1440245b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('RetailerLocation',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('retailer_id', sa.Integer(), nullable=False),
    sa.Column('street_addr', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=2), nullable=True),
    sa.Column('zipcode', sa.String(length=5), nullable=True),
    sa.Column('country', sa.String(length=10), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['retailer_id'], ['Retailer.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', 'retailer_id'),
    sa.UniqueConstraint('country'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('state'),
    sa.UniqueConstraint('street_addr'),
    sa.UniqueConstraint('zipcode')
    )
    with op.batch_alter_table('Category', schema=None) as batch_op:
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=True,
               existing_server_default=sa.text('true'))

    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.alter_column('cost',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=10),
               existing_nullable=True)
        batch_op.create_unique_constraint(None, ['id'])

    with op.batch_alter_table('Retailer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_api', sa.String(length=100), nullable=True))
        batch_op.create_unique_constraint(None, ['id'])
        batch_op.create_unique_constraint(None, ['id_api'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Retailer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('id_api')

    with op.batch_alter_table('Product_Retailer', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.alter_column('cost',
               existing_type=sa.Float(precision=10),
               type_=sa.REAL(),
               existing_nullable=True)

    with op.batch_alter_table('Product', schema=None) as batch_op:
        batch_op.alter_column('is_active',
               existing_type=sa.BOOLEAN(),
               nullable=False,
               existing_server_default=sa.text('true'))

    with op.batch_alter_table('Category', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')

    op.drop_table('RetailerLocation')
    # ### end Alembic commands ###
