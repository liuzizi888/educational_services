"""
每月达成目标模型
"""
from sqlalchemy import String, Integer, Numeric, Date, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from db.database import Base
import enum


class GoalStatusEnum(str, enum.Enum):
    pending = "pending"
    achieved = "achieved"
    failed = "failed"


class MonthlyGoals(Base):
    """每月达成目标表"""
    __tablename__ = "t_monthly_goals"
    
    goal_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='目标ID')
    employee_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='员工ID（逻辑外键）')
    target_month: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment='目标月份')
    target_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment='目标金额/数量')
    actual_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True, comment='实际完成金额/数量')
    achievement_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2), nullable=True, comment='达成率(%)')
    status: Mapped[str] = mapped_column(String(20), default='pending', comment='目标状态:pending-待处理,achieved-已完成,failed-失败')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<MonthlyGoals(goal_id={self.goal_id}, employee_id={self.employee_id}, status={self.status})>"
