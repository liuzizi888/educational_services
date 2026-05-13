"""
学生信息模型
"""
from sqlalchemy import String, Integer, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, date
from typing import Optional
from db.database import Base
import enum


class StudentGenderEnum(str, enum.Enum):
    M = "M"
    F = "F"


class StudentStatusEnum(str, enum.Enum):
    enrolled = "enrolled"
    graduated = "graduated"
    withdrawn = "withdrawn"


class Students(Base):
    """学生信息表"""
    __tablename__ = "t_students"
    
    student_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='学生ID')
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment='学生姓名')
    gender: Mapped[Optional[str]] = mapped_column(String(1), nullable=True, comment='性别 M-男, F-女')
    dob: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment='出生日期')
    class_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, index=True, comment='所在班级ID（逻辑外键）')
    email: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='学生邮箱')
    parent_contact: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='家长联系方式')
    enrollment_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True, comment='入学日期')
    status: Mapped[str] = mapped_column(String(20), default='enrolled', comment='学籍状态: enrolled-已注册, graduated-已毕业, withdrawn-已退学')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<Students(student_id={self.student_id}, name={self.name}, status={self.status})>"
