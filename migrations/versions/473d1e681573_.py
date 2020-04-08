"""empty message

Revision ID: 473d1e681573
Revises: 4a91f657679b
Create Date: 2020-04-08 16:51:55.397326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '473d1e681573'
down_revision = '4a91f657679b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts_categorys',
    sa.Column('posts_id', sa.Integer(), nullable=False),
    sa.Column('categorys_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['categorys_id'], ['categorys.id'], ),
    sa.ForeignKeyConstraint(['posts_id'], ['posts.id'], ),
    sa.PrimaryKeyConstraint('posts_id', 'categorys_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('posts_categorys')
    # ### end Alembic commands ###