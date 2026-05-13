"""
学生聊天记录Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class RiskLevelEnum(str, Enum):
    green = "green"
    yellow = "yellow"
    orange = "orange"
    red = "red"


class StudentChatLogBase(BaseModel):
    """学生聊天记录基础Schema"""
    student_id: int = Field(..., description='学生ID（逻辑外键）')
    message_text: Optional[str] = Field(None, description='聊天内容')
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description='情绪评分 (-1.0 到 1.0)')
    risk_level: Optional[str] = Field('green', description='风险等级: green-绿色, yellow-黄色, orange-橙色, red-红色')
    keywords_detected: Optional[str] = Field(None, max_length=255, description='命中的敏感词')


class StudentChatLogCreate(StudentChatLogBase):
    """创建学生聊天记录Schema"""
    pass


class StudentChatLogUpdate(BaseModel):
    """更新学生聊天记录Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑外键）')
    message_text: Optional[str] = Field(None, description='聊天内容')
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0, description='情绪评分 (-1.0 到 1.0)')
    risk_level: Optional[str] = Field(None, description='风险等级: green-绿色, yellow-黄色, orange-橙色, red-红色')
    keywords_detected: Optional[str] = Field(None, max_length=255, description='命中的敏感词')


class StudentChatLogResponse(BaseModel):
    """学生聊天记录响应Schema"""
    log_id: int
    student_id: int
    message_text: Optional[str] = None
    sentiment_score: Optional[float] = None
    risk_level: str
    keywords_detected: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentChatLogPageResponse(BaseModel):
    """学生聊天记录分页响应Schema"""
    items: list[StudentChatLogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
