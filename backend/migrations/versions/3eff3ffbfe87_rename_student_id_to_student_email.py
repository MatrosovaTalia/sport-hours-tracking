"""Rename student_id to student_email

Revision ID: 3eff3ffbfe87
Revises: c862ba1d29ef
Create Date: 2020-04-10 11:50:48.156630

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eff3ffbfe87'
down_revision = 'c862ba1d29ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('activity_assignment', sa.Column('student_email', sa.String(length=128), nullable=False))
    op.drop_constraint('activity_assignment_student_id_fkey', 'activity_assignment', type_='foreignkey')
    op.create_foreign_key(None, 'activity_assignment', 'users', ['student_email'], ['email'], ondelete='CASCADE')
    op.drop_column('activity_assignment', 'student_id')
    op.add_column('sport_hours_records', sa.Column('student_email', sa.String(length=128), nullable=False))
    op.drop_constraint('sport_hours_records_student_id_activity_id_date_key', 'sport_hours_records', type_='unique')
    op.create_unique_constraint(None, 'sport_hours_records', ['student_email', 'activity_id', 'date'])
    op.drop_constraint('sport_hours_records_student_id_fkey', 'sport_hours_records', type_='foreignkey')
    op.create_foreign_key(None, 'sport_hours_records', 'users', ['student_email'], ['email'])
    op.drop_column('sport_hours_records', 'student_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sport_hours_records', sa.Column('student_id', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'sport_hours_records', type_='foreignkey')
    op.create_foreign_key('sport_hours_records_student_id_fkey', 'sport_hours_records', 'users', ['student_id'], ['email'])
    op.drop_constraint(None, 'sport_hours_records', type_='unique')
    op.create_unique_constraint('sport_hours_records_student_id_activity_id_date_key', 'sport_hours_records', ['student_id', 'activity_id', 'date'])
    op.drop_column('sport_hours_records', 'student_email')
    op.add_column('activity_assignment', sa.Column('student_id', sa.VARCHAR(length=128), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'activity_assignment', type_='foreignkey')
    op.create_foreign_key('activity_assignment_student_id_fkey', 'activity_assignment', 'users', ['student_id'], ['email'], ondelete='CASCADE')
    op.drop_column('activity_assignment', 'student_email')
    # ### end Alembic commands ###
