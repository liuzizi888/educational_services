"""
培训课程模型
"""
from sqlalchemy import String, Text, Integer, Date, Time
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date, time
from typing import Optional
from db.database import Base


class TrainingCourses(Base):
    """培训课程表"""
    __tablename__ = "t_training_courses"
    
    course_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    course_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='课程名称')
    trainer_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='培训讲师')
    target_audience: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='培训对象')
    training_room: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='培训教室/线上链接')
    training_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment='培训日期')
    start_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True, comment='开始时间')
    end_time: Mapped[Optional[time]] = mapped_column(Time, nullable=True, comment='结束时间')
    course_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='课程内容')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<TrainingCourses(course_id={self.course_id}, course_name={self.course_name})>"
