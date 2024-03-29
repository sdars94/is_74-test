"""empty message

Revision ID: 49df01e0c05e
Revises: 5676eac1bac1
Create Date: 2024-02-01 13:24:36.539435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49df01e0c05e'
down_revision: Union[str, None] = '5676eac1bac1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pipeline_task',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('pipeline_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=55), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('data', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['pipeline_id'], ['pipeline.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_pipeline_task_id'), 'pipeline_task', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_pipeline_task_id'), table_name='pipeline_task')
    op.drop_table('pipeline_task')
    # ### end Alembic commands ###
