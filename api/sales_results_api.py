"""
销售成果API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.sales_results import (
    SalesResultCreate,
    SalesResultUpdate,
    SalesResultResponse,
    SalesResultPageResponse
)
from service.sales_results_service import SalesResultsService
from typing import Optional

router = APIRouter(tags=["销售成果"])


@router.post("", response_model=SalesResultResponse)
def create(obj: SalesResultCreate, db: Session = Depends(get_db)):
    """创建销售成果"""
    return SalesResultsService.create(db, obj)


@router.get("/page", response_model=SalesResultPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    result_id: Optional[int] = None,
    employee_id: Optional[int] = None,
    client_id: Optional[int] = None,
    product_type: Optional[str] = None,
    contract_date_start: Optional[str] = None,
    contract_date_end: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """分页查询销售成果
    - result_id: 按销售成果ID精确查询
    - employee_id: 按员工ID筛选
    - client_id: 按客户ID筛选
    - product_type: 按产品类型筛选
    - contract_date_start: 按签约日期起筛选 (格式: YYYY-MM-DD)
    - contract_date_end: 按签约日期止筛选 (格式: YYYY-MM-DD)
    """
    return SalesResultsService.get_page(
        db, page, page_size, result_id, employee_id, client_id, product_type, contract_date_start, contract_date_end
    )


@router.get("/{result_id}", response_model=SalesResultResponse)
def get_by_id(result_id: int, db: Session = Depends(get_db)):
    """根据ID查询销售成果"""
    result = SalesResultsService.get_by_id(db, result_id)
    if not result:
        raise HTTPException(status_code=404, detail="销售成果不存在")
    return result


@router.put("/{result_id}", response_model=SalesResultResponse)
def update(result_id: int, obj: SalesResultUpdate, db: Session = Depends(get_db)):
    """更新销售成果"""
    result = SalesResultsService.update(db, result_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="销售成果不存在")
    return result


@router.delete("/{result_id}")
def delete(result_id: int, db: Session = Depends(get_db)):
    """删除销售成果（软删除）"""
    success = SalesResultsService.delete(db, result_id)
    if not success:
        raise HTTPException(status_code=404, detail="销售成果不存在")
    return {"code": 200, "msg": "删除成功"}
