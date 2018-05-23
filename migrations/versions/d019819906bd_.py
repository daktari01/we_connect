"""empty message

Revision ID: d019819906bd
Revises: cf9e70a6b2c6
Create Date: 2018-05-23 20:02:13.647964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd019819906bd'
down_revision = 'cf9e70a6b2c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('token_user_id', sa.Integer(), nullable=True))
    op.drop_constraint('tokens_users_id_fkey', 'tokens', type_='foreignkey')
    op.create_foreign_key(None, 'tokens', 'users', ['token_user_id'], ['id'])
    op.drop_column('tokens', 'users_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('users_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'tokens', type_='foreignkey')
    op.create_foreign_key('tokens_users_id_fkey', 'tokens', 'users', ['users_id'], ['id'])
    op.drop_column('tokens', 'token_user_id')
    # ### end Alembic commands ###
