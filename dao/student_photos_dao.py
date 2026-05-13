"""
学生人脸识别与心情预判DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.student_photos import StudentPhotos
from typing import Optional, Tuple


class StudentPhotosDAO:
    """学生人脸识别与心情预判数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> StudentPhotos:
        """创建学生人脸识别记录"""
        photo = StudentPhotos(**obj_data)
        db.add(photo)
        db.commit()
        db.refresh(photo)
        return photo

    @staticmethod
    def get_by_id(db: Session, photo_id: int) -> Optional[StudentPhotos]:
        """根据ID查询学生人脸识别记录"""
        return db.query(StudentPhotos).filter(
            and_(
                StudentPhotos.photo_id == photo_id,
                StudentPhotos.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 photo_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 mood_status: Optional[str] = None,
                 risk_level: Optional[str] = None,
                 capture_scene: Optional[str] = None,
                 device_id: Optional[str] = None,
                 sentiment_min: Optional[float] = None,
                 sentiment_max: Optional[float] = None,
                 created_at_start: Optional[str] = None,
                 created_at_end: Optional[str] = None) -> Tuple:
        """分页查询学生人脸识别记录"""
        query = db.query(StudentPhotos).filter(StudentPhotos.is_deleted == 0)

        if photo_id is not None:
            query = query.filter(StudentPhotos.photo_id == photo_id)
        if student_id is not None:
            query = query.filter(StudentPhotos.student_id == student_id)
        if mood_status:
            query = query.filter(StudentPhotos.mood_status == mood_status)
        if risk_level:
            query = query.filter(StudentPhotos.risk_level == risk_level)
        if capture_scene:
            query = query.filter(StudentPhotos.capture_scene.like(f"%{capture_scene}%"))
        if device_id:
            query = query.filter(StudentPhotos.device_id == device_id)
        if sentiment_min is not None:
            query = query.filter(StudentPhotos.sentiment_score >= sentiment_min)
        if sentiment_max is not None:
            query = query.filter(StudentPhotos.sentiment_score <= sentiment_max)
        if created_at_start:
            query = query.filter(StudentPhotos.created_at >= created_at_start)
        if created_at_end:
            query = query.filter(StudentPhotos.created_at <= created_at_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(StudentPhotos.photo_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, photo_id: int, update_data: dict) -> Optional[StudentPhotos]:
        """更新学生人脸识别记录"""
        photo = StudentPhotosDAO.get_by_id(db, photo_id)
        if not photo:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(photo, key):
                setattr(photo, key, value)

        db.commit()
        db.refresh(photo)
        return photo

    @staticmethod
    def delete(db: Session, photo_id: int) -> bool:
        """删除学生人脸识别记录（软删除）"""
        photo = StudentPhotosDAO.get_by_id(db, photo_id)
        if not photo:
            return False

        photo.is_deleted = 1
        db.commit()
        return True
