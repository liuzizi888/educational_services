"""
留学机构合作信息Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class CooperationTypeEnum(str, Enum):
    """合作类型枚举"""
    university = "university"
    agent = "agent"
    language_school = "language_school"
    service_provider = "service_provider"


class CooperationStatusEnum(str, Enum):
    """合作状态枚举"""
    active = "active"
    pending = "pending"
    terminated = "terminated"


class StudyAgencyInfoBase(BaseModel):
    """机构信息基础Schema"""
    agency_name: str = Field(..., min_length=1, max_length=100, description='机构名称')
    country: Optional[str] = Field(None, max_length=50, description='所属国家')
    contact_person: Optional[str] = Field(None, max_length=50, description='联系人')
    contact_phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    contact_email: Optional[str] = Field(None, max_length=100, description='联系邮箱')
    cooperation_type: Optional[CooperationTypeEnum] = Field(None, description='合作类型')
    cooperation_status: CooperationStatusEnum = Field(CooperationStatusEnum.active, description='合作状态')
    notes: Optional[str] = Field(None, description='合作备注')


class StudyAgencyInfoCreate(StudyAgencyInfoBase):
    """创建机构Schema"""
    pass


class StudyAgencyInfoUpdate(BaseModel):
    """更新机构Schema"""
    agency_name: Optional[str] = Field(None, min_length=1, max_length=100, description='机构名称')
    country: Optional[str] = Field(None, max_length=50, description='所属国家')
    contact_person: Optional[str] = Field(None, max_length=50, description='联系人')
    contact_phone: Optional[str] = Field(None, max_length=20, description='联系电话')
    contact_email: Optional[str] = Field(None, max_length=100, description='联系邮箱')
    cooperation_type: Optional[CooperationTypeEnum] = Field(None, description='合作类型')
    cooperation_status: Optional[CooperationStatusEnum] = Field(None, description='合作状态')
    notes: Optional[str] = Field(None, description='合作备注')


class StudyAgencyInfoResponse(BaseModel):
    """机构响应Schema"""
    agency_id: int
    agency_name: str
    country: Optional[str] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    cooperation_type: Optional[str] = None
    cooperation_status: str
    notes: Optional[str] = None
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class StudyAgencyInfoPageResponse(BaseModel):
    """机构分页响应Schema"""
    items: list[StudyAgencyInfoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
