"""Initial migration

Revision ID: a566710c57c8
Revises: 
Create Date: 2024-12-30 01:29:48.873143

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a566710c57c8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parkings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('capacity', sa.Integer(), nullable=False),
    sa.Column('available_slots', sa.Integer(), nullable=False),
    sa.Column('price_per_hour', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('port_facilities',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('operational_hours', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=100), nullable=False),
    sa.Column('arrival_time', sa.DateTime(), nullable=False),
    sa.Column('departure_time', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('bookings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.Integer(), nullable=False),
    sa.Column('booking_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['service_id'], ['services.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedbacks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('schedules',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ship_id', sa.Integer(), nullable=False),
    sa.Column('departure_time', sa.DateTime(), nullable=False),
    sa.Column('arrival_time', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['ship_id'], ['ships.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedules')
    op.drop_table('feedbacks')
    op.drop_table('bookings')
    op.drop_table('users')
    op.drop_table('ships')
    op.drop_table('services')
    op.drop_table('port_facilities')
    op.drop_table('parkings')
    # ### end Alembic commands ###
