"""
学生成绩模型
"""
from sqlalchemy import String, Integer, DECIMAL, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from db.database import Base


class StudentGrades(Base):
    """学生成绩表"""
    __tablename__ = "t_student_grades"

    grade_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='成绩ID')
    student_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment='学生ID（逻辑外键）')
    subject: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='科目')
    score: Mapped[Optional[float]] = mapped_column(DECIMAL(5, 2), nullable=True, comment='分数')
    exam_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='考试类型（期中考、期末考等）')
    exam_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment='考试日期')
    teacher_remark: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='教师评语')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<StudentGrades(grade_id={self.grade_id}, student_id={self.student_id}, subject={self.subject}, score={self.score})>"
