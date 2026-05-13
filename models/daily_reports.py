"""
员工日常工作表模型
"""
from sqlalchemy import String, Integer, Numeric, Date, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from db.database import Base


class DailyReports(Base):
    """员工日常工作表"""
    __tablename__ = "t_daily_reports"
    
    report_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='日报ID')
    employee_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='员工ID（逻辑外键）')
    report_date: Mapped[date] = mapped_column(Date, nullable=False, comment='日报日期')
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='结构化后的日报内容')
    work_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2), nullable=True, comment='工作时长')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<DailyReports(report_id={self.report_id}, employee_id={self.employee_id}, report_date={self.report_date})>"
