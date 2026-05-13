"""
考试信息Service层
"""
from sqlalchemy.orm import Session
from dao.exams_dao import ExamsDAO
from schemas.exams import (
    ExamCreate,
    ExamUpdate,
    ExamResponse,
    ExamPageResponse
)
from typing import Optional


class ExamsService:
    """考试信息服务层"""

    @staticmethod
    def create(db: Session, obj: ExamCreate) -> ExamResponse:
        """创建考试信息"""
        obj_data = obj.model_dump()
        exam = ExamsDAO.create(db, obj_data)
        return ExamResponse.model_validate(exam)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 exam_id: Optional[int] = None,
                 class_name: Optional[str] = None,
                 subject: Optional[str] = None,
                 exam_name: Optional[str] = None,
                 location: Optional[str] = None,
                 exam_time_start: Optional[str] = None,
                 exam_time_end: Optional[str] = None) -> ExamPageResponse:
        """分页查询考试信息"""
        items, total, page, page_size, total_pages = ExamsDAO.get_page(
            db, page, page_size, exam_id, class_name, subject, exam_name,
            location, exam_time_start, exam_time_end
        )
        return ExamPageResponse(
            items=[ExamResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, exam_id: int, obj: ExamUpdate) -> Optional[ExamResponse]:
        """更新考试信息"""
        update_data = obj.model_dump(exclude_unset=True)
        exam = ExamsDAO.update(db, exam_id, update_data)
        if exam:
            return ExamResponse.model_validate(exam)
        return None

    @staticmethod
    def delete(db: Session, exam_id: int) -> bool:
        """删除考试信息"""
        return ExamsDAO.delete(db, exam_id)
