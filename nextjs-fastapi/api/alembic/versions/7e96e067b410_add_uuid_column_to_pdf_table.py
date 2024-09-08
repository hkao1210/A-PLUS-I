"""Add UUID column to PDF table

Revision ID: 7e96e067b410
Revises: 965a9221f015
Create Date: 2023-09-07 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import uuid

# revision identifiers, used by Alembic.
revision = '7e96e067b410'
down_revision = '965a9221f015'
branch_labels = None
depends_on = None

def upgrade():
    # Add a new UUID column
    op.add_column('pdfs', sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True))
    
    # Generate UUIDs for existing rows
    op.execute("UPDATE pdfs SET uuid = gen_random_uuid()")
    
    # Make the UUID column not nullable
    op.alter_column('pdfs', 'uuid', nullable=False)
    
    # Drop the old id column and rename uuid to id
    op.drop_column('pdfs', 'id')
    op.alter_column('pdfs', 'uuid', new_column_name='id')
    
    # Add primary key constraint to the new id column
    op.create_primary_key(None, 'pdfs', ['id'])

def downgrade():
    # Add back the integer id column
    op.add_column('pdfs', sa.Column('int_id', sa.Integer(), autoincrement=True, nullable=True))
    
    # Generate sequential IDs
    op.execute("UPDATE pdfs SET int_id = nextval('pdfs_id_seq')")
    
    # Make the int_id column not nullable
    op.alter_column('pdfs', 'int_id', nullable=False)
    
    # Drop the UUID id column and rename int_id to id
    op.drop_column('pdfs', 'id')
    op.alter_column('pdfs', 'int_id', new_column_name='id')
    
    # Add primary key constraint to the new id column
    op.create_primary_key(None, 'pdfs', ['id'])