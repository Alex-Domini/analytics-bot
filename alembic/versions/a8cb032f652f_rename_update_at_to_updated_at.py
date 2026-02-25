"""rename update_at to updated_at

Revision ID: a8cb032f652f
Revises: ba534efc3db4
Create Date: 2026-02-25 22:03:33.328277

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a8cb032f652f"
down_revision: Union[str, Sequence[str], None] = "ba534efc3db4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column("video_snapshots", "update_at", new_column_name="updated_at")


def downgrade():
    op.alter_column("video_snapshots", "updated_at", new_column_name="update_at")
