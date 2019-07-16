"""empty message

Revision ID: 50c9a4011b95
Revises: d60eb41dc3f8
Create Date: 2019-07-09 20:46:07.109732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '50c9a4011b95'
down_revision = 'd60eb41dc3f8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('languages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('programm_langs_in_job',
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], ),
    sa.ForeignKeyConstraint(['language_id'], ['languages.id'], )
    )
    op.add_column('jobs', sa.Column('is_automation', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('jobs', 'is_automation')
    op.drop_table('programm_langs_in_job')
    op.drop_table('languages')
    # ### end Alembic commands ###
