"""I addded relationships,serialize-rules to the tables

Revision ID: 569c0a92e4ca
Revises: 821c2ab7db52
Create Date: 2024-04-21 17:53:03.986718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '569c0a92e4ca'
down_revision = '821c2ab7db52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('appearances', sa.Column('episode_id', sa.Integer(), nullable=True))
    op.add_column('appearances', sa.Column('guest_id', sa.Integer(), nullable=True))
    op.create_foreign_key(op.f('fk_appearances_episode_id_episodes'), 'appearances', 'episodes', ['episode_id'], ['id'])
    op.create_foreign_key(op.f('fk_appearances_guest_id_guests'), 'appearances', 'guests', ['guest_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_appearances_guest_id_guests'), 'appearances', type_='foreignkey')
    op.drop_constraint(op.f('fk_appearances_episode_id_episodes'), 'appearances', type_='foreignkey')
    op.drop_column('appearances', 'guest_id')
    op.drop_column('appearances', 'episode_id')
    # ### end Alembic commands ###
