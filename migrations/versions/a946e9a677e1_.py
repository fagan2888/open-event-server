"""empty message

Revision ID: a946e9a677e1
Revises: abda2e67f7c3
Create Date: 2016-06-24 12:15:14.410470

"""

# revision identifiers, used by Alembic.
revision = 'a946e9a677e1'
down_revision = 'abda2e67f7c3'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('next_event', sa.Binary(), nullable=True),
    sa.Column('new_paper', sa.Binary(), nullable=True),
    sa.Column('session_accept_reject', sa.Binary(), nullable=True),
    sa.Column('session_schedule', sa.Binary(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_notification')
    ### end Alembic commands ###
