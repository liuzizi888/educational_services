"""
学生投诉、建议Schema定义
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime


class StudentComplaintBase(BaseModel):
    """学生投诉、建议基础Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑外键）')
    content: Optional[str] = Field(None, description='投诉内容')
    type: Optional[Literal['complaints', 'suggestions']] = Field(None, description='类型: complaints-投诉, suggestions-建议')
    status: Optional[Literal['pending', 'processing', 'resolved', 'rejected']] = Field(None, description='处理状态: pending-待处理, processing-处理中, resolved-已解决, rejected-已拒绝')
    handler_id: Optional[int] = Field(None, description='处理人(员工ID)（逻辑外键）')
    resolve_remark: Optional[str] = Field(None, description='处理结果反馈')


class StudentComplaintCreate(StudentComplaintBase):
    """创建学生投诉、建议Schema"""
    pass


class StudentComplaintUpdate(BaseModel):
    """更新学生投诉、建议Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑外键）')
    content: Optional[str] = Field(None, description='投诉内容')
    type: Optional[Literal['complaints', 'suggestions']] = Field(None, description='类型: complaints-投诉, suggestions-建议')
    status: Optional[Literal['pending', 'processing', 'resolved', 'rejected']] = Field(None, description='处理状态: pending-待处理, processing-处理中, resolved-已解决, rejected-已拒绝')
    handler_id: Optional[int] = Field(None, description='处理人(员工ID)（逻辑外键）')
    resolve_remark: Optional[str] = Field(None, description='处理结果反馈')


class StudentComplaintResponse(BaseModel):
    """学生投诉、建议响应Schema"""
    complaint_id: int
    student_id: Optional[int] = None
    content: Optional[str] = None
    type: Optional[str] = None
    status: str
    handler_id: Optional[int] = None
    resolve_remark: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentComplaintPageResponse(BaseModel):
    """学生投诉、建议分页响应Schema"""
    items: list[StudentComplaintResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
