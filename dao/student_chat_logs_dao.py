"""
学生聊天记录DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.student_chat_logs import StudentChatLogs
from typing import Optional, Tuple


class StudentChatLogsDAO:
    """学生聊天记录数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> StudentChatLogs:
        """创建学生聊天记录"""
        chat_log = StudentChatLogs(**obj_data)
        db.add(chat_log)
        db.commit()
        db.refresh(chat_log)
        return chat_log

    @staticmethod
    def get_by_id(db: Session, log_id: int) -> Optional[StudentChatLogs]:
        """根据ID查询学生聊天记录"""
        return db.query(StudentChatLogs).filter(
            and_(
                StudentChatLogs.log_id == log_id,
                StudentChatLogs.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 log_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 risk_level: Optional[str] = None,
                 keywords: Optional[str] = None,
                 sentiment_min: Optional[float] = None,
                 sentiment_max: Optional[float] = None,
                 created_at_start: Optional[str] = None,
                 created_at_end: Optional[str] = None) -> Tuple:
        """分页查询学生聊天记录"""
        query = db.query(StudentChatLogs).filter(StudentChatLogs.is_deleted == 0)

        if log_id is not None:
            query = query.filter(StudentChatLogs.log_id == log_id)
        if student_id is not None:
            query = query.filter(StudentChatLogs.student_id == student_id)
        if risk_level:
            query = query.filter(StudentChatLogs.risk_level == risk_level)
        if keywords:
            query = query.filter(StudentChatLogs.keywords_detected.like(f"%{keywords}%"))
        if sentiment_min is not None:
            query = query.filter(StudentChatLogs.sentiment_score >= sentiment_min)
        if sentiment_max is not None:
            query = query.filter(StudentChatLogs.sentiment_score <= sentiment_max)
        if created_at_start:
            query = query.filter(StudentChatLogs.created_at >= created_at_start)
        if created_at_end:
            query = query.filter(StudentChatLogs.created_at <= created_at_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(StudentChatLogs.log_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, log_id: int, update_data: dict) -> Optional[StudentChatLogs]:
        """更新学生聊天记录"""
        chat_log = StudentChatLogsDAO.get_by_id(db, log_id)
        if not chat_log:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(chat_log, key):
                setattr(chat_log, key, value)

        db.commit()
        db.refresh(chat_log)
        return chat_log

    @staticmethod
    def delete(db: Session, log_id: int) -> bool:
        """删除学生聊天记录（软删除）"""
        chat_log = StudentChatLogsDAO.get_by_id(db, log_id)
        if not chat_log:
            return False

        chat_log.is_deleted = 1
        db.commit()
        return True
