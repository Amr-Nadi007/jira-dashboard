"""Admin routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, models
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])


# ===== Agents Management =====
@router.get("/agents", response_model=List[schemas.Agent])
def list_agents(db: Session = Depends(get_db)):
    """Get all agents."""
    return crud.get_agents(db)


@router.get("/agents/active", response_model=List[schemas.Agent])
def list_active_agents(db: Session = Depends(get_db)):
    """Get active agents."""
    return crud.get_active_agents(db)


@router.post("/agents", response_model=schemas.Agent)
def create_agent(agent: schemas.AgentCreate, db: Session = Depends(get_db)):
    """Create a new agent."""
    existing = crud.get_agent_by_name(db, agent.name)
    if existing:
        return {"error": "Agent already exists"}
    return crud.create_agent(db, agent)


@router.get("/agents/{agent_id}", response_model=schemas.Agent)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """Get agent by ID."""
    agent = crud.get_agent(db, agent_id)
    if not agent:
        return {"error": "Agent not found"}
    return agent


@router.put("/agents/{agent_id}", response_model=schemas.Agent)
def update_agent(
    agent_id: int,
    agent_update: schemas.AgentUpdate,
    db: Session = Depends(get_db)
):
    """Update agent."""
    agent = crud.update_agent(db, agent_id, agent_update)
    if not agent:
        return {"error": "Agent not found"}
    return agent


@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """Delete agent."""
    success = crud.delete_agent(db, agent_id)
    if not success:
        return {"error": "Agent not found"}
    return {"status": "success", "message": "Agent deleted"}


# ===== Settings Management =====
@router.get("/settings")
def get_settings(db: Session = Depends(get_db)):
    """Get Jira settings."""
    jira_url = crud.get_setting(db, 'jira_url')
    jira_email = crud.get_setting(db, 'jira_email')
    
    return {
        "status": "success",
        "data": {
            "jira_url": jira_url.value if jira_url else None,
            "jira_email": jira_email.value if jira_email else None
        }
    }


@router.post("/settings")
def update_settings(
    settings: schemas.AdminSettingsSchema,
    db: Session = Depends(get_db)
):
    """Update Jira settings."""
    crud.set_setting(db, 'jira_url', settings.jira_url)
    crud.set_setting(db, 'jira_email', settings.jira_email)
    crud.set_setting(db, 'jira_api_token', settings.jira_api_token)
    
    return {
        "status": "success",
        "message": "Settings updated successfully"
    }


# ===== Sync Management =====
@router.post("/sync")
def trigger_sync(db: Session = Depends(get_db)):
    """Trigger manual Jira sync."""
    try:
        from app.jira_service import JiraService
        from app import crud
        
        jira_service = JiraService()
        issues = jira_service.get_issues()
        
        if not issues:
            return {
                "status": "success",
                "message": "No issues found",
                "issues_synced": 0
            }
        
        synced_count = 0
        for issue in issues:
            parsed_issue = jira_service.parse_issue(issue)
            crud.create_or_update_issue(db, parsed_issue)
            synced_count += 1
        
        return {
            "status": "success",
            "message": f"Synced {synced_count} issues",
            "issues_synced": synced_count
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


@router.get("/sync-status")
def get_sync_status(db: Session = Depends(get_db)):
    """Get last sync status."""
    latest_issue = db.query(models.JiraIssue).order_by(
        models.JiraIssue.synced_at.desc()
    ).first()
    
    if not latest_issue:
        return {
            "status": "no_sync",
            "message": "No sync has been performed yet"
        }
    
    return {
        "status": "success",
        "last_sync": latest_issue.synced_at,
        "total_issues": db.query(models.JiraIssue).count()
    }
