"""Unite Clubs and SportActivities

Revision ID: da9012c31020
Revises: 774323c7a621
Create Date: 2020-04-18 16:52:58.103795

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'da9012c31020'
down_revision = '774323c7a621'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('clubs')
    op.add_column('sport_activities', sa.Column('chat_link', sa.String(length=256), nullable=True))
    op.add_column('sport_activities', sa.Column('is_club', sa.Boolean(), nullable=False, server_default='False'))
    op.add_column('sport_activities', sa.Column('leader', sa.String(length=128), nullable=False))
    op.create_foreign_key(None, 'sport_activities', 'users', ['leader'], ['email'])
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=False, server_default='False'))
    op.drop_column('users', 'roles')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('roles', postgresql.ARRAY(sa.VARCHAR(length=32)), autoincrement=False, nullable=False))
    op.drop_column('users', 'is_admin')
    op.drop_constraint(None, 'sport_activities', type_='foreignkey')
    op.drop_column('sport_activities', 'leader')
    op.drop_column('sport_activities', 'is_club')
    op.drop_column('sport_activities', 'chat_link')
    op.create_table('clubs',
    sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('leader', sa.VARCHAR(length=128), autoincrement=False, nullable=False),
    sa.Column('link', sa.VARCHAR(length=256), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['id'], ['sport_activities.id'], name='clubs_id_fkey'),
    sa.ForeignKeyConstraint(['leader'], ['users.email'], name='clubs_leader_fkey'),
    sa.PrimaryKeyConstraint('id', name='clubs_pkey')
    )
    # ### end Alembic commands ###
