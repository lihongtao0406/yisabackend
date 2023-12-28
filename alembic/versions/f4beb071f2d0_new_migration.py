"""New Migration

Revision ID: f4beb071f2d0
Revises: 
Create Date: 2023-12-15 11:29:38.289993

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f4beb071f2d0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_client_id'), 'client', ['id'], unique=False)
    op.create_table('employee',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('invoice',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client', sa.String(), nullable=True),
    sa.Column('employee', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('hours', sa.Float(), nullable=True),
    sa.Column('travel_time', sa.Float(), nullable=True),
    sa.Column('travel_km', sa.Integer(), nullable=True),
    sa.Column('invoice_num', sa.String(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payrun',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('employee', sa.String(), nullable=True),
    sa.Column('total_hours', sa.Float(), nullable=True),
    sa.Column('total_km', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shiftreport',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('client_name', sa.String(), nullable=True),
    sa.Column('date', sa.String(), nullable=True),
    sa.Column('support_provider', sa.String(), nullable=True),
    sa.Column('participants_welfare', sa.String(), nullable=True),
    sa.Column('activity', sa.String(), nullable=True),
    sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shiftreport')
    op.drop_table('payrun')
    op.drop_table('invoice')
    op.drop_table('employee')
    op.drop_index(op.f('ix_client_id'), table_name='client')
    op.drop_table('client')
    # ### end Alembic commands ###
