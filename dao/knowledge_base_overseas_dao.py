"""
海外生活知识库DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.knowledge_base_overseas import KnowledgeBaseOverseas
from typing import Optional, Tuple


class KnowledgeBaseOverseasDAO:
    """海外生活知识库数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> KnowledgeBaseOverseas:
        """创建海外生活知识库"""
        kb = KnowledgeBaseOverseas(**obj_data)
        db.add(kb)
        db.commit()
        db.refresh(kb)
        return kb

    @staticmethod
    def get_by_id(db: Session, kb_id: int) -> Optional[KnowledgeBaseOverseas]:
        """根据ID查询海外生活知识库"""
        return db.query(KnowledgeBaseOverseas).filter(
            and_(
                KnowledgeBaseOverseas.kb_id == kb_id,
                KnowledgeBaseOverseas.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 kb_id: Optional[int] = None,
                 country: Optional[str] = None,
                 category: Optional[str] = None,
                 question: Optional[str] = None,
                 keywords: Optional[str] = None,
                 updated_by: Optional[int] = None) -> Tuple:
        """分页查询海外生活知识库"""
        query = db.query(KnowledgeBaseOverseas).filter(KnowledgeBaseOverseas.is_deleted == 0)

        if kb_id is not None:
            query = query.filter(KnowledgeBaseOverseas.kb_id == kb_id)
        if country:
            query = query.filter(KnowledgeBaseOverseas.country.like(f"%{country}%"))
        if category:
            query = query.filter(KnowledgeBaseOverseas.category.like(f"%{category}%"))
        if question:
            query = query.filter(KnowledgeBaseOverseas.question.like(f"%{question}%"))
        if keywords:
            query = query.filter(KnowledgeBaseOverseas.keywords.like(f"%{keywords}%"))
        if updated_by is not None:
            query = query.filter(KnowledgeBaseOverseas.updated_by == updated_by)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(KnowledgeBaseOverseas.kb_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, kb_id: int, update_data: dict) -> Optional[KnowledgeBaseOverseas]:
        """更新海外生活知识库"""
        kb = KnowledgeBaseOverseasDAO.get_by_id(db, kb_id)
        if not kb:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(kb, key):
                setattr(kb, key, value)

        db.commit()
        db.refresh(kb)
        return kb

    @staticmethod
    def delete(db: Session, kb_id: int) -> bool:
        """删除海外生活知识库（软删除）"""
        kb = KnowledgeBaseOverseasDAO.get_by_id(db, kb_id)
        if not kb:
            return False

        kb.is_deleted = 1
        db.commit()
        return True
