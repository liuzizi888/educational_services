"""
常见问题Service层
"""
from sqlalchemy.orm import Session
from dao.faq_dao import FaqDAO
from schemas.faq import FaqCreate, FaqUpdate, FaqResponse, FaqPageResponse
from typing import Optional


class FaqService:
    """常见问题服务层"""

    @staticmethod
    def create(db: Session, obj: FaqCreate) -> FaqResponse:
        """创建FAQ"""
        obj_data = obj.model_dump()
        faq = FaqDAO.create(db, obj_data)
        return FaqResponse.model_validate(faq)

    @staticmethod
    def get_by_id(db: Session, faq_id: int) -> Optional[FaqResponse]:
        """根据ID查询FAQ"""
        faq = FaqDAO.get_by_id(db, faq_id)
        if faq:
            return FaqResponse.model_validate(faq)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 faq_id: Optional[int] = None,
                 category: Optional[str] = None,
                 keyword: Optional[str] = None,
                 is_active: Optional[bool] = None) -> FaqPageResponse:
        """分页查询FAQ"""
        items, total, page, page_size, total_pages = FaqDAO.get_page(
            db, page, page_size, faq_id, category, keyword, is_active
        )
        return FaqPageResponse(
            items=[FaqResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, faq_id: int, obj: FaqUpdate) -> Optional[FaqResponse]:
        """更新FAQ"""
        update_data = obj.model_dump(exclude_unset=True)
        faq = FaqDAO.update(db, faq_id, update_data)
        if faq:
            return FaqResponse.model_validate(faq)
        return None

    @staticmethod
    def increment_view(db: Session, faq_id: int) -> Optional[FaqResponse]:
        """增加查看次数"""
        faq = FaqDAO.increment_view_count(db, faq_id)
        if faq:
            return FaqResponse.model_validate(faq)
        return None

    @staticmethod
    def delete(db: Session, faq_id: int) -> bool:
        """删除FAQ"""
        return FaqDAO.delete(db, faq_id)
