"""
海外生活知识库API接口
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.knowledge_base_overseas import (
    KnowledgeBaseOverseasCreate,
    KnowledgeBaseOverseasUpdate,
    KnowledgeBaseOverseasResponse,
    KnowledgeBaseOverseasPageResponse
)
from service.knowledge_base_overseas_service import KnowledgeBaseOverseasService
from typing import Optional

router = APIRouter(tags=["海外生活知识库"])


@router.post("", response_model=KnowledgeBaseOverseasResponse)
def create(obj: KnowledgeBaseOverseasCreate, db: Session = Depends(get_db)):
    """创建海外生活知识库"""
    return KnowledgeBaseOverseasService.create(db, obj)


@router.get("/page", response_model=KnowledgeBaseOverseasPageResponse)
def get_page(
    page: int = 1,
    page_size: int = 10,
    kb_id: Optional[int] = None,
    country: Optional[str] = None,
    category: Optional[str] = None,
    question: Optional[str] = None,
    keywords: Optional[str] = None,
    updated_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """分页查询海外生活知识库
    - kb_id: 按知识ID精确查询
    - country: 按国家模糊查询
    - category: 按分类模糊查询
    - question: 按问题模糊查询
    - keywords: 按关键词模糊查询
    - updated_by: 按更新人ID筛选
    """
    return KnowledgeBaseOverseasService.get_page(
        db, page, page_size, kb_id, country, category, question, keywords, updated_by
    )


@router.put("/{kb_id}", response_model=KnowledgeBaseOverseasResponse)
def update(kb_id: int, obj: KnowledgeBaseOverseasUpdate, db: Session = Depends(get_db)):
    """更新海外生活知识库"""
    result = KnowledgeBaseOverseasService.update(db, kb_id, obj)
    if not result:
        raise HTTPException(status_code=404, detail="海外生活知识库不存在")
    return result


@router.delete("/{kb_id}")
def delete(kb_id: int, db: Session = Depends(get_db)):
    """删除海外生活知识库（软删除）"""
    success = KnowledgeBaseOverseasService.delete(db, kb_id)
    if not success:
        raise HTTPException(status_code=404, detail="海外生活知识库不存在")
    return {"code": 200, "msg": "删除成功"}
