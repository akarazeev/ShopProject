"""Added commentary table

Revision ID: 93a2fda1d597
Revises: 86a937d98c41
Create Date: 2020-05-03 12:55:39.084530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '93a2fda1d597'
down_revision = '86a937d98c41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commentary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('creation_date', sa.String(length=15), nullable=True),
    sa.Column('text', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('commentary')
    # ### end Alembic commands ###
