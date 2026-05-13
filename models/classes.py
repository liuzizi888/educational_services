"""
班级信息模型
"""
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class Classes(Base):
    """班级信息表"""
    __tablename__ = "t_classes"
    
    class_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='班级ID')
    class_name: Mapped[str] = mapped_column(String(100), nullable=False, comment='班级名称')
    grade_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='年级')
    head_teacher_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='班主任ID（逻辑外键）')
    classroom_location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment='固定教室/地点')
    max_students: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment='班级最大人数')
    current_students: Mapped[int] = mapped_column(default=0, comment='当前在读人数')
    status: Mapped[str] = mapped_column(String(20), default='active', comment='班级状态: active-在读, graduated-已毕业, disbanded-已解散')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<Classes(class_id={self.class_id}, class_name={self.class_name}, status={self.status})>"
