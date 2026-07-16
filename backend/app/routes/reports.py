"""Reports routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/report", tags=["reports"])


@router.get("/morning")
def get_morning_report(db: Session = Depends(get_db)):
    """Get morning report."""
    today = datetime.now().strftime('%Y-%m-%d')
    report = crud.get_report_by_date_and_type(db, today, 'morning')
    
    if not report:
        return {"status": "not_found", "message": "No morning report for today"}
    
    return {
        "status": "success",
        "data": {
            "report_type": report.report_type,
            "report_date": report.report_date,
            "egypt_todo": report.egypt_todo,
            "egypt_in_progress": report.egypt_in_progress,
            "nigeria_todo": report.nigeria_todo,
            "nigeria_in_progress": report.nigeria_in_progress,
            "content": report.content,
            "created_at": report.created_at
        }
    }


@router.get("/night")
def get_night_report(db: Session = Depends(get_db)):
    """Get night report."""
    today = datetime.now().strftime('%Y-%m-%d')
    report = crud.get_report_by_date_and_type(db, today, 'night')
    
    if not report:
        return {"status": "not_found", "message": "No night report for today"}
    
    return {
        "status": "success",
        "data": {
            "report_type": report.report_type,
            "report_date": report.report_date,
            "egypt_todo": report.egypt_todo,
            "egypt_in_progress": report.egypt_in_progress,
            "nigeria_todo": report.nigeria_todo,
            "nigeria_in_progress": report.nigeria_in_progress,
            "content": report.content,
            "created_at": report.created_at
        }
    }


@router.get("/by-date/{date_str}")
def get_reports_by_date(date_str: str, db: Session = Depends(get_db)):
    """Get all reports for a specific date."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    morning_report = crud.get_report_by_date_and_type(db, date_str, 'morning')
    night_report = crud.get_report_by_date_and_type(db, date_str, 'night')
    
    reports = []
    if morning_report:
        reports.append({
            "report_type": "morning",
            "report_date": morning_report.report_date,
            "egypt_todo": morning_report.egypt_todo,
            "egypt_in_progress": morning_report.egypt_in_progress,
            "nigeria_todo": morning_report.nigeria_todo,
            "nigeria_in_progress": morning_report.nigeria_in_progress,
            "content": morning_report.content,
            "created_at": morning_report.created_at
        })
    
    if night_report:
        reports.append({
            "report_type": "night",
            "report_date": night_report.report_date,
            "egypt_todo": night_report.egypt_todo,
            "egypt_in_progress": night_report.egypt_in_progress,
            "nigeria_todo": night_report.nigeria_todo,
            "nigeria_in_progress": night_report.nigeria_in_progress,
            "content": night_report.content,
            "created_at": night_report.created_at
        })
    
    return {
        "status": "success",
        "date": date_str,
        "reports": reports
    }
