"""
学生人脸识别与心情预判Service层
"""
from sqlalchemy.orm import Session
from dao.student_photos_dao import StudentPhotosDAO
from schemas.student_photos import (
    StudentPhotoCreate,
    StudentPhotoUpdate,
    StudentPhotoResponse,
    StudentPhotoPageResponse
)
from typing import Optional


class StudentPhotosService:
    """学生人脸识别与心情预判服务层"""

    @staticmethod
    def create(db: Session, obj: StudentPhotoCreate) -> StudentPhotoResponse:
        """创建学生人脸识别记录"""
        obj_data = obj.model_dump()
        photo = StudentPhotosDAO.create(db, obj_data)
        return StudentPhotoResponse.model_validate(photo)

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
                 created_at_end: Optional[str] = None) -> StudentPhotoPageResponse:
        """分页查询学生人脸识别记录"""
        items, total, page, page_size, total_pages = StudentPhotosDAO.get_page(
            db, page, page_size, photo_id, student_id, mood_status, risk_level,
            capture_scene, device_id, sentiment_min, sentiment_max,
            created_at_start, created_at_end
        )
        return StudentPhotoPageResponse(
            items=[StudentPhotoResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, photo_id: int, obj: StudentPhotoUpdate) -> Optional[StudentPhotoResponse]:
        """更新学生人脸识别记录"""
        update_data = obj.model_dump(exclude_unset=True)
        photo = StudentPhotosDAO.update(db, photo_id, update_data)
        if photo:
            return StudentPhotoResponse.model_validate(photo)
        return None

    @staticmethod
    def delete(db: Session, photo_id: int) -> bool:
        """删除学生人脸识别记录"""
        return StudentPhotosDAO.delete(db, photo_id)
