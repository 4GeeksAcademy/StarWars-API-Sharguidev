"""empty message

Revision ID: b610cee96b86
Revises: a04aeaa7a19d
Create Date: 2024-11-20 10:56:12.244906

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b610cee96b86'
down_revision = 'a04aeaa7a19d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('planets_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.alter_column('planets_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('people_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###