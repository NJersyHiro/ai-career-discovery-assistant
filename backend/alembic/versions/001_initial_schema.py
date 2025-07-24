"""Initial schema creation

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_superuser', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)

    # Create documents table
    op.create_table('documents',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('filename', sa.String(), nullable=False),
        sa.Column('file_type', sa.String(), nullable=False),
        sa.Column('document_type', sa.Enum('RESUME', 'CV', 'SKILL_SHEET', 'OTHER', name='documenttype'), nullable=True),
        sa.Column('file_size', sa.Integer(), nullable=False),
        sa.Column('s3_key', sa.String(), nullable=False),
        sa.Column('status', sa.Enum('UPLOADED', 'PROCESSING', 'PROCESSED', 'FAILED', name='documentstatus'), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('raw_text', sa.Text(), nullable=True),
        sa.Column('structured_data', sa.JSON(), nullable=True),
        sa.Column('extracted_skills', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_documents_id'), 'documents', ['id'], unique=False)

    # Create analyses table
    op.create_table('analyses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('document_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.Enum('PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', name='analysisstatus'), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('processing_time', sa.Float(), nullable=True),
        sa.Column('career_paths', sa.JSON(), nullable=True),
        sa.Column('skill_gaps', sa.JSON(), nullable=True),
        sa.Column('market_insights', sa.JSON(), nullable=True),
        sa.Column('gemini_prompt', sa.Text(), nullable=True),
        sa.Column('gemini_response', sa.JSON(), nullable=True),
        sa.Column('confidence_scores', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_analyses_id'), 'analyses', ['id'], unique=False)

    # Create career_recommendations table
    op.create_table('career_recommendations',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('analysis_id', sa.Integer(), nullable=False),
        sa.Column('career_type', sa.Enum('CORPORATE', 'FREELANCE', 'ENTREPRENEURSHIP', name='careertype'), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('required_skills', sa.JSON(), nullable=False),
        sa.Column('skill_match_percentage', sa.Float(), nullable=False),
        sa.Column('skill_gaps', sa.JSON(), nullable=True),
        sa.Column('salary_range_min', sa.Integer(), nullable=True),
        sa.Column('salary_range_max', sa.Integer(), nullable=True),
        sa.Column('market_demand', sa.String(), nullable=True),
        sa.Column('recommended_courses', sa.JSON(), nullable=True),
        sa.Column('estimated_preparation_time', sa.Integer(), nullable=True),
        sa.Column('pros', sa.JSON(), nullable=True),
        sa.Column('cons', sa.JSON(), nullable=True),
        sa.Column('next_steps', sa.JSON(), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_career_recommendations_id'), 'career_recommendations', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_career_recommendations_id'), table_name='career_recommendations')
    op.drop_table('career_recommendations')
    op.drop_index(op.f('ix_analyses_id'), table_name='analyses')
    op.drop_table('analyses')
    op.drop_index(op.f('ix_documents_id'), table_name='documents')
    op.drop_table('documents')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS documenttype')
    op.execute('DROP TYPE IF EXISTS documentstatus')
    op.execute('DROP TYPE IF EXISTS analysisstatus')
    op.execute('DROP TYPE IF EXISTS careertype')