"""
海外生活知识库Service层
"""
from sqlalchemy.orm import Session
from dao.knowledge_base_overseas_dao import KnowledgeBaseOverseasDAO
from schemas.knowledge_base_overseas import (
    KnowledgeBaseOverseasCreate,
    KnowledgeBaseOverseasUpdate,
    KnowledgeBaseOverseasResponse,
    KnowledgeBaseOverseasPageResponse
)
from typing import Optional


class KnowledgeBaseOverseasService:
    """海外生活知识库服务层"""

    @staticmethod
    def create(db: Session, obj: KnowledgeBaseOverseasCreate) -> KnowledgeBaseOverseasResponse:
        """创建海外生活知识库"""
        obj_data = obj.model_dump()
        kb = KnowledgeBaseOverseasDAO.create(db, obj_data)
        return KnowledgeBaseOverseasResponse.model_validate(kb)

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 kb_id: Optional[int] = None,
                 country: Optional[str] = None,
                 category: Optional[str] = None,
                 question: Optional[str] = None,
                 keywords: Optional[str] = None,
                 updated_by: Optional[int] = None) -> KnowledgeBaseOverseasPageResponse:
        """分页查询海外生活知识库"""
        items, total, page, page_size, total_pages = KnowledgeBaseOverseasDAO.get_page(
            db, page, page_size, kb_id, country, category, question, keywords, updated_by
        )
        return KnowledgeBaseOverseasPageResponse(
            items=[KnowledgeBaseOverseasResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, kb_id: int, obj: KnowledgeBaseOverseasUpdate) -> Optional[KnowledgeBaseOverseasResponse]:
        """更新海外生活知识库"""
        update_data = obj.model_dump(exclude_unset=True)
        kb = KnowledgeBaseOverseasDAO.update(db, kb_id, update_data)
        if kb:
            return KnowledgeBaseOverseasResponse.model_validate(kb)
        return None

    @staticmethod
    def delete(db: Session, kb_id: int) -> bool:
        """删除海外生活知识库"""
        return KnowledgeBaseOverseasDAO.delete(db, kb_id)
