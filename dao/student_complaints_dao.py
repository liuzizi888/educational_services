"""
学生投诉、建议DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.student_complaints import StudentComplaints
from typing import Optional, Tuple


class StudentComplaintsDAO:
    """学生投诉、建议数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> StudentComplaints:
        """创建学生投诉、建议"""
        complaint = StudentComplaints(**obj_data)
        db.add(complaint)
        db.commit()
        db.refresh(complaint)
        return complaint

    @staticmethod
    def get_by_id(db: Session, complaint_id: int) -> Optional[StudentComplaints]:
        """根据ID查询学生投诉、建议"""
        return db.query(StudentComplaints).filter(
            and_(
                StudentComplaints.complaint_id == complaint_id,
                StudentComplaints.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 complaint_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 type: Optional[str] = None,
                 status: Optional[str] = None,
                 handler_id: Optional[int] = None,
                 created_at_start: Optional[str] = None,
                 created_at_end: Optional[str] = None) -> Tuple:
        """分页查询学生投诉、建议"""
        query = db.query(StudentComplaints).filter(StudentComplaints.is_deleted == 0)

        if complaint_id is not None:
            query = query.filter(StudentComplaints.complaint_id == complaint_id)
        if student_id is not None:
            query = query.filter(StudentComplaints.student_id == student_id)
        if type:
            query = query.filter(StudentComplaints.type == type)
        if status:
            query = query.filter(StudentComplaints.status == status)
        if handler_id is not None:
            query = query.filter(StudentComplaints.handler_id == handler_id)
        if created_at_start:
            query = query.filter(StudentComplaints.created_at >= created_at_start)
        if created_at_end:
            query = query.filter(StudentComplaints.created_at <= created_at_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(StudentComplaints.complaint_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, complaint_id: int, update_data: dict) -> Optional[StudentComplaints]:
        """更新学生投诉、建议"""
        complaint = StudentComplaintsDAO.get_by_id(db, complaint_id)
        if not complaint:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(complaint, key):
                setattr(complaint, key, value)

        db.commit()
        db.refresh(complaint)
        return complaint

    @staticmethod
    def delete(db: Session, complaint_id: int) -> bool:
        """删除学生投诉、建议（软删除）"""
        complaint = StudentComplaintsDAO.get_by_id(db, complaint_id)
        if not complaint:
            return False

        complaint.is_deleted = 1
        db.commit()
        return True
