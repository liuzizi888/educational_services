"""
每月达成目标Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from decimal import Decimal


class MonthlyGoalBase(BaseModel):
    """每月达成目标基础Schema"""
    employee_id: int = Field(..., description='员工ID（逻辑外键）')
    target_month: Optional[date] = Field(None, description='目标月份')
    target_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description='目标金额/数量')
    actual_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description='实际完成金额/数量')
    achievement_rate: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2, description='达成率(%)')
    status: Optional[str] = Field(None, description='目标状态: pending-待处理, achieved-已完成, failed-失败')


class MonthlyGoalCreate(MonthlyGoalBase):
    """创建每月达成目标Schema"""
    pass


class MonthlyGoalUpdate(BaseModel):
    """更新每月达成目标Schema"""
    employee_id: Optional[int] = Field(None, description='员工ID（逻辑外键）')
    target_month: Optional[date] = Field(None, description='目标月份')
    target_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description='目标金额/数量')
    actual_amount: Optional[Decimal] = Field(None, ge=0, decimal_places=2, description='实际完成金额/数量')
    achievement_rate: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2, description='达成率(%)')
    status: Optional[str] = Field(None, description='目标状态: pending-待处理, achieved-已完成, failed-失败')


class MonthlyGoalResponse(BaseModel):
    """每月达成目标响应Schema"""
    goal_id: int
    employee_id: int
    target_month: Optional[date] = None
    target_amount: Optional[Decimal] = None
    actual_amount: Optional[Decimal] = None
    achievement_rate: Optional[Decimal] = None
    status: str
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class MonthlyGoalPageResponse(BaseModel):
    """每月达成目标分页响应Schema"""
    items: list[MonthlyGoalResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
