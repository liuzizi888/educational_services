"""
常见问题API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.faq import FaqCreate, FaqUpdate, FaqResponse, FaqPageResponse
from service.faq_service import FaqService
from typing import Optional

router = APIRouter(tags=["常见问题"])


@router.post("", response_model=FaqResponse)
def create(obj: FaqCreate, db: Session = Depends(get_db)):
    """创建FAQ"""
    return FaqService.create(db, obj)


@router.get("/page", response_model=FaqPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    faq_id: Optional[int] = None,
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """分页查询FAQ
    - faq_id: 按FAQ ID精确查询
    - category: 按问题分类筛选
    - keyword: 按问题关键词模糊查询
    - is_active: 按是否启用筛选
    """
    return FaqService.get_page(db, page, page_size, faq_id, category, keyword, is_active)


@router.get("/{faq_id}", response_model=FaqResponse)
def get_by_id(faq_id: int, db: Session = Depends(get_db)):
    """根据ID查询FAQ"""
    result = FaqService.get_by_id(db, faq_id)
    if not result:
        raise HTTPException(status_code=404, detail="FAQ不存在")
    return result


@router.put("/{faq_id}", response_model=FaqResponse)
def update(faq_id: int, obj: FaqUpdate, db: Session = Depends(get_db)):
    """更新FAQ"""
    result = FaqService.update(db, faq_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="FAQ不存在")
    return result


@router.post("/{faq_id}/view", response_model=FaqResponse)
def increment_view(faq_id: int, db: Session = Depends(get_db)):
    """增加FAQ查看次数"""
    result = FaqService.increment_view(db, faq_id)
    if not result:
        raise HTTPException(status_code=404, detail="FAQ不存在")
    return result


@router.delete("/{faq_id}")
def delete(faq_id: int, db: Session = Depends(get_db)):
    """删除FAQ（软删除）"""
    success = FaqService.delete(db, faq_id)
    if not success:
        raise HTTPException(status_code=404, detail="FAQ不存在")
    return {"code": 200, "msg": "删除成功"}
