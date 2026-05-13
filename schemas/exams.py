"""
考试信息Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ExamBase(BaseModel):
    """考试信息基础Schema"""
    class_name: Optional[str] = Field(None, max_length=50, description='适用班级')
    subject: Optional[str] = Field(None, max_length=100, description='科目')
    exam_name: Optional[str] = Field(None, max_length=100, description='考试名称')
    exam_time: Optional[datetime] = Field(None, description='考试时间点')
    location: Optional[str] = Field(None, max_length=255, description='考试地点')


class ExamCreate(ExamBase):
    """创建考试信息Schema"""
    pass


class ExamUpdate(BaseModel):
    """更新考试信息Schema"""
    class_name: Optional[str] = Field(None, max_length=50, description='适用班级')
    subject: Optional[str] = Field(None, max_length=100, description='科目')
    exam_name: Optional[str] = Field(None, max_length=100, description='考试名称')
    exam_time: Optional[datetime] = Field(None, description='考试时间点')
    location: Optional[str] = Field(None, max_length=255, description='考试地点')


class ExamResponse(BaseModel):
    """考试信息响应Schema"""
    exam_id: int
    class_name: Optional[str] = None
    subject: Optional[str] = None
    exam_name: Optional[str] = None
    exam_time: Optional[datetime] = None
    location: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ExamPageResponse(BaseModel):
    """考试信息分页响应Schema"""
    items: list[ExamResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
