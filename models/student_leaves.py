"""
学生请假模型
"""
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class StudentLeaves(Base):
    """学生请假表"""
    __tablename__ = "t_student_leaves"
    
    leave_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='请假ID')
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment='学生ID（逻辑外键）')
    start_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment='请假开始时间')
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment='请假结束时间')
    reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='请假原因')
    status: Mapped[str] = mapped_column(String(20), default='pending', comment='审批状态: pending-待审批, approved-已通过, rejected-已拒绝')
    approver_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment='审批人ID（逻辑外键）')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<StudentLeaves(leave_id={self.leave_id}, student_id={self.student_id}, status={self.status})>"
