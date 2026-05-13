"""
全球留学政策Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date
from enum import Enum


class PolicyTypeEnum(str, Enum):
    """政策倾向枚举"""
    favorable = "favorable"
    tightening = "tightening"
    neutral = "neutral"


class ImpactLevelEnum(str, Enum):
    """影响程度枚举"""
    low = "low"
    medium = "medium"
    high = "high"


class GlobalStudyPolicyBase(BaseModel):
    """政策基础Schema"""
    country: str = Field(..., min_length=1, max_length=50, description='国家/地区')
    policy_category: Optional[str] = Field(None, max_length=50, description='政策分类')
    policy_type: PolicyTypeEnum = Field(PolicyTypeEnum.neutral, description='政策倾向')
    title: str = Field(..., min_length=1, max_length=255, description='政策标题')
    content: Optional[str] = Field(None, description='政策内容')
    effective_date: Optional[date] = Field(None, description='生效日期')
    impact_level: ImpactLevelEnum = Field(ImpactLevelEnum.medium, description='影响程度')
    source_url: Optional[str] = Field(None, max_length=255, description='来源链接')


class GlobalStudyPolicyCreate(GlobalStudyPolicyBase):
    """创建政策Schema"""
    pass


class GlobalStudyPolicyUpdate(BaseModel):
    """更新政策Schema"""
    country: Optional[str] = Field(None, min_length=1, max_length=50, description='国家/地区')
    policy_category: Optional[str] = Field(None, max_length=50, description='政策分类')
    policy_type: Optional[PolicyTypeEnum] = Field(None, description='政策倾向')
    title: Optional[str] = Field(None, min_length=1, max_length=255, description='政策标题')
    content: Optional[str] = Field(None, description='政策内容')
    effective_date: Optional[date] = Field(None, description='生效日期')
    impact_level: Optional[ImpactLevelEnum] = Field(None, description='影响程度')
    source_url: Optional[str] = Field(None, max_length=255, description='来源链接')


class GlobalStudyPolicyResponse(BaseModel):
    """政策响应Schema"""
    policy_id: int
    country: str
    policy_category: Optional[str] = None
    policy_type: str
    title: str
    content: Optional[str] = None
    effective_date: Optional[date] = None
    impact_level: str
    source_url: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class GlobalStudyPolicyPageResponse(BaseModel):
    """政策分页响应Schema"""
    items: list[GlobalStudyPolicyResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
