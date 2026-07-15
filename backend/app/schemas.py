"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Agent Schemas
class AgentBase(BaseModel):
    name: str
    email: Optional[str] = None
    is_active: bool = True


class AgentCreate(AgentBase):
    pass


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None


class Agent(AgentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Jira Issue Schemas
class JiraIssueBase(BaseModel):
    issue_key: str
    issue_type: Optional[str] = None
    summary: Optional[str] = None
    status: Optional[str] = None
    country: Optional[str] = None


class JiraIssue(JiraIssueBase):
    id: int
    assignee: Optional[str] = None
    reporter: Optional[str] = None
    synced_at: datetime
    
    class Config:
        from_attributes = True


# Daily Stats Schemas
class DailyAgentStatsSchema(BaseModel):
    agent_name: str
    date: str
    egypt_count: int
    nigeria_count: int
    total_count: int
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class DashboardStatsSchema(BaseModel):
    egypt_todo: int
    egypt_in_progress: int
    nigeria_todo: int
    nigeria_in_progress: int


class ProductionAgentSchema(BaseModel):
    agent: str
    egypt: int
    nigeria: int
    total: int


class ProductionDashboardSchema(BaseModel):
    agents: List[ProductionAgentSchema]
    total_egypt: int
    total_nigeria: int
    total_all: int


# Report Schemas
class ReportSchema(BaseModel):
    report_type: str
    report_date: str
    egypt_todo: int
    egypt_in_progress: int
    nigeria_todo: int
    nigeria_in_progress: int
    content: str
    
    class Config:
        from_attributes = True


# Admin Settings Schemas
class AdminSettingsSchema(BaseModel):
    jira_url: str
    jira_email: str
    jira_api_token: str


class AdminSettingsResponse(BaseModel):
    jira_url: str
    jira_email: str


# Sync Response
class SyncResponseSchema(BaseModel):
    success: bool
    message: str
    issues_synced: int
