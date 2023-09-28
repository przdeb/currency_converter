"""init

Revision ID: 36d2110c8538
Revises:
Create Date: 2023-09-27 18:52:48.760758

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "36d2110c8538"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "converted_price_pln",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("currency", sa.String(length=3), nullable=True),
        sa.Column("rate", sa.Float(precision=4), nullable=True),
        sa.Column("price_in_pln", sa.Float(precision=2), nullable=True),
        sa.Column("date", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("converted_price_pln")
    # ### end Alembic commands ###