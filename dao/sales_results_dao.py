"""
销售成果DAO层
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.sales_results import SalesResults
from typing import Optional, Tuple


class SalesResultsDAO:
    """销售成果数据访问对象"""

    @staticmethod
    def create(db: Session, obj_data: dict) -> SalesResults:
        """创建销售成果"""
        result = SalesResults(**obj_data)
        db.add(result)
        db.commit()
        db.refresh(result)
        return result

    @staticmethod
    def get_by_id(db: Session, result_id: int) -> Optional[SalesResults]:
        """根据ID查询销售成果"""
        return db.query(SalesResults).filter(
            and_(
                SalesResults.result_id == result_id,
                SalesResults.is_deleted == 0
            )
        ).first()

    @staticmethod
    def get_page(db: Session, page: int = 1, page_size: int = 10,
                 result_id: Optional[int] = None,
                 employee_id: Optional[int] = None,
                 client_id: Optional[int] = None,
                 product_type: Optional[str] = None,
                 contract_date_start: Optional[str] = None,
                 contract_date_end: Optional[str] = None) -> Tuple:
        """分页查询销售成果"""
        query = db.query(SalesResults).filter(SalesResults.is_deleted == 0)

        if result_id is not None:
            query = query.filter(SalesResults.result_id == result_id)
        if employee_id is not None:
            query = query.filter(SalesResults.employee_id == employee_id)
        if client_id is not None:
            query = query.filter(SalesResults.client_id == client_id)
        if product_type:
            query = query.filter(SalesResults.product_type == product_type)
        if contract_date_start:
            query = query.filter(SalesResults.contract_date >= contract_date_start)
        if contract_date_end:
            query = query.filter(SalesResults.contract_date <= contract_date_end)

        total = query.count()
        offset = (page - 1) * page_size
        items = query.order_by(SalesResults.result_id.desc()).offset(offset).limit(page_size).all()
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0

        return items, total, page, page_size, total_pages

    @staticmethod
    def update(db: Session, result_id: int, update_data: dict) -> Optional[SalesResults]:
        """更新销售成果"""
        result = SalesResultsDAO.get_by_id(db, result_id)
        if not result:
            return None

        for key, value in update_data.items():
            if value is not None and hasattr(result, key):
                setattr(result, key, value)

        db.commit()
        db.refresh(result)
        return result

    @staticmethod
    def delete(db: Session, result_id: int) -> bool:
        """删除销售成果（软删除）"""
        result = SalesResultsDAO.get_by_id(db, result_id)
        if not result:
            return False

        result.is_deleted = 1
        db.commit()
        return True
