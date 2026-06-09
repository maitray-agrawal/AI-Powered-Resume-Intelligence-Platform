"""initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-06-09 18:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_schema'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. users Table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # 2. resumes Table
    op.create_table(
        'resumes',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resumes_user_id'), 'resumes', ['user_id'], unique=False)

    # 3. resume_versions Table
    op.create_table(
        'resume_versions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('resume_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('version_number', sa.Integer(), nullable=False),
        sa.Column('file_name', sa.String(length=255), nullable=False),
        sa.Column('file_path', sa.String(length=512), nullable=False),
        sa.Column('raw_text', sa.Text(), nullable=False),
        sa.Column('structured_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resume_versions_resume_id'), 'resume_versions', ['resume_id'], unique=False)

    # 4. job_descriptions Table
    op.create_table(
        'job_descriptions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('company', sa.String(length=255), nullable=True),
        sa.Column('description_text', sa.Text(), nullable=False),
        sa.Column('requirements', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_job_descriptions_user_id'), 'job_descriptions', ['user_id'], unique=False)

    # 5. ats_reports Table
    op.create_table(
        'ats_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('resume_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('findings', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('suggestions', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['resume_version_id'], ['resume_versions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ats_reports_resume_version_id'), 'ats_reports', ['resume_version_id'], unique=False)

    # 6. match_reports Table
    op.create_table(
        'match_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('resume_version_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('job_description_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('score', sa.Float(), nullable=False),
        sa.Column('skills_matched', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('skills_missing', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['job_description_id'], ['job_descriptions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['resume_version_id'], ['resume_versions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_match_reports_job_description_id'), 'match_reports', ['job_description_id'], unique=False)
    op.create_index(op.f('ix_match_reports_resume_version_id'), 'match_reports', ['resume_version_id'], unique=False)

    # 7. chat_sessions Table
    op.create_table(
        'chat_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('resume_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('history', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['resume_id'], ['resumes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_sessions_resume_id'), 'chat_sessions', ['resume_id'], unique=False)
    op.create_index(op.f('ix_chat_sessions_user_id'), 'chat_sessions', ['user_id'], unique=False)

    # 8. agent_reports Table
    op.create_table(
        'agent_reports',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('report_type', sa.String(length=255), nullable=False),
        sa.Column('content', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_agent_reports_user_id'), 'agent_reports', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_agent_reports_user_id'), table_name='agent_reports')
    op.drop_table('agent_reports')
    op.drop_index(op.f('ix_chat_sessions_user_id'), table_name='chat_sessions')
    op.drop_index(op.f('ix_chat_sessions_resume_id'), table_name='chat_sessions')
    op.drop_table('chat_sessions')
    op.drop_index(op.f('ix_match_reports_resume_version_id'), table_name='match_reports')
    op.drop_index(op.f('ix_match_reports_job_description_id'), table_name='match_reports')
    op.drop_table('match_reports')
    op.drop_index(op.f('ix_ats_reports_resume_version_id'), table_name='ats_reports')
    op.drop_table('ats_reports')
    op.drop_index(op.f('ix_job_descriptions_user_id'), table_name='job_descriptions')
    op.drop_table('job_descriptions')
    op.drop_index(op.f('ix_resume_versions_resume_id'), table_name='resume_versions')
    op.drop_table('resume_versions')
    op.drop_index(op.f('ix_resumes_user_id'), table_name='resumes')
    op.drop_table('resumes')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
