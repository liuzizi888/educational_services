"""
学生请假DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.student_leaves import StudentLeaves
from typing import Optional, Tuple


class StudentLeavesDAO:
    """学生请假数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> StudentLeaves:
        """创建学生请假"""
        leave = StudentLeaves(**obj_data)
        db.add(leave)
        db.commit()
        db.refresh(leave)
        return leave

    @staticmethod
    def get_by_id(db: Session, leave_id: int) -> Optional[StudentLeaves]:
        """根据ID查询学生请假"""
        return db.query(StudentLeaves).filter(
            and_(
                StudentLeaves.leave_id == leave_id,
                StudentLeaves.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 leave_id: Optional[int] = None,
                 student_id: Optional[int] = None,
                 approver_id: Optional[int] = None,
                 status: Optional[str] = None,
                 start_time_start: Optional[str] = None,
                 start_time_end: Optional[str] = None) -> Tuple:
        """分页查询学生请假"""
        query = db.query(StudentLeaves).filter(StudentLeaves.is_deleted == 0)

        if leave_id is not None:
            query = query.filter(StudentLeaves.leave_id == leave_id)
        if student_id is not None:
            query = query.filter(StudentLeaves.student_id == student_id)
        if approver_id is not None:
            query = query.filter(StudentLeaves.approver_id == approver_id)
        if status:
            query = query.filter(StudentLeaves.status == status)
        if start_time_start:
            query = query.filter(StudentLeaves.start_time >= start_time_start)
        if start_time_end:
            query = query.filter(StudentLeaves.start_time <= start_time_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(StudentLeaves.leave_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, leave_id: int, update_data: dict) -> Optional[StudentLeaves]:
        """更新学生请假"""
        leave = StudentLeavesDAO.get_by_id(db, leave_id)
        if not leave:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(leave, key):
                setattr(leave, key, value)

        db.commit()
        db.refresh(leave)
        return leave

    @staticmethod
    def delete(db: Session, leave_id: int) -> bool:
        """删除学生请假（软删除）"""
        leave = StudentLeavesDAO.get_by_id(db, leave_id)
        if not leave:
            return False

        leave.is_deleted = 1
        db.commit()
        return True
