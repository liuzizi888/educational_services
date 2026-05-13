"""
考试信息DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.exams import Exams
from typing import Optional, Tuple


class ExamsDAO:
    """考试信息数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> Exams:
        """创建考试信息"""
        exam = Exams(**obj_data)
        db.add(exam)
        db.commit()
        db.refresh(exam)
        return exam

    @staticmethod
    def get_by_id(db: Session, exam_id: int) -> Optional[Exams]:
        """根据ID查询考试信息"""
        return db.query(Exams).filter(
            and_(
                Exams.exam_id == exam_id,
                Exams.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 exam_id: Optional[int] = None,
                 class_name: Optional[str] = None,
                 subject: Optional[str] = None,
                 exam_name: Optional[str] = None,
                 location: Optional[str] = None,
                 exam_time_start: Optional[str] = None,
                 exam_time_end: Optional[str] = None) -> Tuple:
        """分页查询考试信息"""
        query = db.query(Exams).filter(Exams.is_deleted == 0)

        if exam_id is not None:
            query = query.filter(Exams.exam_id == exam_id)
        if class_name:
            query = query.filter(Exams.class_name.like(f"%{class_name}%"))
        if subject:
            query = query.filter(Exams.subject.like(f"%{subject}%"))
        if exam_name:
            query = query.filter(Exams.exam_name.like(f"%{exam_name}%"))
        if location:
            query = query.filter(Exams.location.like(f"%{location}%"))
        if exam_time_start:
            query = query.filter(Exams.exam_time >= exam_time_start)
        if exam_time_end:
            query = query.filter(Exams.exam_time <= exam_time_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Exams.exam_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, exam_id: int, update_data: dict) -> Optional[Exams]:
        """更新考试信息"""
        exam = ExamsDAO.get_by_id(db, exam_id)
        if not exam:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(exam, key):
                setattr(exam, key, value)

        db.commit()
        db.refresh(exam)
        return exam

    @staticmethod
    def delete(db: Session, exam_id: int) -> bool:
        """删除考试信息（软删除）"""
        exam = ExamsDAO.get_by_id(db, exam_id)
        if not exam:
            return False

        exam.is_deleted = 1
        db.commit()
        return True
