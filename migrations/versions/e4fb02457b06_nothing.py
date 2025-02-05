"""nothing

Revision ID: e4fb02457b06
Revises: aac60d257ebf
Create Date: 2020-04-18 17:10:56.081775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4fb02457b06'
down_revision = 'aac60d257ebf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='user')
    op.drop_index('ix_user_token', table_name='user')
    op.drop_index('ix_user_username', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=64), nullable=True),
    sa.Column('email', sa.VARCHAR(length=120), nullable=True),
    sa.Column('birth_date', sa.DATETIME(), nullable=True),
    sa.Column('register_date', sa.DATETIME(), nullable=True),
    sa.Column('password_hash', sa.VARCHAR(length=128), nullable=True),
    sa.Column('phone_number', sa.VARCHAR(length=15), nullable=True),
    sa.Column('token', sa.VARCHAR(length=32), nullable=True),
    sa.Column('token_expiration', sa.DATETIME(), nullable=True),
    sa.Column('cart', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_username', 'user', ['username'], unique=1)
    op.create_index('ix_user_token', 'user', ['token'], unique=1)
    op.create_index('ix_user_email', 'user', ['email'], unique=1)
    # ### end Alembic commands ###
