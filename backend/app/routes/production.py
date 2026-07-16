"""Production dashboard routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from datetime import datetime, date
from app.database import get_db
from app import crud, models, schemas

router = APIRouter(prefix="/production", tags=["production"])


def get_agent_issues_for_date(db: Session, agent_name: str, date_str: str) -> dict:
    """Get count of issues per agent per country for a specific date."""
    # Get comments by agent on specific date
    comments = db.query(models.IssueComment).filter(
        and_(
            models.IssueComment.author == agent_name,
            func.date(models.IssueComment.created_at) == date_str
        )
    ).all()
    
    if not comments:
        return {'egypt': 0, 'nigeria': 0}
    
    # Get unique issue keys with comments from this agent
    issue_keys = set(c.issue_key for c in comments)
    
    # Count issues by country (only one per issue per day)
    egypt_count = 0
    nigeria_count = 0
    
    for issue_key in issue_keys:
        issue = db.query(models.JiraIssue).filter(
            models.JiraIssue.issue_key == issue_key
        ).first()
        
        if issue:
            if issue.country == 'Egypt':
                egypt_count += 1
            elif issue.country == 'Nigeria':
                nigeria_count += 1
    
    return {'egypt': egypt_count, 'nigeria': nigeria_count}


@router.get("/", response_model=schemas.ProductionDashboardSchema)
def get_production_dashboard(db: Session = Depends(get_db)):
    """Get production dashboard with agent statistics."""
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Get active agents
    active_agents = crud.get_active_agents(db)
    
    agents_data = []
    total_egypt = 0
    total_nigeria = 0
    
    for agent in active_agents:
        counts = get_agent_issues_for_date(db, agent.name, today)
        
        agent_entry = schemas.ProductionAgentSchema(
            agent=agent.name,
            egypt=counts['egypt'],
            nigeria=counts['nigeria'],
            total=counts['egypt'] + counts['nigeria']
        )
        agents_data.append(agent_entry)
        total_egypt += counts['egypt']
        total_nigeria += counts['nigeria']
    
    return schemas.ProductionDashboardSchema(
        agents=agents_data,
        total_egypt=total_egypt,
        total_nigeria=total_nigeria,
        total_all=total_egypt + total_nigeria
    )


@router.get("/by-date/{date_str}")
def get_production_dashboard_by_date(date_str: str, db: Session = Depends(get_db)):
    """Get production dashboard for a specific date."""
    # Validate date format YYYY-MM-DD
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    # Get active agents
    active_agents = crud.get_active_agents(db)
    
    agents_data = []
    total_egypt = 0
    total_nigeria = 0
    
    for agent in active_agents:
        counts = get_agent_issues_for_date(db, agent.name, date_str)
        
        agent_entry = schemas.ProductionAgentSchema(
            agent=agent.name,
            egypt=counts['egypt'],
            nigeria=counts['nigeria'],
            total=counts['egypt'] + counts['nigeria']
        )
        agents_data.append(agent_entry)
        total_egypt += counts['egypt']
        total_nigeria += counts['nigeria']
    
    return schemas.ProductionDashboardSchema(
        agents=agents_data,
        total_egypt=total_egypt,
        total_nigeria=total_nigeria,
        total_all=total_egypt + total_nigeria
    )
