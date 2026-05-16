"""
学生请假Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class LeaveStatusEnum(str, Enum):
    """请假状态枚举"""
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class StudentLeaveBase(BaseModel):
    """学生请假基础Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑外键）')
    start_time: Optional[datetime] = Field(None, description='请假开始时间')
    end_time: Optional[datetime] = Field(None, description='请假结束时间')
    reason: Optional[str] = Field(None, description='请假原因')
    status: Optional[LeaveStatusEnum] = Field(None, description='审批状态: pending-待审批, approved-已通过, rejected-已拒绝')
    approver_id: Optional[int] = Field(None, description='审批人ID（逻辑外键）')


class StudentLeaveCreate(StudentLeaveBase):
    """创建学生请假Schema"""
    pass


class StudentLeaveUpdate(BaseModel):
    """更新学生请假Schema"""
    student_id: Optional[int] = Field(None, description='学生ID（逻辑外键）')
    start_time: Optional[datetime] = Field(None, description='请假开始时间')
    end_time: Optional[datetime] = Field(None, description='请假结束时间')
    reason: Optional[str] = Field(None, description='请假原因')
    status: Optional[LeaveStatusEnum] = Field(None, description='审批状态: pending-待审批, approved-已通过, rejected-已拒绝')
    approver_id: Optional[int] = Field(None, description='审批人ID（逻辑外键）')


class StudentLeaveResponse(BaseModel):
    """学生请假响应Schema"""
    leave_id: int
    student_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    reason: Optional[str] = None
    status: LeaveStatusEnum
    approver_id: Optional[int] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudentLeavePageResponse(BaseModel):
    """学生请假分页响应Schema"""
    items: list[StudentLeaveResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
