"""
学生信息DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.students import Students
from typing import Optional, Tuple


class StudentsDAO:
    """学生信息数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> Students:
        """创建学生信息"""
        student = Students(**obj_data)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def get_by_id(db: Session, student_id: int) -> Optional[Students]:
        """根据ID查询学生信息"""
        return db.query(Students).filter(
            and_(
                Students.student_id == student_id,
                Students.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 student_id: Optional[int] = None,
                 class_id: Optional[int] = None,
                 name: Optional[str] = None,
                 status: Optional[str] = None,
                 enrollment_date_start: Optional[str] = None,
                 enrollment_date_end: Optional[str] = None) -> Tuple:
        """分页查询学生信息"""
        query = db.query(Students).filter(Students.is_deleted == 0)

        if student_id is not None:
            query = query.filter(Students.student_id == student_id)
        if class_id is not None:
            query = query.filter(Students.class_id == class_id)
        if name:
            query = query.filter(Students.name.like(f"%{name}%"))
        if status:
            query = query.filter(Students.status == status)
        if enrollment_date_start:
            query = query.filter(Students.enrollment_date >= enrollment_date_start)
        if enrollment_date_end:
            query = query.filter(Students.enrollment_date <= enrollment_date_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Students.student_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, student_id: int, update_data: dict) -> Optional[Students]:
        """更新学生信息"""
        student = StudentsDAO.get_by_id(db, student_id)
        if not student:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(student, key):
                setattr(student, key, value)

        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def delete(db: Session, student_id: int) -> bool:
        """删除学生信息（软删除）"""
        student = StudentsDAO.get_by_id(db, student_id)
        if not student:
            return False

        student.is_deleted = 1
        db.commit()
        return True
