"""
活动信息Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class ActivityTypeEnum(str, Enum):
    """活动类型枚举"""
    offline_saloon = "offline_saloon"
    online_webinar = "online_webinar"
    campus_fair = "campus_fair"
    training = "training"


class ActivityStatusEnum(str, Enum):
    """活动状态枚举"""
    planning = "planning"
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class ActivityInfoBase(BaseModel):
    """活动基础Schema"""
    activity_name: str = Field(..., min_length=1, max_length=100, description='活动名称')
    activity_type: Optional[ActivityTypeEnum] = Field(None, description='活动类型')
    location: Optional[str] = Field(None, max_length=255, description='活动地点')
    start_time: Optional[datetime] = Field(None, description='开始时间')
    end_time: Optional[datetime] = Field(None, description='结束时间')
    max_participants: Optional[int] = Field(None, ge=1, description='最大参与人数')
    organizer_id: Optional[int] = Field(None, description='负责人ID')
    description: Optional[str] = Field(None, description='活动描述')
    status: ActivityStatusEnum = Field(ActivityStatusEnum.planning, description='活动状态')


class ActivityInfoCreate(ActivityInfoBase):
    """创建活动Schema"""
    pass


class ActivityInfoUpdate(BaseModel):
    """更新活动Schema"""
    activity_name: Optional[str] = Field(None, min_length=1, max_length=100, description='活动名称')
    activity_type: Optional[ActivityTypeEnum] = Field(None, description='活动类型')
    location: Optional[str] = Field(None, max_length=255, description='活动地点')
    start_time: Optional[datetime] = Field(None, description='开始时间')
    end_time: Optional[datetime] = Field(None, description='结束时间')
    max_participants: Optional[int] = Field(None, ge=1, description='最大参与人数')
    organizer_id: Optional[int] = Field(None, description='负责人ID')
    description: Optional[str] = Field(None, description='活动描述')
    status: Optional[ActivityStatusEnum] = Field(None, description='活动状态')


class ActivityInfoResponse(BaseModel):
    """活动响应Schema"""
    activity_id: int
    activity_name: str
    activity_type: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_participants: Optional[int] = None
    organizer_id: Optional[int] = None
    description: Optional[str] = None
    status: str
    is_deleted: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ActivityInfoPageResponse(BaseModel):
    """活动分页响应Schema"""
    items: list[ActivityInfoResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
