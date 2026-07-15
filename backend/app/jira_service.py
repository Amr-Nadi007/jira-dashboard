"""Jira Cloud API integration service."""
import requests
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class JiraService:
    """Service for Jira Cloud API interactions."""
    
    def __init__(self):
        """Initialize Jira service with credentials."""
        self.base_url = settings.jira_url
        self.email = settings.jira_email
        self.api_token = settings.jira_api_token
        self.auth = (self.email, self.api_token)
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.project_key = "DHNON"
    
    def _get_request(self, endpoint: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make GET request to Jira API."""
        try:
            url = f"{self.base_url}/rest/api/3{endpoint}"
            response = requests.get(url, auth=self.auth, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Jira API error: {str(e)}")
            return None
    
    def _get_field_value(self, issue: Dict, field_name: str) -> Optional[str]:
        """Get custom field value from issue."""
        try:
            fields = issue.get('fields', {})
            
            # Handle standard fields
            if field_name == 'Country':
                # Try to find country in custom fields
                for field_id, field_value in fields.items():
                    if field_id.startswith('customfield_') and field_value:
                        if isinstance(field_value, dict) and 'value' in field_value:
                            return field_value['value']
                        elif isinstance(field_value, str):
                            return field_value
            
            return None
        except Exception as e:
            logger.error(f"Error extracting field: {str(e)}")
            return None
    
    def get_issues(self) -> Optional[List[Dict]]:
        """Get all issues with key starting with DHNON."""
        try:
            jql = f'project = "{self.project_key}" ORDER BY updated DESC'
            params = {
                'jql': jql,
                'maxResults': 100,
                'expand': 'changelog'
            }
            
            issues = []
            start_at = 0
            
            while True:
                params['startAt'] = start_at
                result = self._get_request('/search', params)
                
                if not result:
                    break
                
                issues.extend(result.get('issues', []))
                
                if result.get('isLast', True):
                    break
                
                start_at += 100
            
            return issues
        except Exception as e:
            logger.error(f"Error fetching issues: {str(e)}")
            return None
    
    def get_issue_details(self, issue_key: str) -> Optional[Dict]:
        """Get detailed information for a specific issue."""
        return self._get_request(f'/issues/{issue_key}', {'expand': 'changelog'})
    
    def get_issue_comments(self, issue_key: str) -> Optional[List[Dict]]:
        """Get all comments for an issue."""
        try:
            result = self._get_request(f'/issues/{issue_key}/comments')
            return result.get('comments', []) if result else None
        except Exception as e:
            logger.error(f"Error fetching comments: {str(e)}")
            return None
    
    def parse_issue(self, issue: Dict) -> Dict:
        """Parse Jira issue to standardized format."""
        fields = issue.get('fields', {})
        
        return {
            'issue_key': issue.get('key'),
            'issue_type': fields.get('issuetype', {}).get('name'),
            'summary': fields.get('summary'),
            'description': fields.get('description'),
            'status': fields.get('status', {}).get('name'),
            'assignee': fields.get('assignee', {}).get('displayName') if fields.get('assignee') else None,
            'reporter': fields.get('reporter', {}).get('displayName') if fields.get('reporter') else None,
            'created': fields.get('created'),
            'updated': fields.get('updated'),
            'country': self._extract_country(fields)
        }
    
    def _extract_country(self, fields: Dict) -> Optional[str]:
        """Extract country from issue fields (Jira Assets or custom field)."""
        # Look for country in custom fields
        for field_id, field_value in fields.items():
            if field_id.startswith('customfield_'):
                # Check if it's a country field
                if isinstance(field_value, dict):
                    value = field_value.get('value')
                    if value in ['Egypt', 'Nigeria']:
                        return value
                elif isinstance(field_value, str):
                    if field_value in ['Egypt', 'Nigeria']:
                        return field_value
                elif isinstance(field_value, list) and len(field_value) > 0:
                    first_item = field_value[0]
                    if isinstance(first_item, dict):
                        value = first_item.get('value')
                        if value in ['Egypt', 'Nigeria']:
                            return value
        
        return None
    
    def get_comments_by_author(self, issue_key: str, author_name: str) -> Optional[List[Dict]]:
        """Get comments for an issue by specific author."""
        comments = self.get_issue_comments(issue_key)
        if not comments:
            return None
        
        return [c for c in comments if c.get('author', {}).get('displayName') == author_name]
    
    def is_working_hours(self, timestamp_str: str) -> bool:
        """Check if timestamp is within working hours (08:00 - 00:00)."""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            hour = dt.hour
            # 08:00 (8) to 23:59 (23) - midnight is 00:00
            return 8 <= hour < 24
        except Exception as e:
            logger.error(f"Error parsing timestamp: {str(e)}")
            return False
    
    def get_active_agents_for_date(self, date_str: str) -> List[str]:
        """Get agents who commented on issues on a specific date."""
        agents = set()
        issues = self.get_issues()
        
        if not issues:
            return []
        
        for issue in issues:
            comments = self.get_issue_comments(issue['key'])
            if comments:
                for comment in comments:
                    created = comment.get('created')
                    if created and created.startswith(date_str) and self.is_working_hours(created):
                        author = comment.get('author', {}).get('displayName')
                        if author:
                            agents.add(author)
        
        return list(agents)
