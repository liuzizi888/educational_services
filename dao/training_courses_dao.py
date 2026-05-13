"""
培训课程DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.training_courses import TrainingCourses
from typing import Optional, Tuple


class TrainingCoursesDAO:
    """培训课程数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> TrainingCourses:
        """创建课程"""
        course = TrainingCourses(**obj_data)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def get_by_id(db: Session, course_id: int) -> Optional[TrainingCourses]:
        """根据ID查询课程"""
        return db.query(TrainingCourses).filter(
            and_(
                TrainingCourses.course_id == course_id,
                TrainingCourses.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 course_id: Optional[int] = None,
                 course_name: Optional[str] = None,
                 trainer_name: Optional[str] = None,
                 training_date: Optional[str] = None) -> Tuple:
        """分页查询课程"""
        query = db.query(TrainingCourses).filter(TrainingCourses.is_deleted == 0)

        if course_id is not None:
            query = query.filter(TrainingCourses.course_id == course_id)
        if course_name:
            query = query.filter(TrainingCourses.course_name.like(f"%{course_name}%"))
        if trainer_name:
            query = query.filter(TrainingCourses.trainer_name.like(f"%{trainer_name}%"))
        if training_date:
            query = query.filter(TrainingCourses.training_date == training_date)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(TrainingCourses.course_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, course_id: int, update_data: dict) -> Optional[TrainingCourses]:
        """更新课程"""
        course = TrainingCoursesDAO.get_by_id(db, course_id)
        if not course:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(course, key):
                setattr(course, key, value)

        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete(db: Session, course_id: int) -> bool:
        """删除课程（软删除）"""
        course = TrainingCoursesDAO.get_by_id(db, course_id)
        if not course:
            return False

        course.is_deleted = 1
        db.commit()
        return True
