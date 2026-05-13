"""
班级信息DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.classes import Classes
from typing import Optional, Tuple


class ClassesDAO:
    """班级信息数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> Classes:
        """创建班级信息"""
        class_obj = Classes(**obj_data)
        db.add(class_obj)
        db.commit()
        db.refresh(class_obj)
        return class_obj

    @staticmethod
    def get_by_id(db: Session, class_id: int) -> Optional[Classes]:
        """根据ID查询班级信息"""
        return db.query(Classes).filter(
            and_(
                Classes.class_id == class_id,
                Classes.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 class_id: Optional[int] = None,
                 class_name: Optional[str] = None,
                 grade_level: Optional[str] = None,
                 head_teacher_id: Optional[int] = None,
                 status: Optional[str] = None) -> Tuple:
        """分页查询班级信息"""
        query = db.query(Classes).filter(Classes.is_deleted == 0)

        if class_id is not None:
            query = query.filter(Classes.class_id == class_id)
        if class_name:
            query = query.filter(Classes.class_name.like(f"%{class_name}%"))
        if grade_level:
            query = query.filter(Classes.grade_level == grade_level)
        if head_teacher_id is not None:
            query = query.filter(Classes.head_teacher_id == head_teacher_id)
        if status:
            query = query.filter(Classes.status == status)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Classes.class_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, class_id: int, update_data: dict) -> Optional[Classes]:
        """更新班级信息"""
        class_obj = ClassesDAO.get_by_id(db, class_id)
        if not class_obj:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(class_obj, key):
                setattr(class_obj, key, value)

        db.commit()
        db.refresh(class_obj)
        return class_obj

    @staticmethod
    def delete(db: Session, class_id: int) -> bool:
        """删除班级信息（软删除）"""
        class_obj = ClassesDAO.get_by_id(db, class_id)
        if not class_obj:
            return False

        class_obj.is_deleted = 1
        db.commit()
        return True
