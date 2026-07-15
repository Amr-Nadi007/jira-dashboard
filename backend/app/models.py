"""SQLAlchemy database models."""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Float
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base


class Agent(Base):
    """Agent model."""
    __tablename__ = "agents"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class JiraIssue(Base):
    """Jira issue model."""
    __tablename__ = "jira_issues"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String(50), unique=True, index=True, nullable=False)
    issue_type = Column(String(50))
    summary = Column(String(500))
    description = Column(Text)
    status = Column(String(50), index=True)
    country = Column(String(50), index=True)  # Egypt or Nigeria
    assignee = Column(String(255))
    reporter = Column(String(255))
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    jira_created_at = Column(DateTime(timezone=True))
    jira_updated_at = Column(DateTime(timezone=True))
    synced_at = Column(DateTime(timezone=True), server_default=func.now())


class IssueComment(Base):
    """Jira issue comment model."""
    __tablename__ = "issue_comments"
    
    id = Column(Integer, primary_key=True, index=True)
    issue_key = Column(String(50), index=True, nullable=False)
    comment_id = Column(String(100), unique=True, index=True)
    author = Column(String(255), index=True)
    body = Column(Text)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))
    synced_at = Column(DateTime(timezone=True), server_default=func.now())


class DailyAgentStats(Base):
    """Daily agent statistics model."""
    __tablename__ = "daily_agent_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(255), index=True, nullable=False)
    date = Column(String(10), index=True, nullable=False)  # YYYY-MM-DD
    egypt_count = Column(Integer, default=0)
    nigeria_count = Column(Integer, default=0)
    total_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Report(Base):
    """Report model."""
    __tablename__ = "reports"
    
    id = Column(Integer, primary_key=True, index=True)
    report_type = Column(String(20), index=True)  # morning, night
    report_date = Column(String(10), index=True)  # YYYY-MM-DD
    egypt_todo = Column(Integer, default=0)
    egypt_in_progress = Column(Integer, default=0)
    nigeria_todo = Column(Integer, default=0)
    nigeria_in_progress = Column(Integer, default=0)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Settings(Base):
    """System settings model."""
    __tablename__ = "settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(100), unique=True, index=True, nullable=False)
    value = Column(Text)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
