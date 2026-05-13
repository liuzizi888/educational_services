"""
学生人脸识别模型
"""
from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base


class StudentFaceRecords(Base):
    """学生人脸识别表"""
    __tablename__ = "t_student_face_records"
    
    face_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='人脸记录ID')
    student_id: Mapped[int] = mapped_column(Integer, nullable=False, comment='学生ID（逻辑外键）')
    face_feature_data: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment='人脸特征向量数据')
    photo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='人脸照片存储路径')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除：0-未删除，1-已删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<StudentFaceRecords(face_id={self.face_id}, student_id={self.student_id})>"
