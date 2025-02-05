"""cart added to User

Revision ID: da0806395352
Revises: 158add84f791
Create Date: 2020-03-19 21:28:34.143799

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'da0806395352'
down_revision = '158add84f791'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('cart', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'cart')
    # ### end Alembic commands ###
