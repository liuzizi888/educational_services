"""
海外生活知识库Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class KnowledgeBaseOverseasBase(BaseModel):
    """海外生活知识库基础Schema"""
    country: Optional[str] = Field(None, max_length=50, description='国家（如：英国、美国）')
    category: Optional[str] = Field(None, max_length=50, description='分类（如：安全、交通、医疗）')
    question: Optional[str] = Field(None, max_length=255, description='标准问题')
    answer: Optional[str] = Field(None, description='详细回答')
    keywords: Optional[str] = Field(None, max_length=255, description='关键词标签，用于检索')
    updated_by: Optional[int] = Field(None, description='最后更新人ID（逻辑外键）')


class KnowledgeBaseOverseasCreate(KnowledgeBaseOverseasBase):
    """创建海外生活知识库Schema"""
    pass


class KnowledgeBaseOverseasUpdate(BaseModel):
    """更新海外生活知识库Schema"""
    country: Optional[str] = Field(None, max_length=50, description='国家（如：英国、美国）')
    category: Optional[str] = Field(None, max_length=50, description='分类（如：安全、交通、医疗）')
    question: Optional[str] = Field(None, max_length=255, description='标准问题')
    answer: Optional[str] = Field(None, description='详细回答')
    keywords: Optional[str] = Field(None, max_length=255, description='关键词标签，用于检索')
    updated_by: Optional[int] = Field(None, description='最后更新人ID（逻辑外键）')


class KnowledgeBaseOverseasResponse(BaseModel):
    """海外生活知识库响应Schema"""
    kb_id: int
    country: Optional[str] = None
    category: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    keywords: Optional[str] = None
    updated_by: Optional[int] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KnowledgeBaseOverseasPageResponse(BaseModel):
    """海外生活知识库分页响应Schema"""
    items: list[KnowledgeBaseOverseasResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
