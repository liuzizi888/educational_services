"""
员工日常工作Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class DailyReportBase(BaseModel):
    """员工日常工作基础Schema"""
    employee_id: Optional[int] = Field(None, description='员工ID（逻辑外键）')
    report_date: date = Field(..., description='日报日期')
    content: Optional[str] = Field(None, description='结构化后的日报内容')
    work_hours: Optional[Decimal] = Field(None, ge=0, le=24, decimal_places=2, description='工作时长')


class DailyReportCreate(DailyReportBase):
    """创建员工日常工作Schema"""
    pass


class DailyReportUpdate(BaseModel):
    """更新员工日常工作Schema"""
    employee_id: Optional[int] = Field(None, description='员工ID（逻辑外键）')
    report_date: Optional[date] = Field(None, description='日报日期')
    content: Optional[str] = Field(None, description='结构化后的日报内容')
    work_hours: Optional[Decimal] = Field(None, ge=0, le=24, decimal_places=2, description='工作时长')


class DailyReportResponse(BaseModel):
    """员工日常工作响应Schema"""
    report_id: int
    employee_id: Optional[int] = None
    report_date: date
    content: Optional[str] = None
    work_hours: Optional[Decimal] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DailyReportPageResponse(BaseModel):
    """员工日常工作分页响应Schema"""
    items: list[DailyReportResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
