"""
学生信息Service层
"""
from sqlalchemy.orm import Session
from dao.students_dao import StudentsDAO
from schemas.students import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
    StudentPageResponse
)
from typing import Optional


class StudentsService:
    """学生信息服务层"""

    @staticmethod
    def create(db: Session, obj: StudentCreate) -> StudentResponse:
        """创建学生信息"""
        obj_data = obj.model_dump()
        student = StudentsDAO.create(db, obj_data)
        return StudentResponse.model_validate(student)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 student_id: Optional[int] = None,
                 class_id: Optional[int] = None,
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 enrollment_date_start: Optional[str] = None,
                 enrollment_date_end: Optional[str] = None) -> StudentPageResponse:
        """分页查询学生信息"""
        items, total, page, page_size, total_pages = StudentsDAO.get_page(
            db, page, page_size, student_id, class_id, name, status, enrollment_date_start, enrollment_date_end
        )
        return StudentPageResponse(
            items=[StudentResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, student_id: int, obj: StudentUpdate) -> Optional[StudentResponse]:
        """更新学生信息"""
        update_data = obj.model_dump(exclude_unset=True)
        student = StudentsDAO.update(db, student_id, update_data)
        if student:
            return StudentResponse.model_validate(student)
        return None

    @staticmethod
    def delete(db: Session, student_id: int) -> bool:
        """删除学生信息"""
        return StudentsDAO.delete(db, student_id)
