"""Scheduler service for automated tasks."""
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import crud, models
from app.jira_service import JiraService
from pytz import timezone

logger = logging.getLogger(__name__)
CAIRO_TZ = timezone('Africa/Cairo')


class SchedulerService:
    """Service for managing scheduled tasks."""
    
    def __init__(self):
        """Initialize scheduler."""
        self.scheduler = BackgroundScheduler()
        self.jira_service = JiraService()
    
    def start(self):
        """Start the scheduler."""
        if self.scheduler.running:
            return
        
        # Morning report at 08:00
        self.scheduler.add_job(
            self.generate_morning_report,
            CronTrigger(hour=8, minute=0, timezone=CAIRO_TZ),
            id='morning_report',
            name='Generate morning report',
            replace_existing=True
        )
        
        # Night report at 00:00 (midnight)
        self.scheduler.add_job(
            self.generate_night_report,
            CronTrigger(hour=0, minute=0, timezone=CAIRO_TZ),
            id='night_report',
            name='Generate night report',
            replace_existing=True
        )
        
        # Sync Jira data every hour
        self.scheduler.add_job(
            self.sync_jira_data,
            CronTrigger(minute=0, timezone=CAIRO_TZ),
            id='sync_jira',
            name='Sync Jira data',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Scheduler started successfully")
    
    def stop(self):
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Scheduler stopped")
    
    def generate_morning_report(self):
        """Generate morning report at 08:00."""
        try:
            db = SessionLocal()
            logger.info("Generating morning report...")
            
            # Get current date
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Get dashboard stats
            stats = crud.get_dashboard_stats(db)
            
            # Create report
            report = {
                'report_type': 'morning',
                'report_date': today,
                'egypt_todo': stats['egypt_todo'],
                'egypt_in_progress': stats['egypt_in_progress'],
                'nigeria_todo': stats['nigeria_todo'],
                'nigeria_in_progress': stats['nigeria_in_progress'],
                'content': self._format_report(stats, 'morning')
            }
            
            crud.create_report(db, report)
            logger.info(f"Morning report generated for {today}")
            
        except Exception as e:
            logger.error(f"Error generating morning report: {str(e)}")
        finally:
            db.close()
    
    def generate_night_report(self):
        """Generate night report at 00:00 (midnight)."""
        try:
            db = SessionLocal()
            logger.info("Generating night report...")
            
            # Get yesterday's date for the report
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Get dashboard stats
            stats = crud.get_dashboard_stats(db)
            
            # Create report
            report = {
                'report_type': 'night',
                'report_date': yesterday,
                'egypt_todo': stats['egypt_todo'],
                'egypt_in_progress': stats['egypt_in_progress'],
                'nigeria_todo': stats['nigeria_todo'],
                'nigeria_in_progress': stats['nigeria_in_progress'],
                'content': self._format_report(stats, 'night')
            }
            
            crud.create_report(db, report)
            logger.info(f"Night report generated for {yesterday}")
            
        except Exception as e:
            logger.error(f"Error generating night report: {str(e)}")
        finally:
            db.close()
    
    def sync_jira_data(self):
        """Sync data from Jira Cloud."""
        try:
            db = SessionLocal()
            logger.info("Syncing data from Jira...")
            
            issues = self.jira_service.get_issues()
            if not issues:
                logger.warning("No issues found in Jira")
                return
            
            synced_count = 0
            for issue in issues:
                parsed_issue = self.jira_service.parse_issue(issue)
                crud.create_or_update_issue(db, parsed_issue)
                synced_count += 1
                
                # Sync comments
                comments = self.jira_service.get_issue_comments(issue['key'])
                if comments:
                    for comment in comments:
                        comment_data = {
                            'issue_key': issue['key'],
                            'comment_id': comment.get('id'),
                            'author': comment.get('author', {}).get('displayName'),
                            'body': comment.get('body'),
                            'created_at': comment.get('created'),
                            'updated_at': comment.get('updated')
                        }
                        # Check if comment already exists
                        existing = db.query(models.IssueComment).filter(
                            models.IssueComment.comment_id == comment.get('id')
                        ).first()
                        if not existing:
                            crud.create_comment(db, comment_data)
            
            logger.info(f"Synced {synced_count} issues from Jira")
            
        except Exception as e:
            logger.error(f"Error syncing Jira data: {str(e)}")
        finally:
            db.close()
    
    def _format_report(self, stats: dict, report_type: str) -> str:
        """Format report content."""
        title = "Morning Report" if report_type == 'morning' else "Night Report"
        return f"""
{title}
{'=' * 50}

Egypt:
  TO DO: {stats['egypt_todo']}
  IN PROGRESS: {stats['egypt_in_progress']}
  
Nigeria:
  TO DO: {stats['nigeria_todo']}
  IN PROGRESS: {stats['nigeria_in_progress']}

Total:
  TO DO: {stats['egypt_todo'] + stats['nigeria_todo']}
  IN PROGRESS: {stats['egypt_in_progress'] + stats['nigeria_in_progress']}
        """
