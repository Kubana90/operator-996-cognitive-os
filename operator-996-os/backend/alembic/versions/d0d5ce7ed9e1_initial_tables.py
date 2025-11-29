"""initial_tables

Revision ID: d0d5ce7ed9e1
Revises: 
Create Date: 2025-11-29 13:27:19.198480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'd0d5ce7ed9e1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if using PostgreSQL for native types
    bind = op.get_bind()
    is_postgresql = bind.dialect.name == 'postgresql'
    
    if is_postgresql:
        from sqlalchemy.dialects import postgresql
        uuid_type = postgresql.UUID(as_uuid=True)
        json_type = postgresql.JSONB()
    else:
        uuid_type = sa.String(36)
        json_type = sa.JSON()
    
    op.create_table('profiles',
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('cognitive_data', json_type, nullable=True),
        sa.Column('behavioral_data', json_type, nullable=True),
        sa.Column('communication_data', json_type, nullable=True),
        sa.Column('shadow_data', json_type, nullable=True),
        sa.Column('domains_data', json_type, nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('anomalies',
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('profile_id', uuid_type, nullable=False),
        sa.Column('anomaly_type', sa.String(length=100), nullable=False),
        sa.Column('severity', sa.Float(), nullable=False),
        sa.Column('explanation', sa.Text(), nullable=True),
        sa.Column('recommendation', sa.Text(), nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('behavioral_events',
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('profile_id', uuid_type, nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.Column('decision_logic', sa.Text(), nullable=True),
        sa.Column('outcome', sa.Text(), nullable=True),
        sa.Column('tags', json_type, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patterns',
        sa.Column('id', uuid_type, nullable=False),
        sa.Column('profile_id', uuid_type, nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('characteristics', json_type, nullable=True),
        sa.Column('supporting_events', json_type, nullable=True),
        sa.Column('detected_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('patterns')
    op.drop_table('behavioral_events')
    op.drop_table('anomalies')
    op.drop_table('profiles')
