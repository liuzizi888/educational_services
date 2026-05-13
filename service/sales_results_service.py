"""
销售成果Service层
"""
from sqlalchemy.orm import Session
from dao.sales_results_dao import SalesResultsDAO
from schemas.sales_results import (
    SalesResultCreate,
    SalesResultUpdate,
    SalesResultResponse,
    SalesResultPageResponse
)
from typing import Optional


class SalesResultsService:
    """销售成果服务层"""

    @staticmethod
    def create(db: Session, obj: SalesResultCreate) -> SalesResultResponse:
        """创建销售成果"""
        obj_data = obj.model_dump()
        result = SalesResultsDAO.create(db, obj_data)
        return SalesResultResponse.model_validate(result)

    @staticmethod
    def get_by_id(db: Session, result_id: int) -> Optional[SalesResultResponse]:
        """根据ID查询销售成果"""
        result = SalesResultsDAO.get_by_id(db, result_id)
        if result:
            return SalesResultResponse.model_validate(result)
        return None

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 result_id: Optional[int] = None,
                 employee_id: Optional[int] = None,
                 client_id: Optional[int] = None,
                 product_type: Optional[str] = None,
                 contract_date_start: Optional[str] = None,
                 contract_date_end: Optional[str] = None) -> SalesResultPageResponse:
        """分页查询销售成果"""
        items, total, page, page_size, total_pages = SalesResultsDAO.get_page(
            db, page, page_size, result_id, employee_id, client_id, product_type, contract_date_start, contract_date_end
        )
        return SalesResultPageResponse(
            items=[SalesResultResponse.model_validate(item) for item in items],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )

    @staticmethod
    def update(db: Session, result_id: int, obj: SalesResultUpdate) -> Optional[SalesResultResponse]:
        """更新销售成果"""
        update_data = obj.model_dump(exclude_unset=True)
        result = SalesResultsDAO.update(db, result_id, update_data)
        if result:
            return SalesResultResponse.model_validate(result)
        return None

    @staticmethod
    def delete(db: Session, result_id: int) -> bool:
        """删除销售成果"""
        return SalesResultsDAO.delete(db, result_id)
