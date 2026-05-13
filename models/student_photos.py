"""
学生人脸识别与心情预判模型
"""
from sqlalchemy import String, Integer, Text, Enum, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from db.database import Base
import enum


class PhotoRiskLevelEnum(str, enum.Enum):
    green = "green"
    yellow = "yellow"
    orange = "orange"
    red = "red"


class StudentPhotos(Base):
    """学生人脸识别与心情预判记录表"""
    __tablename__ = "t_student_photos"

    photo_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='识别记录ID')
    student_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True, comment='学生ID（逻辑关联）')
    photo_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, comment='抓拍照片存储路径')
    mood_status: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment='识别出的心情状态（开心、平静、焦虑、愤怒、悲伤）')
    risk_level: Mapped[str] = mapped_column(String(20), default='green', comment='风险等级: green-绿色, yellow-黄色, orange-橙色, red-红色')
    sentiment_score: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 2), nullable=True, comment='情绪评分 (-1.0 到 1.0)')
    capture_scene: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='抓拍场景（校门闸机、宿舍门口、教室摄像头）')
    device_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment='抓拍设备编号')
    is_deleted: Mapped[int] = mapped_column(default=0, comment='软删除标识：0-正常，1-删除')
    created_at: Mapped[Optional[datetime]] = mapped_column(default=None)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=None)

    def __repr__(self):
        return f"<StudentPhotos(photo_id={self.photo_id}, student_id={self.student_id}, mood_status={self.mood_status})>"
