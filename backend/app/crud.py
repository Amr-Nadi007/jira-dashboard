"""CRUD operations for database models."""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, date
from app import models, schemas
from typing import List, Optional


# ===== Agent CRUD =====
def create_agent(db: Session, agent: schemas.AgentCreate) -> models.Agent:
    """Create a new agent."""
    db_agent = models.Agent(**agent.model_dump())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


def get_agent(db: Session, agent_id: int) -> Optional[models.Agent]:
    """Get agent by ID."""
    return db.query(models.Agent).filter(models.Agent.id == agent_id).first()


def get_agent_by_name(db: Session, name: str) -> Optional[models.Agent]:
    """Get agent by name."""
    return db.query(models.Agent).filter(models.Agent.name == name).first()


def get_agents(db: Session, skip: int = 0, limit: int = 100) -> List[models.Agent]:
    """Get all agents."""
    return db.query(models.Agent).offset(skip).limit(limit).all()


def get_active_agents(db: Session) -> List[models.Agent]:
    """Get all active agents."""
    return db.query(models.Agent).filter(models.Agent.is_active == True).all()


def update_agent(db: Session, agent_id: int, agent: schemas.AgentUpdate) -> Optional[models.Agent]:
    """Update agent."""
    db_agent = get_agent(db, agent_id)
    if not db_agent:
        return None
    
    for key, value in agent.model_dump(exclude_unset=True).items():
        setattr(db_agent, key, value)
    
    db.commit()
    db.refresh(db_agent)
    return db_agent


def delete_agent(db: Session, agent_id: int) -> bool:
    """Delete agent."""
    db_agent = get_agent(db, agent_id)
    if not db_agent:
        return False
    
    db.delete(db_agent)
    db.commit()
    return True


# ===== Jira Issue CRUD =====
def create_or_update_issue(db: Session, issue_data: Dict) -> models.JiraIssue:
    """Create or update Jira issue."""
    db_issue = db.query(models.JiraIssue).filter(
        models.JiraIssue.issue_key == issue_data['issue_key']
    ).first()
    
    if db_issue:
        # Update existing
        for key, value in issue_data.items():
            setattr(db_issue, key, value)
        db_issue.synced_at = datetime.utcnow()
    else:
        # Create new
        db_issue = models.JiraIssue(**issue_data, synced_at=datetime.utcnow())
        db.add(db_issue)
    
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issues_by_country_and_status(
    db: Session, country: str, status: str
) -> List[models.JiraIssue]:
    """Get issues by country and status."""
    return db.query(models.JiraIssue).filter(
        and_(
            models.JiraIssue.country == country,
            models.JiraIssue.status == status
        )
    ).all()


def get_dashboard_stats(db: Session) -> Dict:
    """Get dashboard statistics."""
    stats = {
        'egypt_todo': len(get_issues_by_country_and_status(db, 'Egypt', 'TO DO')),
        'egypt_in_progress': len(get_issues_by_country_and_status(db, 'Egypt', 'IN PROGRESS')),
        'nigeria_todo': len(get_issues_by_country_and_status(db, 'Nigeria', 'TO DO')),
        'nigeria_in_progress': len(get_issues_by_country_and_status(db, 'Nigeria', 'IN PROGRESS')),
    }
    return stats


# ===== Issue Comment CRUD =====
def create_comment(db: Session, comment_data: Dict) -> models.IssueComment:
    """Create issue comment."""
    db_comment = models.IssueComment(**comment_data)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments_by_issue(db: Session, issue_key: str) -> List[models.IssueComment]:
    """Get all comments for an issue."""
    return db.query(models.IssueComment).filter(
        models.IssueComment.issue_key == issue_key
    ).all()


def get_comments_by_author_and_date(
    db: Session, author: str, date_str: str
) -> List[models.IssueComment]:
    """Get comments by author on a specific date."""
    return db.query(models.IssueComment).filter(
        and_(
            models.IssueComment.author == author,
            func.date(models.IssueComment.created_at) == date_str
        )
    ).all()


# ===== Daily Stats CRUD =====
def create_or_update_daily_stats(
    db: Session, agent_name: str, date_str: str, stats: Dict
) -> models.DailyAgentStats:
    """Create or update daily agent statistics."""
    db_stats = db.query(models.DailyAgentStats).filter(
        and_(
            models.DailyAgentStats.agent_name == agent_name,
            models.DailyAgentStats.date == date_str
        )
    ).first()
    
    if db_stats:
        db_stats.egypt_count = stats.get('egypt_count', 0)
        db_stats.nigeria_count = stats.get('nigeria_count', 0)
        db_stats.total_count = stats.get('total_count', 0)
    else:
        db_stats = models.DailyAgentStats(
            agent_name=agent_name,
            date=date_str,
            **stats
        )
        db.add(db_stats)
    
    db.commit()
    db.refresh(db_stats)
    return db_stats


def get_daily_stats_by_date(db: Session, date_str: str) -> List[models.DailyAgentStats]:
    """Get all daily stats for a specific date."""
    return db.query(models.DailyAgentStats).filter(
        models.DailyAgentStats.date == date_str
    ).all()


# ===== Report CRUD =====
def create_report(db: Session, report: Dict) -> models.Report:
    """Create a new report."""
    db_report = models.Report(**report)
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report_by_date_and_type(
    db: Session, date_str: str, report_type: str
) -> Optional[models.Report]:
    """Get report by date and type."""
    return db.query(models.Report).filter(
        and_(
            models.Report.report_date == date_str,
            models.Report.report_type == report_type
        )
    ).first()


# ===== Settings CRUD =====
def get_setting(db: Session, key: str) -> Optional[models.Settings]:
    """Get setting by key."""
    return db.query(models.Settings).filter(models.Settings.key == key).first()


def set_setting(db: Session, key: str, value: str) -> models.Settings:
    """Set or update a setting."""
    db_setting = get_setting(db, key)
    
    if db_setting:
        db_setting.value = value
    else:
        db_setting = models.Settings(key=key, value=value)
        db.add(db_setting)
    
    db.commit()
    db.refresh(db_setting)
    return db_setting


from typing import Dict
