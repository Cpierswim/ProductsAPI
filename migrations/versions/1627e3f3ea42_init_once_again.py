"""Init once again

Revision ID: 1627e3f3ea42
Revises: 
Create Date: 2023-03-10 16:30:11.736734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1627e3f3ea42'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('inventory_quantity', sa.Integer(), nullable=False),
    sa.Column('img_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    # ### end Alembic commands ###