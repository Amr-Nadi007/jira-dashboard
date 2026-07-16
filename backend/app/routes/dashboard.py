"""Dashboard routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/", response_model=schemas.DashboardStatsSchema)
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get dashboard statistics."""
    stats = crud.get_dashboard_stats(db)
    return stats


@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary."""
    stats = crud.get_dashboard_stats(db)
    return {
        "status": "success",
        "data": {
            "egypt": {
                "todo": stats['egypt_todo'],
                "in_progress": stats['egypt_in_progress'],
                "total": stats['egypt_todo'] + stats['egypt_in_progress']
            },
            "nigeria": {
                "todo": stats['nigeria_todo'],
                "in_progress": stats['nigeria_in_progress'],
                "total": stats['nigeria_todo'] + stats['nigeria_in_progress']
            },
            "total": {
                "todo": stats['egypt_todo'] + stats['nigeria_todo'],
                "in_progress": stats['egypt_in_progress'] + stats['nigeria_in_progress'],
                "total": stats['egypt_todo'] + stats['egypt_in_progress'] + stats['nigeria_todo'] + stats['nigeria_in_progress']
            }
        }
    }
