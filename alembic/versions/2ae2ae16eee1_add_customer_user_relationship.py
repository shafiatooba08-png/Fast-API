"""add customer user relationship

Revision ID: 2ae2ae16eee1
Revises: affeab119ad7
Create Date: 2026-07-19 22:50:57.532531

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = '2ae2ae16eee1'
down_revision: Union[str, Sequence[str], None] = 'affeab119ad7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add user relationship to customers table
    op.add_column(
        'customers',
        sa.Column(
            'user_id',
            sa.Integer(),
            nullable=True
        )
    )

    op.create_unique_constraint(
        None,
        'customers',
        ['user_id']
    )

    op.create_foreign_key(
        None,
        'customers',
        'users',
        ['user_id'],
        ['id']
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(
        None,
        'customers',
        type_='foreignkey'
    )

    op.drop_constraint(
        None,
        'customers',
        type_='unique'
    )

    op.drop_column(
        'customers',
        'user_id'
    )