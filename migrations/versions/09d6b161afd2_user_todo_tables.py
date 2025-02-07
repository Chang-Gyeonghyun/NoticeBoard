"""user_todo_tables

Revision ID: 09d6b161afd2
Revises: 
Create Date: 2024-08-23 23:00:23.465102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09d6b161afd2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userID', sa.String(length=255), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('userName', sa.String(length=255), nullable=True),
    sa.Column('phone', sa.String(length=255), nullable=True),
    sa.Column('birthday', sa.String(length=255), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_address'), 'user', ['address'], unique=False)
    op.create_index(op.f('ix_user_birthday'), 'user', ['birthday'], unique=False)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=False)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_password'), 'user', ['password'], unique=False)
    op.create_index(op.f('ix_user_phone'), 'user', ['phone'], unique=False)
    op.create_index(op.f('ix_user_userID'), 'user', ['userID'], unique=True)
    op.create_index(op.f('ix_user_userName'), 'user', ['userName'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_userName'), table_name='user')
    op.drop_index(op.f('ix_user_userID'), table_name='user')
    op.drop_index(op.f('ix_user_phone'), table_name='user')
    op.drop_index(op.f('ix_user_password'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_birthday'), table_name='user')
    op.drop_index(op.f('ix_user_address'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
