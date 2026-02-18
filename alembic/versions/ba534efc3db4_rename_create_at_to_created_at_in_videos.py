"""rename create_at to created_at in videos

Revision ID: ba534efc3db4
Revises: 8e127ceeb1fe
Create Date: 2026-02-18 23:29:13.996150

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ba534efc3db4"
down_revision: Union[str, Sequence[str], None] = "8e127ceeb1fe"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column("video_snapshots", "create_at", new_column_name="created_at")


def downgrade():
    op.alter_column("video_snapshots", "created_at", new_column_name="create_at")
