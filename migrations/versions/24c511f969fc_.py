"""empty message

Revision ID: 24c511f969fc
Revises: 
Create Date: 2021-01-19 20:35:15.762371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24c511f969fc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Actor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Movie',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Movie_Actor',
    sa.Column('Movie_id', sa.Integer(), nullable=True),
    sa.Column('Actor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['Actor_id'], ['Actor.id'], ),
    sa.ForeignKeyConstraint(['Movie_id'], ['Movie.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Movie_Actor')
    op.drop_table('Movie')
    op.drop_table('Actor')
    # ### end Alembic commands ###
