"""
常见问题Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FaqBase(BaseModel):
    """FAQ基础Schema"""
    category: Optional[str] = Field(None, max_length=50, description='问题分类')
    question: str = Field(..., min_length=1, max_length=255, description='问题')
    answer: str = Field(..., min_length=1, description='回答')
    sort_order: int = Field(0, ge=0, description='排序权重')
    view_count: int = Field(0, ge=0, description='查看次数')
    is_active: bool = Field(True, description='是否启用')


class FaqCreate(FaqBase):
    """创建FAQ Schema"""
    pass


class FaqUpdate(BaseModel):
    """更新FAQ Schema"""
    category: Optional[str] = Field(None, max_length=50, description='问题分类')
    question: Optional[str] = Field(None, min_length=1, max_length=255, description='问题')
    answer: Optional[str] = Field(None, min_length=1, description='回答')
    sort_order: Optional[int] = Field(None, ge=0, description='排序权重')
    view_count: Optional[int] = Field(None, ge=0, description='查看次数')
    is_active: Optional[bool] = Field(None, description='是否启用')


class FaqResponse(BaseModel):
    """FAQ响应Schema"""
    faq_id: int
    category: Optional[str] = None
    question: str
    answer: str
    sort_order: int
    view_count: int
    is_active: bool
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class FaqPageResponse(BaseModel):
    """FAQ分页响应Schema"""
    items: list[FaqResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
