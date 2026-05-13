"""
学生投诉、建议Service层
"""
from sqlalchemy.orm import Session
from dao.student_complaints_dao import StudentComplaintsDAO
from schemas.student_complaints import (
    StudentComplaintCreate,
    StudentComplaintUpdate,
    StudentComplaintResponse,
    StudentComplaintPageResponse
)
from typing import Optional


class StudentComplaintsService:
    """学生投诉、建议服务层"""

    @staticmethod
    def create(db: Session, obj: StudentComplaintCreate) -> StudentComplaintResponse:
        """创建学生投诉、建议"""
        obj_data = obj.model_dump()
        complaint = StudentComplaintsDAO.create(db, obj_data)
        return StudentComplaintResponse.model_validate(complaint)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 complaint_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 type: Optional[str] = None,
                 status: Optional[str] = None,
                 handler_id: Optional[int] = None,
                 created_at_start: Optional[str] = None,
                 created_at_end: Optional[str] = None) -> StudentComplaintPageResponse:
        """分页查询学生投诉、建议"""
        items, total, page, page_size, total_pages = StudentComplaintsDAO.get_page(
            db, page, page_size, complaint_id, student_id, type, status, handler_id, created_at_start, created_at_end
        )
        return StudentComplaintPageResponse(
            items=[StudentComplaintResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, complaint_id: int, obj: StudentComplaintUpdate) -> Optional[StudentComplaintResponse]:
        """更新学生投诉、建议"""
        update_data = obj.model_dump(exclude_unset=True)
        complaint = StudentComplaintsDAO.update(db, complaint_id, update_data)
        if complaint:
            return StudentComplaintResponse.model_validate(complaint)
        return None

    @staticmethod
    def delete(db: Session, complaint_id: int) -> bool:
        """删除学生投诉、建议"""
        return StudentComplaintsDAO.delete(db, complaint_id)
