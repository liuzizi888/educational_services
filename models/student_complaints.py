"""
学生投诉、建议模型
"""
from sqlalchemy import String, Integer, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class StudentComplaints(Base):
    """学生投诉、建议表"""
    __tablename__ = "t_student_complaints"

    complaint_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='投诉ID')
    student_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='学生ID（逻辑外键）')
    content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='投诉内容')
    type: Mapped[Optional[str]] = mapped_column(SQLEnum('complaints', 'suggestions', name='complaint_type_enum'), nullable=True, comment='类型: complaints-投诉, suggestions-建议')
    status: Mapped[str] = mapped_column(String(20), default='pending', comment='处理状态: pending-待处理, processing-处理中, resolved-已解决, rejected-已拒绝')
    handler_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='处理人(员工ID)（逻辑外键）')
    resolve_remark: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='处理结果反馈')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<StudentComplaints(complaint_id={self.complaint_id}, student_id={self.student_id}, type={self.type})>"
