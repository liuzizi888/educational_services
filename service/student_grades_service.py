"""
学生成绩Service层
"""
from sqlalchemy.orm import Session
from dao.student_grades_dao import StudentGradesDAO
from schemas.student_grades import (
    StudentGradeCreate,
    StudentGradeUpdate,
    StudentGradeResponse,
    StudentGradePageResponse
)
from typing import Optional


class StudentGradesService:
    """学生成绩服务层"""

    @staticmethod
    def create(db: Session, obj: StudentGradeCreate) -> StudentGradeResponse:
        """创建学生成绩"""
        obj_data = obj.model_dump()
        grade = StudentGradesDAO.create(db, obj_data)
        return StudentGradeResponse.model_validate(grade)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 grade_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 subject: Optional[str] = None,
                 exam_type: Optional[str] = None,
                 score_min: Optional[float] = None,
                 score_max: Optional[float] = None,
                 exam_date_start: Optional[str] = None,
                 exam_date_end: Optional[str] = None) -> StudentGradePageResponse:
        """分页查询学生成绩"""
        items, total, page, page_size, total_pages = StudentGradesDAO.get_page(
            db, page, page_size, grade_id, student_id, subject, exam_type,
            score_min, score_max, exam_date_start, exam_date_end
        )
        return StudentGradePageResponse(
            items=[StudentGradeResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, grade_id: int, obj: StudentGradeUpdate) -> Optional[StudentGradeResponse]:
        """更新学生成绩"""
        update_data = obj.model_dump(exclude_unset=True)
        grade = StudentGradesDAO.update(db, grade_id, update_data)
        if grade:
            return StudentGradeResponse.model_validate(grade)
        return None

    @staticmethod
    def delete(db: Session, grade_id: int) -> bool:
        """删除学生成绩"""
        return StudentGradesDAO.delete(db, grade_id)
