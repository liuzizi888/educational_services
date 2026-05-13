"""
考试信息模型
"""
from sqlalchemy import String, Integer, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class Exams(Base):
    """考试信息表"""
    __tablename__ = "t_exams"

    exam_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='考试ID')
    class_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='适用班级')
    subject: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='科目')
    exam_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='考试名称')
    exam_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment='考试时间点')
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='考试地点')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<Exams(exam_id={self.exam_id}, exam_name={self.exam_name}, subject={self.subject})>"
