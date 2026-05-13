"""
培训课程Service层
"""
from sqlalchemy.orm import Session
from dao.training_courses_dao import TrainingCoursesDAO
from schemas.training_courses import (
    TrainingCourseCreate,
    TrainingCourseUpdate,
    TrainingCourseResponse,
    TrainingCoursePageResponse
)
from typing import Optional


class TrainingCoursesService:
    """培训课程服务层"""

    @staticmethod
    def create(db: Session, obj: TrainingCourseCreate) -> TrainingCourseResponse:
        """创建课程"""
        obj_data = obj.model_dump()
        course = TrainingCoursesDAO.create(db, obj_data)
        return TrainingCourseResponse.model_validate(course)

    @staticmethod
    def get_by_id(db: Session, course_id: int) -> Optional[TrainingCourseResponse]:
        """根据ID查询课程"""
        course = TrainingCoursesDAO.get_by_id(db, course_id)
        if course:
            return TrainingCourseResponse.model_validate(course)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 course_id: Optional[int] = None,
                 course_name: Optional[str] = None,
                 trainer_name: Optional[str] = None,
                 training_date: Optional[str] = None) -> TrainingCoursePageResponse:
        """分页查询课程"""
        items, total, page, page_size, total_pages = TrainingCoursesDAO.get_page(
            db, page, page_size, course_id, course_name, trainer_name, training_date
        )
        return TrainingCoursePageResponse(
            items=[TrainingCourseResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, course_id: int, obj: TrainingCourseUpdate) -> Optional[TrainingCourseResponse]:
        """更新课程"""
        update_data = obj.model_dump(exclude_unset=True)
        course = TrainingCoursesDAO.update(db, course_id, update_data)
        if course:
            return TrainingCourseResponse.model_validate(course)
        return None

    @staticmethod
    def delete(db: Session, course_id: int) -> bool:
        """删除课程"""
        return TrainingCoursesDAO.delete(db, course_id)
