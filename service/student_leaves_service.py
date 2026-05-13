"""
学生请假Service层
"""
from sqlalchemy.orm import Session
from dao.student_leaves_dao import StudentLeavesDAO
from schemas.student_leaves import (
    StudentLeaveCreate,
    StudentLeaveUpdate,
    StudentLeaveResponse,
    StudentLeavePageResponse
)
from typing import Optional


class StudentLeavesService:
    """学生请假服务层"""

    @staticmethod
    def create(db: Session, obj: StudentLeaveCreate) -> StudentLeaveResponse:
        """创建学生请假"""
        obj_data = obj.model_dump()
        leave = StudentLeavesDAO.create(db, obj_data)
        return StudentLeaveResponse.model_validate(leave)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 leave_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 approver_id: Optional[int] = None,
                 status: Optional[str] = None,
                 start_time_start: Optional[str] = None,
                 start_time_end: Optional[str] = None) -> StudentLeavePageResponse:
        """分页查询学生请假"""
        items, total, page, page_size, total_pages = StudentLeavesDAO.get_page(
            db, page, page_size, leave_id, student_id, approver_id, status, start_time_start, start_time_end
        )
        return StudentLeavePageResponse(
            items=[StudentLeaveResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, leave_id: int, obj: StudentLeaveUpdate) -> Optional[StudentLeaveResponse]:
        """更新学生请假"""
        update_data = obj.model_dump(exclude_unset=True)
        leave = StudentLeavesDAO.update(db, leave_id, update_data)
        if leave:
            return StudentLeaveResponse.model_validate(leave)
        return None

    @staticmethod
    def delete(db: Session, leave_id: int) -> bool:
        """删除学生请假"""
        return StudentLeavesDAO.delete(db, leave_id)
