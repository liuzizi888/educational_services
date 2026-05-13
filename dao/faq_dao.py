"""
常见问题DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.faq import Faq
from typing import Optional, Tuple


class FaqDAO:
    """常见问题数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> Faq:
        """创建FAQ"""
        faq = Faq(**obj_data)
        db.add(faq)
        db.commit()
        db.refresh(faq)
        return faq

    @staticmethod
    def get_by_id(db: Session, faq_id: int) -> Optional[Faq]:
        """根据ID查询FAQ"""
        return db.query(Faq).filter(
            and_(
                Faq.faq_id == faq_id,
                Faq.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 faq_id: Optional[int] = None,
                 category: Optional[str] = None,
                 keyword: Optional[str] = None,
                 is_active: Optional[bool] = None) -> Tuple:
        """分页查询FAQ"""
        query = db.query(Faq).filter(Faq.is_deleted == 0)

        if faq_id is not None:
            query = query.filter(Faq.faq_id == faq_id)
        if category:
            query = query.filter(Faq.category == category)
        if keyword:
            query = query.filter(Faq.question.like(f"%{keyword}%"))
        if is_active is not None:
            query = query.filter(Faq.is_active == is_active)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(Faq.sort_order.desc(), Faq.faq_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, faq_id: int, update_data: dict) -> Optional[Faq]:
        """更新FAQ"""
        faq = FaqDAO.get_by_id(db, faq_id)
        if not faq:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(faq, key):
                setattr(faq, key, value)

        db.commit()
        db.refresh(faq)
        return faq

    @staticmethod
    def increment_view_count(db: Session, faq_id: int) -> Optional[Faq]:
        """增加查看次数"""
        faq = FaqDAO.get_by_id(db, faq_id)
        if not faq:
            return None
        faq.view_count += 1
        db.commit()
        db.refresh(faq)
        return faq

    @staticmethod
    def delete(db: Session, faq_id: int) -> bool:
        """删除FAQ（软删除）"""
        faq = FaqDAO.get_by_id(db, faq_id)
        if not faq:
            return False

        faq.is_deleted = 1
        db.commit()
        return True
