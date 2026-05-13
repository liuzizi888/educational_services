"""
学生聊天记录Service层
"""
from sqlalchemy.orm import Session
from dao.student_chat_logs_dao import StudentChatLogsDAO
from schemas.student_chat_logs import (
    StudentChatLogCreate,
    StudentChatLogUpdate,
    StudentChatLogResponse,
    StudentChatLogPageResponse
)
from typing import Optional


class StudentChatLogsService:
    """学生聊天记录服务层"""

    @staticmethod
    def create(db: Session, obj: StudentChatLogCreate) -> StudentChatLogResponse:
        """创建学生聊天记录"""
        obj_data = obj.model_dump()
        chat_log = StudentChatLogsDAO.create(db, obj_data)
        return StudentChatLogResponse.model_validate(chat_log)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 log_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 risk_level: Optional[str] = None,
                 keywords: Optional[str] = None,
                 sentiment_min: Optional[float] = None,
                 sentiment_max: Optional[float] = None,
                 created_at_start: Optional[str] = None,
                 created_at_end: Optional[str] = None) -> StudentChatLogPageResponse:
        """分页查询学生聊天记录"""
        items, total, page, page_size, total_pages = StudentChatLogsDAO.get_page(
            db, page, page_size, log_id, student_id, risk_level, keywords,
            sentiment_min, sentiment_max, created_at_start, created_at_end
        )
        return StudentChatLogPageResponse(
            items=[StudentChatLogResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, log_id: int, obj: StudentChatLogUpdate) -> Optional[StudentChatLogResponse]:
        """更新学生聊天记录"""
        update_data = obj.model_dump(exclude_unset=True)
        chat_log = StudentChatLogsDAO.update(db, log_id, update_data)
        if chat_log:
            return StudentChatLogResponse.model_validate(chat_log)
        return None

    @staticmethod
    def delete(db: Session, log_id: int) -> bool:
        """删除学生聊天记录"""
        return StudentChatLogsDAO.delete(db, log_id)
